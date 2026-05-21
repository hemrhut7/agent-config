"""
Unit tests for the memory skill scripts.

Tests cover:
  - recall.py: file scanning, topic matching, fallback paths
  - save.py: file routing, auto type detection, append behavior
  - daily_summarize.py: time gate, knowledge extraction, archive flow
  - promote.py: registration, invocation counting, promotion
  - compress.py: limit checking, compression, archiving
"""

import json
import os
import shutil
import tempfile
import time
from datetime import datetime
from pathlib import Path

import pytest

# Add parent to path for imports
import sys
sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "scripts"))


@pytest.fixture
def memory_root(tmp_path):
    """Create a temporary memory directory structure for testing."""
    root = tmp_path / "memory"
    root.mkdir()

    # Create sub-directories
    (root / "user").mkdir()
    (root / "topics").mkdir()
    (root / "temp_skills").mkdir()
    (root / "archive").mkdir()
    (root / "scripts").mkdir()

    # Create SKILL.md
    (root / "SKILL.md").write_text(
        "<!-- SCOPE: Master index for memory skill. -->\n# Memory\nTest content\n",
        encoding="utf-8",
    )

    # Create brain.md
    (root / "brain.md").write_text(
        "<!-- SCOPE: Today's task log. Read at conversation start. -->\n"
        "# Brain — Working Memory\n\n"
        "## Last Updated: 2026-05-14 10:00\n\n"
        "### Active Tasks\n"
        "- [ ] Test EKF convergence\n\n"
        "### Session Notes\n"
        "- Key finding: The EKF altitude filter needs a 3-second warm-up\n"
        "- Learned: pymavlink requires python3.9+ for type hints\n"
        "- Short note\n\n"
        "### Pending Decisions\n"
        "- (none)\n",
        encoding="utf-8",
    )

    # Create user/preferences.md
    (root / "user" / "preferences.md").write_text(
        "<!-- SCOPE: User communication and work habits. -->\n"
        "# User Preferences\n\n"
        "## Communication\n"
        "- Prefers English commit messages\n",
        encoding="utf-8",
    )

    # Create a topic file
    (root / "topics" / "topic-ekf.md").write_text(
        "<!-- SCOPE: Knowledge about EKF tuning and filter optimization. -->\n"
        "# EKF Tuning\n\n"
        "### [2026-05-10] Tags: ekf, tuning\n"
        "The process noise Q matrix needs careful tuning per sensor.\n",
        encoding="utf-8",
    )

    # Create registry
    (root / "temp_skills" / "_registry.json").write_text(
        json.dumps({"version": 1, "skills": {}}),
        encoding="utf-8",
    )

    return root


# ============================================================
# Tests for recall.py
# ============================================================

class TestRecall:
    def test_scan_first_lines(self, memory_root):
        from recall import scan_first_lines
        entries = scan_first_lines(memory_root)
        assert len(entries) > 0
        # All entries should have scope lines
        for e in entries:
            assert "scope" in e
            assert "path" in e

    def test_match_topic_found(self, memory_root):
        from recall import scan_first_lines, match_topic
        entries = scan_first_lines(memory_root)
        matches = match_topic("EKF tuning", entries)
        assert len(matches) > 0
        assert matches[0]["score"] > 0

    def test_match_topic_not_found(self, memory_root):
        from recall import scan_first_lines, match_topic
        entries = scan_first_lines(memory_root)
        matches = match_topic("blockchain cryptocurrency", entries)
        assert len(matches) == 0

    def test_recall_background_file_match(self, memory_root):
        from recall import recall_background
        result = recall_background("EKF tuning", memory_root)
        assert result["source"] == "file"
        assert "ekf" in result["path"].lower()
        assert result["content"]  # Should have content

    def test_recall_background_no_file_match(self, memory_root):
        from recall import recall_background
        result = recall_background("quantum computing", memory_root)
        # No file match expected; may fall back to vectordb if available
        assert result["source"] in ("none", "vectordb")

    def test_archive_excluded_from_scan(self, memory_root):
        """Archive files should not appear in fast scan results."""
        # Create an archive file
        (memory_root / "archive" / "old.md").write_text(
            "<!-- SCOPE: Old EKF knowledge -->\n# Archived\n",
            encoding="utf-8",
        )
        from recall import scan_first_lines
        entries = scan_first_lines(memory_root)
        paths = [e["path"] for e in entries]
        assert not any("archive" in p for p in paths)


# ============================================================
# Tests for save.py
# ============================================================

