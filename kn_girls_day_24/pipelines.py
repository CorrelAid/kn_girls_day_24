from kn_girls_day_24.get_billboard_data import billboard_hot_100_songs
from kn_girls_day_24.get_spotify_data import spotify_uris, spotify_audio_features
import pandas as pd

def get_data(limit=None, out_path="./data/data.csv"):
    billboard_df = billboard_hot_100_songs()
    if limit is not None:
        unique_artist_song_combinations = billboard_df[["artist", "song"]].drop_duplicates().to_dict(orient='records')[:limit]
    else:
        unique_artist_song_combinations = billboard_df[["artist", "song"]].drop_duplicates().to_dict(orient='records')
    print(f"{len(unique_artist_song_combinations)} unique artist, song combinations")

    uris_df = spotify_uris(unique_artist_song_combinations)
    uris = uris_df["uri"].to_list()

    audio_features_df = spotify_audio_features(uris)

    staging_df = pd.merge(uris_df, billboard_df, on=["artist", "song"], how="right")

    df = pd.merge(audio_features_df, staging_df, on=["uri"], how="right")

    df.to_csv(out_path, index=False)