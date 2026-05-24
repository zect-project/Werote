# Werote

**An open-source utility for creating .txt files with the structure and contents of files for coding with AI.**

Werote helps developers quickly export a project's directory tree and file contents into a single, well-formatted text file — perfect for feeding your entire codebase to AI models like Claude, GPT, Grok, or Cursor.

---

## ✨ Features

- **Directory Tree**: Clean, visual tree structure with proper indentation
- **File Contents**: All files concatenated with clear headers
- **Smart Filtering**: Ignores common unnecessary directories (`.git`, `__pycache__`, `node_modules`, etc.)
- **Binary File Handling**: Gracefully skips or warns on binary files
- **Customizable**: Command-line options for output file and additional ignores
- **Simple & Lightweight**: Single Python file, no dependencies

---

## 📥 Installation

### 1. Clone the repository:
   ```bash
   git clone https://github.com/zect-project/Werote.git
   ```
### 2. Use
   ```bash
   python C:\holl\Starts\Werote.py C:\holl\python\test
   ```

  ### werote_export.txt:
   ```
      test                  <- Tree
         └── tester.py

      # tester.py               <- File contents
      print("Hellow World!")
   ```
