
import pandas as pd
import os
import traceback

# Constants
INPUT_DIR = "input"
OUTPUT_DIR = "output"
REQUIRED_COLUMNS = {'folder_name', 'folder_size_mb'}

# Ensure output directory exists
os.makedirs(OUTPUT_DIR, exist_ok=True)

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

def main():
    if not os.path.exists(INPUT_DIR):
        print(f"[ERROR] Input directory '{INPUT_DIR}' not found. Please create it and place CSV files inside.")
        return

    for file in os.listdir(INPUT_DIR):
        if file.endswith(".csv"):
            input_path = os.path.join(INPUT_DIR, file)
            output_path = os.path.join(OUTPUT_DIR, f"tagged_{file}")
            print(f"[INFO] Processing {input_path}")
            try:
                df = pd.read_csv(input_path)
            except Exception as e:
                print(f"[ERROR] Failed to read CSV: {input_path}")
                traceback.print_exc()
                continue

            missing = REQUIRED_COLUMNS - set(df.columns)
            if missing:
                print(f"[ERROR] Missing required columns in {file}: {missing}")
                continue

            try:
                df['tags'] = df.apply(tag_row, axis=1)
                df.to_csv(output_path, index=False)
                print(f"[SUCCESS] Tagged file written to {output_path}")
            except Exception as e:
                print(f"[ERROR] Failed during tagging/export for {file}")
                traceback.print_exc()

    print("[DONE] All files processed.")

if __name__ == "__main__":
    main()
