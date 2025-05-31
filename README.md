# File Tagger – AI-Ready Folder Classification Tool

## 🚀 What This Tool Does

File Tagger is a modular Python tool to auto-tag folders/files based on rule-driven logic, making it easy to organize and search large exports (such as from Julius or similar systems).  
It supports simple hardcoded rules, YAML-based rule configuration, and extensible logic for robust, AI-ready classification.

**Main Features:**
- Batch-process CSV exports of folder/file metadata.
- Tag files/folders with rules like `#archive`, `#project_codebase`, `#large`, etc.
- YAML-based rule customization for flexible, maintainable tagging.
- Handles multiple CSVs at once.
- Designed for easy future integration with GPT or other AI for smart tagging.

---

## 🛠️ How To Use

### 1. Prerequisites

- Python 3.11+ is recommended.
- Install dependencies:
  ```
  pip install -r requirements.txt
  ```

### 2. Prepare Data

- Place your CSV export(s) in:
  ```
  D:\AI-Projects\file-tagger\input
  ```
- (CSV should contain at least `folder_name` and `folder_size_mb` columns.)

### 3. Run the Tagger

- For single-file tagging:
  ```
  python tagger.py
  ```
- For batch processing and YAML rule support:
  ```
  python tagger_enhanced.py
  python tagger_robust_adaptive.py
  python tagger_yaml_enhanced.py
  ```

### 4. Check Output

- Tagged files will be written to:
  ```
  D:\AI-Projects\file-tagger\output
  ```

---

## 📝 Sample CSV Input

```csv
folder_name,folder_size_mb
python_project,1200
archive_zip,5000
my_data_folder,100
important_project,4000
```

---

## 🧩 Customizing Rules

Edit `tag_rules.yaml` to add or modify tagging logic.  
Example (YAML):

```yaml
rules:
  - condition: "'zip' in folder_name or 'rar' in folder_name"
    tag: '#archive'
  - condition: "'python' in folder_name or 'project' in folder_name"
    tag: '#project_codebase'
  - condition: folder_size_mb > 3000
    tag: '#large'
```
- Use `folder_name` (as lowercase string) and `folder_size_mb` (as float) in conditions.
- Rules are evaluated for each row; tags are added if the condition is true.

---

## ⚠️ Notes & Best Practices

- **Do not commit large CSV data or outputs:** The `.gitignore` is set up to prevent this.
- **Security:** Avoid using untrusted YAML rules (as they are evaluated with `eval`).
- **Extend:** You can add more scripts for AI-based tagging or integrate with cloud pipelines.

---

## 💡 Future Additions

- GPT-enhanced tagging.
- Archive lineage detection.
- Integration into Open Interpreter or LangChain.

---

## 🤝 Contributing

Feel free to fork and submit PRs for new rules, bugfixes, or AI integrations!
