import subprocess

def import_to_mongodb(uri, collection, csv_file):
    """
    Function to import CSV data into MongoDB using mongoimport.
    
    Args:
    - uri: MongoDB URI (e.g., "mongodb://localhost:27017/mydatabase")
    - collection: MongoDB collection name
    - csv_file: Path to the CSV file to import
    """
    # Construct the mongoimport command
    command = [
        "mongoimport",
        "--uri", uri,
        "--collection", collection,
        "--type", "csv",
        "--file", csv_file,
        "--headerline"
    ]
    
    # Execute the command using subprocess
    try:
        subprocess.run(command, check=True)
        print(f"CSV file {csv_file} imported successfully into collection '{collection}'")
    except subprocess.CalledProcessError as e:
        print(f"Error importing CSV file into MongoDB: {e}")


# Example usage
if __name__ == "__main__":
    # Example MongoDB URI (replace with your MongoDB URI)
    mongodb_uri = "mongodb://localhost:27017/mydatabase"
    
    # Example collection name
    mongodb_collection = "mycollection"
    
    # Example path to CSV file
    csv_file_path = "/path/to/your/csvfile.csv"
    
    # Call the function to import CSV into MongoDB
    import_to_mongodb(mongodb_uri, mongodb_collection, csv_file_path)
