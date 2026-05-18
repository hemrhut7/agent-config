"""
Reflect_On_Error(error_message) — Auto-triggered error analysis and persistence.

When a script execution fails, this module:
1. Parses the error for key patterns (module, traceback, error type)
2. Searches existing topics/ for related anti-patterns
3. Generates a structured pitfall entry
4. Saves via Save_To_LongTerm to prevent repeating the same mistake

Usage:
    python -u scripts/reflect.py "ModuleNotFoundError: No module named 'cv2'"
    python -u scripts/reflect.py --file error_log.txt
"""

import argparse
import json
import re
import sys
from pathlib import Path


def get_memory_root() -> Path:
    return Path(__file__).resolve().parent.parent


def parse_error(error_message: str) -> dict:
    """
    Extract structured information from an error message.

    Returns:
        dict with: error_type, module, key_message, traceback_files
    """
    result = {
        "error_type": "Unknown",
        "module": "",
        "key_message": error_message.strip().split("\n")[-1] if error_message.strip() else "",
        "traceback_files": [],
    }

    # Extract error type (e.g., ModuleNotFoundError, ValueError, etc.)
    type_match = re.search(r"(\w+Error|\w+Exception|\w+Warning):\s*(.+)", error_message)
    if type_match:
        result["error_type"] = type_match.group(1)
        result["key_message"] = type_match.group(2).strip()

    # Extract module from ModuleNotFoundError
    module_match = re.search(r"No module named ['\"](\w+)['\"]", error_message)
    if module_match:
        result["module"] = module_match.group(1)

    # Extract file references from traceback
    file_matches = re.findall(r'File "([^"]+)", line (\d+)', error_message)
    result["traceback_files"] = [
        {"file": f, "line": int(l)} for f, l in file_matches
    ]

    return result


def search_existing_pitfalls(error_info: dict, memory_root: Path) -> list[dict]:
    """Check if similar pitfalls already exist in topics/."""
    topics_dir = memory_root / "topics"
    if not topics_dir.exists():
        return []

    matches = []
    search_terms = [
        error_info["error_type"].lower(),
        error_info["module"].lower(),
    ]
    search_terms = [t for t in search_terms if t]

    for md_file in topics_dir.glob("*.md"):
        try:
            content = md_file.read_text(encoding="utf-8").lower()
            for term in search_terms:
                if term in content:
                    matches.append({
                        "file": str(md_file.relative_to(memory_root)),
                        "matched_term": term,
                    })
                    break
        except (OSError, UnicodeDecodeError):
            continue

    return matches


def generate_pitfall_entry(error_info: dict, error_message: str) -> str:
    """Generate a structured pitfall markdown entry."""
    lines = [
        f"**Pitfall: {error_info['error_type']}**",
        f"- **Trigger**: {error_info['key_message']}",
    ]

    if error_info["module"]:
        lines.append(f"- **Module**: `{error_info['module']}`")

    if error_info["traceback_files"]:
        files_str = ", ".join(
            f"`{tf['file']}:{tf['line']}`" for tf in error_info["traceback_files"][:3]
        )
        lines.append(f"- **Location**: {files_str}")

    lines.extend([
        f"- **Fix**: (to be determined after root cause analysis)",
        f"- **Prevention**: (to be determined)",
    ])

    return "\n".join(lines)


def reflect_on_error(
    error_message: str,
    memory_root: Path | None = None,
    auto_save: bool = True,
) -> dict:
    """
    Main entry point for Reflect_On_Error.

    Args:
        error_message: The full error output (traceback + message)
        memory_root: Override memory root path
        auto_save: Whether to automatically persist the pitfall

    Returns:
        dict with analysis results and save status
    """
    root = memory_root or get_memory_root()

    # Step 1: Parse
    error_info = parse_error(error_message)

    # Step 2: Check existing pitfalls
    existing = search_existing_pitfalls(error_info, root)

    # Step 3: Generate entry
    pitfall_entry = generate_pitfall_entry(error_info, error_message)

    result = {
        "error_info": error_info,
        "existing_pitfalls": existing,
        "pitfall_entry": pitfall_entry,
        "is_known": len(existing) > 0,
    }

    # Step 4: Save if new and auto_save is enabled
    if auto_save and not existing:
        try:
            from . import save as save_module
        except ImportError:
            import save as save_module
        tags = ["pitfall", error_info["error_type"].lower()]
        if error_info["module"]:
            tags.append(error_info["module"])

        save_result = save_module.save_to_longterm(
            tags=tags,
            content=pitfall_entry,
            storage_type="file",
            memory_root=root,
        )
        result["save_result"] = save_result
    elif existing:
        result["message"] = f"Similar pitfall already recorded in: {existing[0]['file']}"

    return result


def main():
    parser = argparse.ArgumentParser(description="Reflect_On_Error — analyze and persist error patterns")
    parser.add_argument("error", nargs="?", help="Error message string")
    parser.add_argument("--file", help="Read error from a file instead")
    parser.add_argument("--no-save", action="store_true", help="Don't auto-save the pitfall")
    parser.add_argument("--memory-root", help="Override memory skill root path")
    args = parser.parse_args()

    if args.file:
        error_msg = Path(args.file).read_text(encoding="utf-8")
    elif args.error:
        error_msg = args.error
    else:
        error_msg = sys.stdin.read()

    result = reflect_on_error(
        error_message=error_msg,
        memory_root=Path(args.memory_root) if args.memory_root else None,
        auto_save=not args.no_save,
    )

    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
