from scrapers.openai_scraper import GPTScraper
from scrapers.web_scraper import scrape_website
from utils.utily_funcs import subset_hyperlinks
from pathlib import Path
from io import StringIO
import pandas as pd
import numpy as np
import argparse


def main(args):

    # Instantiate ID df
    df = pd.read_csv(Path.cwd()/ args.data)

    # Instantiate GPT Scraper
    scraper = GPTScraper()

    #Instantiate Prompts
    prompt1 = args.prompt1
    prompt2 = args.prompt2

    # Instantiate Years to iterate 
    recruit_yr = [year for year in range(2006,2025)]

    # Instantiate Teams recruiting class df's
    team_df_list = []

    # Iterate through df ID'S
    for team, idx in df.iterrows():
        print("Current Team:",idx[0])
        team_df_list = []
        for year in recruit_yr:
            print("Current Year:", year)
            url = f'https://www.espn.com/college-sports/football/recruiting/school/_/id/{idx["ID"]}/class/{year}'
            print(url)

            # Scrape Website & Extract HTML
            try:
                raw_html, hyper_links = scrape_website(url)
            except Exception as e:
                print(f"Error scraping data for {url}: {e}")
                continue

            # Run GPT Scraper Commit Prompt
            try:
                cleaned_html = scraper.scrape(prompt1, raw_html)
            except Exception as e:
                print(f"Error cleaning HTML data for {url}: {e}")
                continue

            # Convert data
            data = StringIO(cleaned_html)
            team_df = pd.read_csv(data, on_bad_lines='skip')

            # Check if 'Name' column exists in team_df
            if 'Name' not in team_df.columns:
                print("'Name' column not found in team_df. Skipping to next years recruit class.")
                continue
            
            # Extract hyper links of current players in recruiting class
            hyper_links = subset_hyperlinks(team_df, hyper_links)

            # Extract raw html of each players hyperlink
            raw_htmls = [scrape_website(list(hyper_links.values())[player][0]) for player in range(len(hyper_links))]

            for hyper_link in range(len(raw_htmls)):

                if raw_htmls[hyper_link] is None:
                    print(f"Skip hyperlink {hyper_link} because raw_htmls[{hyper_link}] is None.")
                    continue

                # Call prompt2 for transforming & structuring hyperlink data
                cleaned_hyper_html = scraper.scrape(prompt2, raw_htmls[hyper_link][0])
                
                # Convert data
                data = StringIO(cleaned_hyper_html)
    
                try:
                    # Instantiate current player df
                    player_df = pd.read_csv(data)

                    # Add column names to team_df only if they don't already exist
                    if hyper_link == 0:
                        for col in player_df.columns:
                            if col not in team_df.columns:
                                team_df[col] = None

                    # Add player_df data to team_df row-wise based on the row index
                    for col in player_df.columns:
                        if col in team_df.columns:  # Ensure the column exists in team_df
                            try:
                                # Try to access the first element of player_df[col]
                                value = player_df[col].iloc[0]
                            except IndexError:
                                # If IndexError occurs, set value to NaN
                                value = np.nan
                            # Insert the value into team_df at the specified row and column
                            team_df.at[hyper_link, col] = value
                
                except pd.errors.ParserError as e:
                    print(f"Error parsing CSV data for hyperlink {hyper_link}: {e}")
                    print("Skipping to the next hyperlink.")
                    continue 
            
            # Instantiate recruting class year & team column
            team_df['Year'] = year
            team_df['Team'] = idx[0]

            # Append the current years recruiting class for the current team                    
            team_df_list.append(team_df)

        # Concatenate all DataFrames into a single DataFrame
        final_team_df = pd.concat(team_df_list, ignore_index=True)

        # Save the concatenated DataFrame to a CSV file
        team_name = idx.iloc[0]  # Use .iloc to access the value by position
        final_team_df.to_csv(f'{team_name}_recruiting_data.csv', index=False)

def cli_main():
    parser = argparse.ArgumentParser(description="Load Scraper objective")
    parser.add_argument("-p1", "--prompt1", type=str, required = False, help= "Loads memory value of key for a given scraping objective", default="Commit_Prompt")
    parser.add_argument("-p2", "--prompt2", type=str, required = False, help= "Loads memory value of key for a given scraping objective", default="Hyper_Prompt")
    parser.add_argument("-d", "--data", type=str, required=False,help = "Loads Team ID Value data for URL Scraping", default= "data/team_ids.csv")
    args = parser.parse_args()
    main(args)

if __name__ == "__main__":
    cli_main()
