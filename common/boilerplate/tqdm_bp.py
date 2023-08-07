import asyncio
from tqdm import tqdm


def complete_async_tasks(tasks, desc: str):
    with tqdm(total=len(tasks), desc=desc) as pbar:
        responses = []
        for task in asyncio.as_completed(tasks):
            response = await task
            if response is not None:
                responses.append(response)
            pbar.update()
