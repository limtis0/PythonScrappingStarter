import asyncio
import httpx
from random_user_agent.user_agent import UserAgent
from random_user_agent.params import SoftwareName, OperatingSystem


def create_client(cookies: dict = None) -> httpx.AsyncClient:
    software_names = [SoftwareName.CHROME.value]
    operating_systems = [OperatingSystem.WINDOWS.value, OperatingSystem.LINUX.value]
    ua_provider = UserAgent(software_names=software_names, operating_systems=operating_systems, limit=10)

    async_client = httpx.AsyncClient(
        headers={
            'User-Agent': ua_provider.get_random_user_agent(),
            'Accept-Language': 'en-US,en;q=0.5',
            'Accept-Encoding': 'gzip, deflate, br',
            'Connection': 'keep-alive',
            'Cache-Control': 'max-age=0'
        },
        cookies=cookies
    )

    return async_client


async def get(
        client: httpx.AsyncClient,
        url: str,
        timeout: float = 10,
        retry_after: float = 5,
        max_retries: int = 3,
        verbose: bool = False,
        **kwargs) -> httpx.Response:
    retries = 0

    while retries < max_retries:
        try:
            response = await client.get(url, timeout=timeout, **kwargs)
            response.raise_for_status()
            return response
        except httpx.RequestError as e:
            if verbose:
                print(f"Error getting {url}: {e}")
            await asyncio.sleep(retry_after)
            retries += 1

    raise httpx.RequestError(f"Max retries reached. Unable to get a successful response from {url}")
