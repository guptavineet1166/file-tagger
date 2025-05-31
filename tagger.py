import pandas as pd
import os
import traceback

# File paths
INPUT_PATH = "input/julius_export.csv"
OUTPUT_PATH = "output/tagged_output.csv"

# Custom tagging logic
def tag_row(row):
    tags = []
    try:
        name = str(row.get('folder_name', '')).lower()
        size = float(row.get('folder_size_mb', 0) or 0)

        if "zip" in name or "rar" in name:
            tags.append("#archive")
        if "python" in name or "project" in name:
            tags.append("#project_codebase")
        if size > 3000:
            tags.append("#large")
    except Exception as e:
        tags.append("#error-tagging")
        print(f"[Tagging Error] Row: {row} | Error: {e}")
    return " ".join(tags)

# Main execution block
def main():
    if not os.path.exists(INPUT_PATH):
        print(f"[ERROR] Input file not found: {INPUT_PATH}")
        print("Please check the file name and make sure it's placed inside the 'input/' folder.")
        return

    try:
        df = pd.read_csv(INPUT_PATH)
    except Exception as e:
        print(f"[ERROR] Failed to read CSV: {INPUT_PATH}")
        traceback.print_exc()
        return

    required_columns = {'folder_name', 'folder_size_mb'}
    missing_columns = required_columns - set(df.columns)
    if missing_columns:
        print(f"[ERROR] Missing required columns in input CSV: {missing_columns}")
        return

    try:
        df['tags'] = df.apply(tag_row, axis=1)
        os.makedirs(os.path.dirname(OUTPUT_PATH), exist_ok=True)
        df.to_csv(OUTPUT_PATH, index=False)
        print(f"[SUCCESS] Tagged output written to: {OUTPUT_PATH}")
    except Exception as e:
        print(f"[ERROR] Failed during tagging or CSV export.")
        traceback.print_exc()

if __name__ == "__main__":
    main()