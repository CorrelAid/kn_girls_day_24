from kn_girls_day_24.get_spotify_data import process_track


def test_process_track():
    track = {"artist": "T.I.", "song": "Top Back"}
    result = process_track(track)
    assert result["uri"]

    track = {"artist": "Ke$ha", "song": "TiK ToK"}
    result = process_track(track)
    assert result["uri"]

    track = {"artist": "3OH!3", "song": "Hit It Again"}
    result = process_track(track)
    assert result["uri"]

    track = {"artist": "Glee Cast", "song": "ABC"}
    result = process_track(track)
    assert result["uri"]

    track = {"artist": "112", "song": "It's Over Now"}
    result = process_track(track)
    assert result["uri"]

    track = {"artist": "U2", "song": "The Fly"}
    result = process_track(track)
    assert result["uri"]