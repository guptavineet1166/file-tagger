
import pandas as pd
import os
import traceback
import yaml
from difflib import get_close_matches

INPUT_DIR = "input"
OUTPUT_DIR = "output"
RULES_FILE = "tag_rules.yaml"
REQUIRED_FIELDS = ['folder_name', 'folder_size_mb']

os.makedirs(OUTPUT_DIR, exist_ok=True)

def load_rules(path):
    try:
        with open(path, 'r') as f:
            config = yaml.safe_load(f)
            return config.get('rules', [])
    except Exception as e:
        print(f"[ERROR] Unable to load rules: {e}")
        return []

def find_column_match(possible_names, columns, cutoff=0.6):
    for name in possible_names:
        matches = get_close_matches(name, columns, n=1, cutoff=cutoff)
        if matches:
            return matches[0]
    return None

def map_columns(df):
    mapped = {}
    for field in REQUIRED_FIELDS:
        match = find_column_match([field], df.columns)
        if match:
            mapped[field] = match
        else:
            mapped[field] = None
    return mapped

def safe_eval_condition(row, condition, field_map):
    try:
        local_vars = {}
        for key in REQUIRED_FIELDS:
            col = field_map.get(key)
            value = row.get(col) if col else None
            if key == 'folder_name' and value:
                value = str(value).lower()
            if key == 'folder_size_mb' and value:
                try:
                    value = float(value)
                except:
                    value = 0
            local_vars[key] = value
        return eval(condition, {}, local_vars)
    except Exception as e:
        print(f"[WARN] Eval error on row: {e}")
        return False

def tag_row(row, rules, field_map):
    tags = []
    for rule in rules:
        condition = rule.get("condition", "")
        tag = rule.get("tag", "")
        if safe_eval_condition(row, condition, field_map):
            tags.append(tag)
    return " ".join(tags)

def main():
    if not os.path.exists(INPUT_DIR):
        print(f"[ERROR] Input directory '{INPUT_DIR}' not found.")
        return

    rules = load_rules(RULES_FILE)

    for file in os.listdir(INPUT_DIR):
        if not file.endswith(".csv"):
            continue

        input_path = os.path.join(INPUT_DIR, file)
        output_path = os.path.join(OUTPUT_DIR, f"tagged_{file}")
        print(f"[INFO] Processing {file}...")

        try:
            df = pd.read_csv(input_path)
        except Exception as e:
            print(f"[ERROR] Could not read '{file}': {e}")
            continue

        field_map = map_columns(df)
        if not field_map['folder_name'] and not field_map['folder_size_mb']:
            print(f"[WARN] No usable columns found in '{file}' — skipping.")
            continue

        try:
            df['tags'] = df.apply(lambda row: tag_row(row, rules, field_map), axis=1)
            df.to_csv(output_path, index=False)
            print(f"[SUCCESS] Tagged file saved as {output_path}")
        except Exception as e:
            print(f"[ERROR] Failed tagging/export for '{file}': {e}")

    print("[DONE] All files processed.")

if __name__ == "__main__":
    main()