class TestSave:
    def test_determine_target_file_topic(self, memory_root):
        from save import determine_target_file
        target = determine_target_file(["ekf", "tuning"], memory_root)
        assert "topics" in str(target)
        assert "topic-ekf" in str(target)

    def test_determine_target_file_user(self, memory_root):
        from save import determine_target_file
        target = determine_target_file(["preference", "language"], memory_root)
        assert "user" in str(target)
        assert "preferences" in str(target)

    def test_save_to_file(self, memory_root):
        from save import save_to_longterm
        result = save_to_longterm(
            tags=["gnss", "denied"],
            content="GNSS denied mode triggers after 5 seconds without fix.",
            storage_type="file",
            memory_root=memory_root,
        )
        assert result["action"] == "appended"
        # Check file was created
        topic_file = memory_root / "topics" / "topic-gnss.md"
        assert topic_file.exists()
        content = topic_file.read_text(encoding="utf-8")
        assert "GNSS denied mode" in content

    def test_save_append_existing(self, memory_root):
        from save import save_to_longterm
        # Save twice to same topic
        save_to_longterm(tags=["ekf"], content="First entry", storage_type="file", memory_root=memory_root)
        save_to_longterm(tags=["ekf"], content="Second entry", storage_type="file", memory_root=memory_root)

        topic_file = memory_root / "topics" / "topic-ekf.md"
        content = topic_file.read_text(encoding="utf-8")
        assert "First entry" in content
        assert "Second entry" in content

    def test_auto_type_short(self, memory_root):
        from save import auto_determine_type
        assert auto_determine_type("Short fact.") == "file"

    def test_auto_type_structured(self, memory_root):
        from save import auto_determine_type
        content = "\n".join([f"- Point {i}" for i in range(20)])
        assert auto_determine_type(content) == "file"

    def test_auto_type_long_narrative(self, memory_root):
        from save import auto_determine_type
        content = "\n".join([f"This is a long paragraph about topic {i}." for i in range(20)])
        assert auto_determine_type(content) == "vector"

    def test_sanitize_filename(self, memory_root):
        from save import sanitize_filename
        assert sanitize_filename("EKF Tuning!") == "ekf-tuning"
        assert sanitize_filename("  hello  ") == "hello"
        assert sanitize_filename("a/b/c") == "a-b-c"


# ============================================================
# Tests for daily_summarize.py
# ============================================================

class TestDailySummarize:
    def test_extract_knowledge(self, memory_root):
        from daily_summarize import extract_knowledge
        brain_content = (memory_root / "brain.md").read_text(encoding="utf-8")
        knowledge = extract_knowledge(brain_content)
        # Should extract "Key finding" and "Learned" entries
        assert len(knowledge) >= 2
        types = [k["type"] for k in knowledge]
        assert "key finding" in types
        assert "learned" in types

    def test_time_gate_not_due(self, memory_root):
        from daily_summarize import check_time_gate
        brain_path = memory_root / "brain.md"
        # Touch the file to make it recent
        brain_path.write_text(brain_path.read_text(encoding="utf-8"), encoding="utf-8")
        result = check_time_gate(brain_path)
        assert result["due"] is False

    def test_time_gate_due(self, memory_root):
        from daily_summarize import check_time_gate
        brain_path = memory_root / "brain.md"
        # Set mtime to 10 hours ago
        old_time = time.time() - (10 * 3600)
        os.utime(brain_path, (old_time, old_time))
        result = check_time_gate(brain_path)
        assert result["due"] is True

    def test_daily_summarize_skip_recent(self, memory_root):
        from daily_summarize import daily_summarize
        # brain.md is recent, should skip
        result = daily_summarize(memory_root=memory_root, force=False)
        assert result["action"] == "skipped"

    def test_daily_summarize_force(self, memory_root):
        from daily_summarize import daily_summarize
        result = daily_summarize(memory_root=memory_root, force=True)
        assert result["action"] == "completed"
        assert result["knowledge_extracted"] >= 2
        assert result["brain_reset"] is True
        # Check archive was created
        archive_files = list((memory_root / "archive").glob("brain_*.md"))
        assert len(archive_files) >= 1
        # Check brain was reset
        brain_content = (memory_root / "brain.md").read_text(encoding="utf-8")
        assert "Active Tasks" in brain_content
        assert "(none yet)" in brain_content or "(fresh session)" in brain_content


# ============================================================
# Tests for promote.py
# ============================================================

