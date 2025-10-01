from pathlib import Path
import json

def load_context(context_dir="context"):
    """
    Load all JSON files from the context directory and return combined text.
    """
    context_path = Path(context_dir)
    context_path.mkdir(exist_ok=True)

    all_content = ""
    for file_path in context_path.glob("*.json"):
        if file_path.is_file():
            try:
                with file_path.open(encoding="utf-8") as f:
                    data = json.load(f)
                    all_content += f"\n=== {file_path.name} ===\n{json.dumps(data, indent=2)}\n"
            except Exception as e:
                print(f"Failed to load {file_path.name}: {e}")

    return all_content.strip() or "No context files found"
