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
until test -x /workspace/tools/bin/opencode && test -s /workspace/opencode.json &&
      test -s /workspace/server-password; do sleep 1; done
export OPENCODE_SERVER_PASSWORD="$(cat /workspace/server-password)"
export OPENCODE_CONFIG=/workspace/opencode.json
cd /workspace
exec /workspace/tools/bin/opencode serve --hostname 0.0.0.0 --port 4096 >> /workspace/http.log 2>&1
"""],
                env=[("NODE_EXTRA_CA_CERTS", "/etc/ssl/certs/ca-certificates.crt")],
                secrets=[boxlite.Secret(
                    name="anthropic",
                    value=getpass("Model provider API key: "),
                    hosts=["<YOUR_MODEL_HOST>"],
                )],
            ),
            name="opencode-http",
        )
        print(box.id)
        await box.start()
    except Exception as exc:
        raise SystemExit(f"{type(exc).__name__}: inspect opencode-http before retrying creation.") from None
    finally:
        runtime.close()

asyncio.run(main())
