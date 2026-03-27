import asyncio
from uvicorn import Server, Config


async def main() -> None:
    await asyncio.gather(
        run_server()
    )


async def run_server() -> None:
    config = Config(app="app.main:app", host="127.0.0.1", port=17001)
    server = Server(config)
    await server.serve()


if __name__ == '__main__':
    asyncio.run(main())