class TestPromote:
    def test_register_skill(self, memory_root):
        from promote import register_skill
        result = register_skill("test-skill", "Testing purpose", memory_root)
        assert result["action"] == "registered"
        assert result["invocations"] == 0

    def test_register_duplicate(self, memory_root):
        from promote import register_skill
        register_skill("test-skill", "", memory_root)
        result = register_skill("test-skill", "", memory_root)
        assert result["action"] == "already_exists"

    def test_record_invocation(self, memory_root):
        from promote import register_skill, record_invocation
        register_skill("test-skill", "", memory_root)
        result = record_invocation("test-skill", memory_root)
        assert result["action"] == "invocation_recorded"
        assert result["invocations"] == 1
        assert result["ready_for_promotion"] is False

    def test_promotion_threshold(self, memory_root):
        from promote import register_skill, record_invocation
        register_skill("test-skill", "", memory_root)
        for i in range(5):
            result = record_invocation("test-skill", memory_root)
        assert result["ready_for_promotion"] is True
        assert result["invocations"] == 5

    def test_check_promotions(self, memory_root):
        from promote import register_skill, record_invocation, check_promotions
        register_skill("ready-skill", "", memory_root)
        for _ in range(5):
            record_invocation("ready-skill", memory_root)
        register_skill("pending-skill", "", memory_root)
        record_invocation("pending-skill", memory_root)

        result = check_promotions(memory_root)
        assert len(result["ready_for_promotion"]) == 1
        assert len(result["pending"]) == 1
        assert result["ready_for_promotion"][0]["name"] == "ready-skill"

    def test_promote_skill(self, memory_root):
        from promote import register_skill, promote_skill
        # Create a temp skill file
        skill_content = "---\nname: test-skill\n---\n# Test Skill\nDoes testing.\n"
        (memory_root / "temp_skills" / "test-skill.md").write_text(skill_content, encoding="utf-8")
        register_skill("test-skill", "", memory_root)

        # We need to set up the parent skills/ directory structure
        # promote.py expects memory_root.parent to be skills/
        # In our test, memory_root IS the skills dir effectively
        result = promote_skill("test-skill", memory_root)
        assert result["action"] == "promoted"


# ============================================================
# Tests for compress.py
# ============================================================

class TestCompress:
    def test_check_within_limit(self, memory_root):
        from compress import check_file
        result = check_file(memory_root / "SKILL.md", memory_root)
        assert result["status"] == "ok"

    def test_check_over_limit(self, memory_root):
        from compress import check_file
        # Create a topics file with >100 lines
        big_content = "<!-- SCOPE: Big topic -->\n" + "\n".join([f"Line {i}" for i in range(120)])
        (memory_root / "topics" / "topic-big.md").write_text(big_content, encoding="utf-8")
        result = check_file(memory_root / "topics" / "topic-big.md", memory_root)
        assert result["status"] == "over_limit"
        assert result["over"] > 0

    def test_check_all(self, memory_root):
        from compress import check_all
        results = check_all(memory_root)
        assert len(results) > 0
        # All existing files should be within limits
        for r in results:
            assert r["status"] == "ok", f"{r['path']} is over limit"

    def test_compress_file(self, memory_root):
        from compress import compress_file
        # Create oversized file
        big_content = "<!-- SCOPE: Big topic -->\n" + "\n".join([f"Line {i}" for i in range(120)])
        big_path = memory_root / "topics" / "topic-big.md"
        big_path.write_text(big_content, encoding="utf-8")

        result = compress_file(big_path, memory_root)
        assert result["action"] == "compressed"
        assert result["compressed_lines"] <= 100

        # Check archive was created
        archive_files = list((memory_root / "archive" / "compressed").rglob("*.md"))
        assert len(archive_files) >= 1

    def test_compress_skips_within_limit(self, memory_root):
        from compress import compress_file
        result = compress_file(memory_root / "SKILL.md", memory_root)
        assert result["action"] == "skipped"


# ============================================================
# Tests for vectordb_manager.py (stub behavior)
# ============================================================

class TestVectorDB:
    def test_search_returns_valid_result(self, memory_root):
        from vectordb_manager import search
        result = search("EKF tuning")
        # Whether ChromaDB is installed or not, source should be valid
        assert result["source"] in ("none", "vectordb")

    def test_add_document(self, memory_root):
        from vectordb_manager import add_document
        result = add_document("test content", {"tags": ["test"]})
        # Either stored successfully or reported unavailable
        assert result["status"] in ("stored", "unavailable")

    def test_status(self, memory_root):
        from vectordb_manager import get_status
        status = get_status()
        assert "available" in status or "status" in status


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
