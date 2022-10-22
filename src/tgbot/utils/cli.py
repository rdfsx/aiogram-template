import asyncio


async def create_cli_process(cmd: list[str]) -> tuple[bytes, bytes]:
    proc = await asyncio.create_subprocess_shell(
        " ".join(cmd),
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.PIPE,
    )
    return await proc.communicate()
