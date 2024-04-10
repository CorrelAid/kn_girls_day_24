import requests

def test_spotify_request():
    url = "https://api.spotify.com/v1/search?query=track%253Asexy%252520artist%253Amfsb&type=track&offset=0&limit=1"
    headers = {
        "Authorization": "Bearer BQCjgYKWEvYVvEUAauHL13XMxdXp3GQKvm7F5GpIDjBKKmTNbSY77icyZ3q28XozjrhGwdTmDjvwZ9ryj8CVUiRrLaCZQ_cKuaXH-0gmD0F74-sByqM"
    }

    response = requests.get(url, headers=headers)

    print(response.text)
    print(f"{int(response.headers['Retry-After'])/60/60} hours to retry")

    assert response.status_code == 200

    