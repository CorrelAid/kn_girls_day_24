import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
from dotenv import load_dotenv
import pandas as pd
import concurrent.futures
import random
import time
import re
from tqdm import tqdm

max_workers = 1

def wait_jitter():
    time.sleep(random.uniform(0.2, 1.0))

def chunks(xs, n):
    n = max(1, n)
    return (xs[i:i+n] for i in range(0, len(xs), n))

def spotify_init():
    load_dotenv()
    print("Spotify credentials loaded")
    auth_manager = SpotifyClientCredentials()
    spotify = spotipy.Spotify(auth_manager=auth_manager, backoff_factor=0.5, retries=0, requests_timeout=60)
    return spotify

def clean_string(string):
    # remove dots 
    temp = re.sub(r"\.", "", string)
    # replace all non alphanumeric characters with spaces
    temp = re.sub(r"[^a-zA-Z0-9 ]", " ", temp)
    #lower string
    temp = temp.lower()
    return temp


spotify = spotify_init()

def process_track(track):
    # wait_jitter()
    artist = track["artist"]
    song = track["song"]
    cleaned_artist = clean_string(artist)
    cleaned_song = clean_string(song)
    query = f"track%3A{cleaned_song}%2520artist%3A{cleaned_artist}"   
    result = spotify.search(q=query, type="track", limit=1)
    if len(result["tracks"]["items"]) == 0:
        print(f"No results for {artist} - {song}, {query}")
        return None
    return {"uri":result["tracks"]["items"][0]["uri"], "artist":artist, "song":song}

def spotify_uris(track_lst):
    with concurrent.futures.ThreadPoolExecutor(max_workers=max_workers) as executor:
        results = list(tqdm(executor.map(process_track, track_lst), total=len(track_lst), desc="Processing Tracks"))
        
    results = [i for i in results if i is not None]
       
    df = pd.DataFrame(results)
    
    return df



def spotify_audio_features(uris):
  results = []

  def get_features(uri_chunk):
    spotify_audio_features = spotify.audio_features(uri_chunk)
    # wait_jitter()
    return spotify_audio_features

  with concurrent.futures.ThreadPoolExecutor(max_workers=max_workers) as executor:  # Adjust max_workers as needed
    # Submit tasks for each chunk of URIs
    futures = [executor.submit(get_features, chunk) for chunk in chunks(uris, 50)]

  # Add tqdm for progress bar
  for future in tqdm(concurrent.futures.as_completed(futures), total=len(futures)):
    try:
      results.extend(future.result())  # Append features from each chunk
    except Exception as e:  # Add error handling (optional)
      print(f"Error retrieving features for chunk: {e}")

  return pd.DataFrame(results)