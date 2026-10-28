import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry




def create_session(
    retries: int = 5,
    backoff_factor: float = 0.3,
    status_forcelist=(429, 500, 502, 503, 504),
) -> requests.Session:

    retry_strategy = Retry(
        total=retries,
        connect=retries,
        read=retries,
        status=retries,
        backoff_factor=backoff_factor,
        status_forcelist=status_forcelist,
        allowed_methods=frozenset({"GET"}),
        respect_retry_after_header=True,
    )

    adapter = HTTPAdapter(
        max_retries=retry_strategy,
        pool_connections=10,
        pool_maxsize=10,
    )

    session = requests.Session()
    session.mount("https://", adapter)
    session.mount("http://", adapter)
    return session
