import requests


def get_word_by_id(external_id: int):
    url = f"https://api.artic.edu/api/v1/works/{external_id}"

    try:
        response = requests.get(url, timeout=10)
    except requests.RequestException:
        return None

    if response.status_code != 200:
        return None

    data = response.json().get("data")

    if data is None:
        return None

    return {
        "external_id": data["id"],
        "title": data.get("title", "Unknown"),
    }
