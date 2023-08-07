import time
import requests
from random_user_agent.user_agent import UserAgent
from random_user_agent.params import SoftwareName, OperatingSystem


def create_session(cookies: dict = None) -> requests.Session:
    session = requests.Session()

    software_names = [SoftwareName.CHROME.value]
    operating_systems = [OperatingSystem.WINDOWS.value, OperatingSystem.LINUX.value]
    ua_provider = UserAgent(software_names=software_names, operating_systems=operating_systems, limit=10)

    headers = {
        'User-Agent': ua_provider.get_random_user_agent(),
        'Accept-Language': 'en-US,en;q=0.5',
        'Accept-Encoding': 'gzip, deflate, br',
        'Connection': 'keep-alive',
        'Cache-Control': 'max-age=0'
    }

    session.headers.update(headers)
    session.cookies.update(cookies)

    return session


def get(
        session: requests.Session,
        url: str,
        timeout: float = 10,
        retry_after: float = 5,
        max_retries: int = 3,
        **kwargs) -> requests.Response:
    retries = 0

    while retries < max_retries:
        try:
            response = session.get(url, timeout=timeout, **kwargs)
            response.raise_for_status()
            return response
        except requests.exceptions.RequestException as e:
            print(f"Error getting {url}: {e}")
            time.sleep(retry_after)
            retries += 1

    raise requests.exceptions.RequestException(f"Max retries reached. Unable to get a successful response from {url}")
