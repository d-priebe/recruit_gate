import pandas as pd
import requests
from urllib.parse import quote
import time
from pathlib import Path


def fetch_location_details(query, user_agent="MyPythonScript"):
    base_url = "https://nominatim.openstreetmap.org/search"
    # Directly encode the unencoded query string
    encoded_query = quote(query)
    params = f'q={encoded_query}&format=json&limit=1'
    headers = {'User-Agent': user_agent}

    full_url = f"{base_url}?{params}"
    print(f"Requesting: {full_url}")  # Debug the full URL

    response = requests.get(base_url, headers=headers, params={'q': query, 'format': 'json', 'limit': 1})

    print(f"Requesting: {response.url}")  # Debug URL being requested
    
    if response.status_code == 200:
        results = response.json()
        print(f"Results for '{query}':", results)  # Debug response data
        if results:
            return (results[0].get('lat'), results[0].get('lon'),
                    results[0].get('osm_id'), results[0].get('osm_type'), results[0].get('display_name'))
        else:
            return (None, None, None, None, None)
    else:
        print(f"Failed to fetch '{query}', Status Code: {response.status_code}, Reason: {response.reason}")
        return (None, None, None, None, None)


def add_location_details_to_df(df):
    latitudes, longitudes, osm_ids, osm_types, location_data = [], [], [], [], []
    for _, row in df.iterrows():
        hs_name = row['hs_name']
        query = f"{row['hs_name']} High school, {row['city_state']}"
        lat, lon, osm_id, osm_type, display_names = fetch_location_details(query)
        latitudes.append(lat)
        longitudes.append(lon)
        osm_ids.append(osm_id)
        osm_types.append(osm_type)
        location_data.append(display_names)
        #time.sleep(1)  

    df['latitude'] = latitudes
    df['longitude'] = longitudes
    df['osm_id'] = osm_ids
    df['osm_type'] = osm_types
    df['location_info'] = location_data

if __name__ == "__main__":
    file_path = Path.cwd() / 'data/recruit_data_10_25.csv'
    df = pd.read_csv(file_path)
    add_location_details_to_df(df)
    updated_file_path = Path.cwd() / 'updated_recruit_data_10_25.csv'
    df.to_csv(updated_file_path, index=False)
    print(f"Updated data saved to {updated_file_path}")

