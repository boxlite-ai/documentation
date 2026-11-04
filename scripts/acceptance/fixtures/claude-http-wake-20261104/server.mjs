import http from 'node:http';
import { readFileSync } from 'node:fs';
import { createHash, timingSafeEqual } from 'node:crypto';
import { execFile } from 'node:child_process';

const tokenHash = Buffer.from(readFileSync('/workspace/http-token.sha256', 'utf8').trim(), 'hex');
if (tokenHash.length !== 32) throw new Error('Invalid HTTP token hash');
let busy = false;

function reply(res, status, body) {
  res.writeHead(status, { 'Content-Type': 'application/json' });
  res.end(JSON.stringify(body));
}

const server = http.createServer(async (req, res) => {
  const authorization = req.headers.authorization ?? '';
  const token = authorization.slice(7);
  const suppliedHash = createHash('sha256').update(token).digest();
  if (!authorization.startsWith('Bearer ') || !timingSafeEqual(suppliedHash, tokenHash)) {
    return reply(res, 401, { error: 'Unauthorized' });
  }
  if (req.method === 'GET' && req.url === '/health') {
    return reply(res, 200, { ready: true, busy });
  }
  if (req.method !== 'POST' || req.url !== '/tasks') {
    return reply(res, 404, { error: 'Use POST /tasks' });
  }

  let prompt;
  try {
    req.setEncoding('utf8');
    let body = '';
    for await (const chunk of req) {
      body += chunk;
      if (Buffer.byteLength(body) > 65536) {
        return reply(res, 413, { error: 'Request too large' });
      }
    }
    ({ prompt } = JSON.parse(body));
    if (typeof prompt !== 'string' || !prompt.trim()) throw new Error('Invalid prompt');
  } catch {
    return reply(res, 400, { error: 'Send JSON with a nonempty prompt string' });
  }
  if (busy) return reply(res, 409, { error: 'A task is already running' });
  busy = true;

  const abort = new AbortController();
  res.on('close', () => { if (!res.writableEnded) abort.abort(); });
  const child = execFile('/workspace/tools/bin/claude', [
    '--permission-mode', 'bypassPermissions', '--output-format', 'json', '-p', prompt,
  ], {
    cwd: '/workspace', detached: true, timeout: 180000, killSignal: 'SIGKILL',
    maxBuffer: 2 * 1024 * 1024, signal: abort.signal,
  }, (error, stdout) => {
    busy = false;
    if (error && child.pid) {
      try { process.kill(-child.pid, 'SIGKILL'); } catch {}
    }
    if (res.destroyed) return;
    try {
      const result = JSON.parse(stdout);
      return reply(res, error || result.is_error ? 502 : 200, result);
    } catch {
      return reply(res, error?.killed ? 504 : 502, { error: 'Claude did not return a result' });
    }
  });
  child.stdin.end();
});

server.requestTimeout = 30000;
server.listen(8080, '0.0.0.0');
