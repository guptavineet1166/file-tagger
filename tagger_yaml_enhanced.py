
import pandas as pd
import os
import traceback
import yaml

# Constants
INPUT_DIR = "input"
OUTPUT_DIR = "output"
RULES_FILE = "tag_rules.yaml"
REQUIRED_COLUMNS = {'folder_name', 'folder_size_mb'}

# Ensure output directory exists
os.makedirs(OUTPUT_DIR, exist_ok=True)

def load_rules(yaml_path):
    try:
        with open(yaml_path, 'r') as f:
            config = yaml.safe_load(f)
            return config.get("rules", [])
    except Exception as e:
        print(f"[ERROR] Failed to load tag rules from {yaml_path}: {e}")
        return []

def evaluate_condition(row, condition):
    try:
        folder_name = str(row.get('folder_name', '')).lower()
        folder_size_mb = float(row.get('folder_size_mb', 0) or 0)
        return eval(condition)
    except Exception as e:
        print(f"[ERROR] Evaluating condition '{condition}' failed on row {row}: {e}")
        return False

def tag_row(row, rules):
    tags = []
    for rule in rules:
        condition = rule.get("condition", "")
        tag = rule.get("tag", "")
        if evaluate_condition(row, condition):
            tags.append(tag)
    return " ".join(tags)

def main():
    if not os.path.exists(INPUT_DIR):
        print(f"[ERROR] Input directory '{INPUT_DIR}' not found. Please create it and place CSV files inside.")
        return

    rules = load_rules(RULES_FILE)

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
                df['tags'] = df.apply(lambda row: tag_row(row, rules), axis=1)
                df.to_csv(output_path, index=False)
                print(f"[SUCCESS] Tagged file written to {output_path}")
            except Exception as e:
                print(f"[ERROR] Failed during tagging/export for {file}")
                traceback.print_exc()

    print("[DONE] All files processed.")

if __name__ == "__main__":
    main()
