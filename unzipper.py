import os
import tarfile
import gzip
import pandas as pd
from io import BytesIO

def extract_and_read(file_obj, dfs):
    """Recursively extract tar files and read CSV content"""
    try:
        with tarfile.open(fileobj=file_obj, mode="r:*") as tar:
            for member in tar.getmembers():
                if member.isfile():  # Skip directories
                    if member.name.endswith('.tar'):
                        # Recursively process nested tar
                        inner_file = tar.extractfile(member)
                        extract_and_read(inner_file, dfs)
                    elif member.name.endswith('.csv'):
                        # Process CSV file (might be gzipped)
                        csv_file = tar.extractfile(member)
                        process_csv(csv_file, dfs)
    except tarfile.ReadError:
        # Handle case where file is actually a gzipped CSV
        process_csv(file_obj, dfs)

def process_csv(file_obj, dfs):
    """Process CSV file that might be gzip compressed"""
    file_obj.seek(0)
    raw_data = file_obj.read()
    
    try:
        # Try to decompress as gzip
        decompressed = gzip.decompress(raw_data)
        df = pd.read_csv(BytesIO(decompressed))
    except OSError:
        # If decompression fails, read directly
        df = pd.read_csv(BytesIO(raw_data))
    
    dfs.append(df)

def main():
    root_dir = "OSMOSE"
    dfs = []
    
    for filename in os.listdir(root_dir):
        if filename.endswith('.tar'):
            filepath = os.path.join(root_dir, filename)
            with open(filepath, 'rb') as f:
                extract_and_read(f, dfs)
    
    if dfs:
        combined_df = pd.concat(dfs, ignore_index=True)
        print(f"Combined DataFrame shape: {combined_df.shape}")
        return combined_df
    else:
        print("No CSV files found")
        return pd.DataFrame()

if __name__ == "__main__":
    result_df = main()