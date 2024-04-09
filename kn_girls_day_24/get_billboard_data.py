import requests
from datetime import datetime, date
import pandas as pd

def get_gh_data():
    response = requests.get("https://raw.githubusercontent.com/mhollingshead/billboard-hot-100/main/all.json")
    response.raise_for_status()
    return response.json()

def billboard_hot_100_songs(min_date: date = date(1958, 8, 4), max_date: date = date(2024, 4, 8) ):
    gh_data = get_gh_data()
    start_idx = next((i for i, chart in enumerate(gh_data) if datetime.strptime(chart["date"], "%Y-%m-%d").date() >= min_date), 0)
    end_idx = next((i for i, chart in enumerate(gh_data[start_idx:]) if datetime.strptime(chart["date"], "%Y-%m-%d").date() > max_date), len(gh_data[start_idx:])) + start_idx
    charts = [chart for chart in gh_data[start_idx:end_idx]]
    chart_data_lst = []
    for chart in charts:
        for chart_data in chart["data"]:
            chart_data.update({"date": chart["date"]}) 
            chart_data_lst.append(chart_data)
    df = pd.DataFrame(chart_data_lst)  
    return df

        

