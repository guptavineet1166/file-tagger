# File Tagger – AI-Ready Folder Classification Tool

This is your first modular assistant tool to auto-tag folders/files based on Julius exports.

## 🛠 How It Works

- Input: `input/julius_export.csv`
- Output: `output/tagged_output.csv`
- Rule-based tag generation (archive, project, size)
- Optional: Plug into GPT later for smart tag refinement

## ✅ To Run

```bash
python tagger.py
```

Make sure Python 3.11+ is installed.

## 💡 Future Additions

- GPT-enhanced tagging
- Archive lineage detection
- Integration into Open Interpreter or LangChain

---

## 🔃 GitHub Setup

```bash
git init
git add .
git commit -m "Initial commit: Tagger module"
```

To push to GitHub:

```bash
git remote add origin <your-repo-url>
git branch -M main
git push -u origin main
```