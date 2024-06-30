import requests
from bs4 import BeautifulSoup
import re
import pandas as pd

def scrape_website(url):
    """Fetch the website content."""
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')
        text = soup.get_text()
        return text
    except requests.RequestException as e:
        print(f"Request failed: {e}")

def extract_data(text, year):
    """Extract structured data from the text."""
    refined_pattern = r"(\d+)\s+(\d+)\s+([^\d]+?)\s{2,}([^\(]+?)\s+\(([^)]+?)\)\s+(Edge|[A-Z]+)\s+(\d+-\d+(?:\.\d+)?)\s*\/\s*(\d+)\s+(\d+)\s+(\d+)\s+(\d+)\s+(\d+)"
    extracted_data = re.findall(refined_pattern, text)

    structured_data = []
    for entry in extracted_data:
        # Safely split height and weight to prevent IndexError
        height_weight = entry[6].split('/')
        height = height_weight[0].strip() if len(height_weight) > 0 else ""
        weight = height_weight[1].strip() if len(height_weight) > 1 else ""

        structured_data.append({
            "year": year,
            "rank": entry[0],
            "name": entry[2].strip(),
            "hs_name": entry[3].strip(),
            "city_state": entry[4],
            "pos": entry[5],
            "height": height,
            "weight": entry[7],
            "24/7_rating": entry[8], 
            "nat_ovr": entry[9],
            "pos_ovr": entry[10],
            "state_ovr": entry[11]
        })

    return structured_data

def main():
    """Main function to orchestrate the scraping and data structuring."""
    master_df = pd.DataFrame()

    for year in range(2010, 2025):
        url = f"https://247sports.com/Season/{year}-Football/RecruitRankings/?InstitutionGroup=highschool"
        text = scrape_website(url)
        # Preprocess the text to isolate relevant section
        if " Edit    \n     Top247 247Sports Composite    Rank Player Pos Ht / Wt Rating Team      " in text:
            text = text.split(" Edit    \n     Top247 247Sports Composite    Rank Player Pos Ht / Wt Rating Team      ")[1]
        if "Signed            Recruit Search Football     Football Basketball" in text:
            text = text.split("Signed            Recruit Search Football     Football Basketball")[0]
        structured_data = extract_data(text, year)
        df_year = pd.DataFrame(structured_data)
        master_df = pd.concat([master_df, df_year], ignore_index=True)

    # Save the accumulated data to a CSV file
    master_df.to_csv("example_data.csv", index=False)
    print("Data has been successfully saved to 'example_data.csv'.")

if __name__ == "__main__":
    main()
