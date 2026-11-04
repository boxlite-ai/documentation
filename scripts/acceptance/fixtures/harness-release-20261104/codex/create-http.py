import asyncio
from getpass import getpass
import boxlite

async def main():
    runtime = boxlite.Boxlite.rest(boxlite.BoxliteRestOptions.from_env())
    try:
        box = await runtime.create(
            boxlite.BoxOptions(
                image="node",
                cpus=1, memory_mib=2048, disk_size_gb=10,
                auto_stop=120, auto_resume=True, auto_delete=0, detach=True,
                network=boxlite.NetworkSpec(inbound=boxlite.InboundNetworkSpec(mode="enabled")),
                entrypoint=["/bin/sh", "-c"],
                cmd=["""
until test -x /workspace/tools/bin/codex && test -s /workspace/codex/config.toml &&
      test -s /workspace/server.mjs && test -s /workspace/http-token.sha256; do sleep 1; done
exec node /workspace/server.mjs >> /workspace/http.log 2>&1
"""],
                env=[
                    ("SSL_CERT_FILE", "/etc/ssl/certs/ca-certificates.crt"),
                    ("CODEX_API_KEY", "<BOXLITE_SECRET:openai>"),
                ],
                secrets=[boxlite.Secret(
                    name="openai",
                    value=getpass("Model provider API key: "),
                    hosts=["<YOUR_MODEL_HOST>"],
                )],
            ),
            name="codex-http",
        )
        print(box.id)
        await box.start()
    except Exception as exc:
        raise SystemExit(f"{type(exc).__name__}: inspect codex-http before retrying creation.") from None
    finally:
        runtime.close()

asyncio.run(main())
