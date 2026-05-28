import requests


def get_artwork_by_id(external_id: int):
    url = f"https://api.artic.edu/api/v1/artworks/{external_id}?fields=id,title"

    try:
        response = requests.get(url, timeout=10)
        print("External API status:", response.status_code)
        print("External API response:", response.text[:500])
    except requests.RequestException:
        print("External API error:", error)
        return None

    if response.status_code != 200:
        return None

    data = response.json().get("data")

    if data is None:
        return None

    return {
        "external_id": data.get("id"),
        "title": data.get("title") or "Unknown title",
    }
