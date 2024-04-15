from kn_girls_day_24.get_billboard_data import billboard_hot_100_songs
from kn_girls_day_24.get_spotify_data import spotify_uris, spotify_audio_features
import pandas as pd

def get_data(limit=None, out_path="./data/data.csv"):
    print("Retrieving Billboard data..")
    billboard_df = billboard_hot_100_songs()
    print(f"{len(billboard_df)} rows in billboard data")
    # We will only get spotify data for songs that have been on chart rank 1
    filtered_billboard_df = billboard_df.query("this_week == 1")
    if limit is not None:
        unique_artist_song_combinations = filtered_billboard_df[["artist", "song"]].drop_duplicates().to_dict(orient='records')[:limit]
    else:
        unique_artist_song_combinations = filtered_billboard_df[["artist", "song"]].drop_duplicates().to_dict(orient='records')
    print(f"{len(unique_artist_song_combinations)} unique artist song combinations in filtered billboard data")

    print("Retrieving Spotify uris..")
    uris_df = spotify_uris(unique_artist_song_combinations)
    uris = uris_df["uri"].to_list()

    print("Retrieving Spotify audio features..")
    audio_features_df = spotify_audio_features(uris)

    print("Merging dataframes..")
    staging_df = pd.merge(uris_df, billboard_df, on=["artist", "song"], how="right")

    df = pd.merge(audio_features_df, staging_df, on=["uri"], how="right")
    print( f"{len(df)} rows in merged data")

    df.to_csv(out_path, index=False)