import asyncio
from uvicorn import Config, Server


async def main() -> None:
    await asyncio.gather(
        run_server()
    )


async def run_server() -> None:
    config = Config(app="controllers.messages:app", host="127.0.0.1", port=17001, reload=False)
    server = Server(config)
    await server.serve()


if __name__ == '__main__':
    asyncio.run(main())
