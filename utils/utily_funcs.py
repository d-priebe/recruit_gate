
def subset_hyperlinks(df, hyper_links):
    # Dictionary to store matches
    matched_urls = {}

    # Iterate over DFrows
    for index, row in df.iterrows():
        # Preprocess the name for URL matching
        processed_name = row['Name'].replace('.', '').replace(' ', '-').lower()

        # Check each URL
        for url in hyper_links:
            # Check if the processed name is in the URL
            if processed_name in url:
                # If the name key exists, append to the list; else, create a new list
                if row['Name'] in matched_urls:
                    matched_urls[row['Name']].append(url)
                else:
                    matched_urls[row['Name']] = [url]

    return matched_urls 


def open_file(filepath):
        with open(filepath, 'r', encoding='utf-8') as infile:
            return infile.read()