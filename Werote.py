import argparse
import sys
import os


# ============================================================
EXPORT_TREE = True   # Output to structure file 
EXPORT_CONTENTS = True   # Output file contents
File = "werote_export"   # File name 
# ============================================================

IGNORE = {'.git', '__pycache__', 'node_modules', '.venv', 'venv', 'build', 'dist'}


def generate_tree(start_path, prefix="", ignore_dirs=None):
    if ignore_dirs is None:
        ignore_dirs = set()
    lines = []
    
    try:
        entries = sorted(os.listdir(start_path))
    except PermissionError:
        return lines

    filtered = [e for e in entries if not (os.path.isdir(os.path.join(start_path, e)) and e in ignore_dirs)]
    for i, entry in enumerate(filtered):
        full_path = os.path.join(start_path, entry)
        is_last = (i == len(filtered) - 1)
        connector = "└── " if is_last else "├── "
        lines.append(f"{prefix}{connector}{entry}")

        if os.path.isdir(full_path):
            extension = "    " if is_last else "│   "
            lines.extend(generate_tree(full_path, prefix + extension, ignore_dirs))
    return lines


def collect_files_ordered(start_path, ignore_dirs=None):
    if ignore_dirs is None:
        ignore_dirs = set()
    files = []
    try:
        entries = sorted(os.listdir(start_path))
    except PermissionError:
        return files

    for entry in entries:
        full_path = os.path.join(start_path, entry)
        if os.path.isdir(full_path) and entry in ignore_dirs:
            continue
        if os.path.isfile(full_path):
            files.append(full_path)
        elif os.path.isdir(full_path):
            files.extend(collect_files_ordered(full_path, ignore_dirs))
    return files


def read_file_content(filepath):
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            return f.read()
    except UnicodeDecodeError:
        return "[Warning: Binary file]"  
    except Exception as e:
        return f"[Error Reading: {e}]"



def get_tree_text(start_path, ignore_dirs):
    root_name = os.path.basename(start_path) or start_path
    tree_lines = [root_name] + generate_tree(start_path, ignore_dirs=ignore_dirs)
    return "\n".join(tree_lines)


def get_contents_text(start_path, ignore_dirs):
    files = collect_files_ordered(start_path, ignore_dirs=ignore_dirs)
    content_blocks = []
    for fpath in files:
        filename = os.path.basename(fpath)
        content = read_file_content(fpath)
        content_blocks.append(f"# {filename}\n{content}")
    return "\n\n".join(content_blocks)


def main():
    parser = argparse.ArgumentParser(
        description="Creates a .txt file with directory tree and file contents."
    )
    parser.add_argument("path", nargs="?", default=".", help="Path to directory (default: current)")
    parser.add_argument("-o", "--output", default=File + ".txt", help="Output filename")   # File
    parser.add_argument("--ignore", nargs="*", default=[], help="Additional directories to ignore")
    args = parser.parse_args()

    start_path = os.path.abspath(args.path)
    output_file = args.output
    
    if not os.path.isdir(start_path):
        print(f"Error: '{start_path}' is not a directory.")
        sys.exit(1)

    ignore_dirs = IGNORE.union(set(args.ignore))
    print(f"Scan...\n   {start_path}")


    output_parts = []
    if EXPORT_TREE:
        output_parts.append(get_tree_text(start_path, ignore_dirs))
    if EXPORT_CONTENTS:
        output_parts.append(get_contents_text(start_path, ignore_dirs))

    if not output_parts:
        print("Warning: Both export modes are disabled.")
        full_output = ""
    else:
        full_output = "\n\n".join(output_parts) + "\n"

    try:
        with open(output_file, "w", encoding="utf-8") as f:
            f.write(full_output)
        print(f"Successfully saved to '{output_file}'")
    except IOError as e:
        print(f"Write error: {e}")
        sys.exit(1)


if 1 == 1:
    main()