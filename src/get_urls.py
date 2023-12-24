import requests

from params import urls_path

headers = {
    "authority": "success.outsystems.com",
    "accept": "application/json",
    "accept-language": "en-GB,en-US;q=0.9,en;q=0.8",
    "cache-control": "no-cache",
    "content-type": "application/json; charset=UTF-8",
    "origin": "https://success.outsystems.com",
    "outsystems-locale": "en-US",
    "pragma": "no-cache",
    "referer": "https://success.outsystems.com/documentation/11/getting_started/",
    "sec-ch-ua": '"Not_A Brand";v="8", "Chromium";v="120", "Google Chrome";v="120"',
    "sec-ch-ua-mobile": "?0",
    "sec-ch-ua-platform": '"macOS"',
    "sec-fetch-dest": "empty",
    "sec-fetch-mode": "cors",
    "sec-fetch-site": "same-origin",
    "user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "x-csrftoken": "T6C+9iB49TLra4jEsMeSckDMNhQ=",
}

request_body = {
    "versionInfo": {
        "moduleVersion": "H2phGW_5VEoOz1+AM5VctA",
        "apiVersion": "nVTN1tuxAJUhAtnTJAGwiQ",
    },
    "viewName": "Documentation.Documentation",
    "screenData": {
        "variables": {
            "MultipleItems": True,
            "ContentGUID": "036994b9-0656-4dc8-8b94-b0c4e9d71a1f",
            "_contentGUIDInDataFetchStatus": 1,
            "RepoSection": "11",
            "_repoSectionInDataFetchStatus": 1,
            "LocaleId": "en-US",
            "_localeIdInDataFetchStatus": 1,
        },
    },
}


def parse_data(data: list[dict]):
    """Extracts a list of URLs from data."""

    for d in data:
        for k, v in d.items():
            if k == "URL":
                yield v
            if isinstance(v, dict):
                nested_list = v.get("List")
                if nested_list is not None:
                    yield from parse_data(nested_list)


def main(url: str):
    response = requests.post(
        url=url,
        headers=headers,
        json=request_body,
    )

    print(f"{response.status_code=}")
    assert response.status_code == 200, "Response status code is not 200"

    response_body = response.json()

    data = response_body["data"]["Hierarchy"]["List"]
    urls = sorted(set(parse_data(data)))

    print("urls retrived:", len(urls))

    if not urls_path.parent.exists():
        urls_path.parent.mkdir()

    with open(urls_path, mode="w") as f:
        for url in urls:
            f.write(url + "\n")


if __name__ == "__main__":
    toc = "https://success.outsystems.com/screenservices/Documentation_UI/TOC/LeftTableOfContents/DataActionGetLeftToCDataSource"

    main(toc)
