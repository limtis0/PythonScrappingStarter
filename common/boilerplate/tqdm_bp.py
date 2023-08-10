import asyncio
from tqdm.asyncio import tqdm


async def gather_with_concurrency(n_workers: int, *coroutines):
    semaphore = asyncio.Semaphore(n_workers)

    async def semaphore_coroutine(coroutine):
        async with semaphore:
            return await coroutine

    return await tqdm.gather(*(semaphore_coroutine(c) for c in coroutines))
