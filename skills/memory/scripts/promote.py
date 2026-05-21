"""
Skill Promotion — temp_skills/ → .agents/skills/ pipeline.

Tracks invocations of temporary skills via _registry.json. When a skill reaches
5 successful invocations, it gets promoted to a full skill in .agents/skills/.

Usage:
    python -u scripts/promote.py --register "my-new-skill"
    python -u scripts/promote.py --invoke "my-new-skill"
    python -u scripts/promote.py --check-promotions
    python -u scripts/promote.py --promote "my-new-skill"   # Force promote
"""

import argparse
import json
import shutil
import sys
from datetime import datetime
from pathlib import Path

PROMOTION_THRESHOLD = 5


def get_memory_root() -> Path:
    return Path(__file__).resolve().parent.parent


def get_skills_root(memory_root: Path) -> Path:
    """Get the main .agents/skills/ directory."""
    return memory_root.parent  # memory/ is inside skills/


def load_registry(memory_root: Path) -> dict:
    """Load the temp skills registry."""
    registry_path = memory_root / "temp_skills" / "_registry.json"
    if registry_path.exists():
        return json.loads(registry_path.read_text(encoding="utf-8"))
    return {"version": 1, "skills": {}}


def save_registry(memory_root: Path, registry: dict):
    """Save the temp skills registry."""
    registry_path = memory_root / "temp_skills" / "_registry.json"
    registry_path.write_text(json.dumps(registry, ensure_ascii=False, indent=2), encoding="utf-8")


def register_skill(
    skill_name: str,
    requirement: str = "",
    memory_root: Path | None = None,
) -> dict:
    """Register a new temporary skill in the registry."""
    root = memory_root or get_memory_root()
    registry = load_registry(root)

    if skill_name in registry["skills"]:
        return {
            "action": "already_exists",
            "skill": skill_name,
            "invocations": registry["skills"][skill_name]["invocations"],
        }

    registry["skills"][skill_name] = {
        "invocations": 0,
        "created": datetime.now().isoformat(),
        "last_used": None,
        "source_requirement": requirement,
    }

    save_registry(root, registry)

    return {
        "action": "registered",
        "skill": skill_name,
        "invocations": 0,
        "promotion_threshold": PROMOTION_THRESHOLD,
    }


def record_invocation(skill_name: str, memory_root: Path | None = None) -> dict:
    """Increment the invocation counter for a temp skill."""
    root = memory_root or get_memory_root()
    registry = load_registry(root)

    if skill_name not in registry["skills"]:
        return {"action": "error", "reason": f"Skill '{skill_name}' not in registry"}

    entry = registry["skills"][skill_name]
    entry["invocations"] += 1
    entry["last_used"] = datetime.now().isoformat()

    save_registry(root, registry)

    result = {
        "action": "invocation_recorded",
        "skill": skill_name,
        "invocations": entry["invocations"],
        "promotion_threshold": PROMOTION_THRESHOLD,
        "ready_for_promotion": entry["invocations"] >= PROMOTION_THRESHOLD,
    }

    if result["ready_for_promotion"]:
        result["message"] = (
            f"🎉 '{skill_name}' has reached {PROMOTION_THRESHOLD} invocations! "
            f"Ready for promotion to .agents/skills/."
        )

    return result


def check_promotions(memory_root: Path | None = None) -> dict:
    """Check which skills are ready for promotion."""
    root = memory_root or get_memory_root()
    registry = load_registry(root)

    ready = []
    pending = []

    for name, entry in registry["skills"].items():
        info = {
            "name": name,
            "invocations": entry["invocations"],
            "remaining": max(0, PROMOTION_THRESHOLD - entry["invocations"]),
        }
        if entry["invocations"] >= PROMOTION_THRESHOLD:
            ready.append(info)
        else:
            pending.append(info)

    return {
        "ready_for_promotion": ready,
        "pending": pending,
        "threshold": PROMOTION_THRESHOLD,
    }


def promote_skill(skill_name: str, memory_root: Path | None = None) -> dict:
    """
    Promote a skill from temp_skills/ to .agents/skills/.

    Steps:
    1. Verify skill exists in temp_skills/
    2. Copy to .agents/skills/<skill_name>/
    3. Remove from registry
    4. Update SKILL.md index
    """
    root = memory_root or get_memory_root()
    skills_root = get_skills_root(root)

    temp_skill_path = root / "temp_skills" / f"{skill_name}.md"
    target_dir = skills_root / skill_name

    if not temp_skill_path.exists():
        return {"action": "error", "reason": f"Temp skill file not found: {temp_skill_path}"}

    if target_dir.exists():
        return {"action": "error", "reason": f"Skill directory already exists: {target_dir}"}

    # Create target directory and move file as SKILL.md
    target_dir.mkdir(parents=True, exist_ok=True)
    target_path = target_dir / "SKILL.md"
    shutil.copy2(temp_skill_path, target_path)

    # Remove from registry
    registry = load_registry(root)
    removed_entry = registry["skills"].pop(skill_name, None)
    save_registry(root, registry)

    # Remove temp file
    temp_skill_path.unlink()

    return {
        "action": "promoted",
        "skill": skill_name,
        "from": str(temp_skill_path),
        "to": str(target_path),
        "total_invocations": removed_entry["invocations"] if removed_entry else "unknown",
        "reminder": "Update using-agents/SKILL.md and memory/SKILL.md indexes if needed.",
    }


def main():
    parser = argparse.ArgumentParser(description="Skill Promotion — manage temp skill lifecycle")
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--register", metavar="NAME", help="Register a new temp skill")
    group.add_argument("--invoke", metavar="NAME", help="Record an invocation of a temp skill")
    group.add_argument("--check-promotions", action="store_true", help="List skills ready for promotion")
    group.add_argument("--promote", metavar="NAME", help="Force-promote a skill")
    parser.add_argument("--requirement", default="", help="Source requirement (for --register)")
    parser.add_argument("--memory-root", help="Override memory skill root path")
    args = parser.parse_args()

    root = Path(args.memory_root) if args.memory_root else None

    if args.register:
        result = register_skill(args.register, args.requirement, root)
    elif args.invoke:
        result = record_invocation(args.invoke, root)
    elif args.check_promotions:
        result = check_promotions(root)
    elif args.promote:
        result = promote_skill(args.promote, root)

    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
