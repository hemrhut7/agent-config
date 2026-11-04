# Concurrency Decision Matrix & Isolation Guide

This document provides architectural guidance on selecting the appropriate **Subagent Type**, **Workspace Isolation Mode**, **Model Tier**, and **Conflict Avoidance Strategy** during concurrent subagent dispatch.

---

## 1. Task Archetype Matrix

| Task Characteristics | Typical Examples | Recommended TypeName | Recommended Workspace | Recommended Model | Primary Deliverable |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **Read-Only Code Survey** | Cross-directory symbol trace, architectural analysis, API audit | `research` | `inherit` | `flash` or `flash_lite` | Structured Markdown analysis report |
| **Read-Only Telemetry / Log Audit** | Multi-file log parsing, CSV telemetry statistics, anomaly timestamp isolation | `research` or `self` | `inherit` | `flash` | Metric summary & anomaly index |
| **Deep Algorithmic Derivation** | EKF observation matrix Jacobian derivation, covariance propagation modeling | `self` or `research` | `inherit` | `inherit` or `pro` | Symbolic derivations & numerical verifications |
| **Independent Module Feature / Refactor** | Modifying decoupled modules A and B with disjoint file sets | `self` | `branch` (preferred) or disjoint `inherit` | `inherit` | Code modifications & unit tests |
| **Isolated Unit Test Suite Authoring** | Writing dedicated test cases for distinct modules | `self` | `inherit` | `inherit` | New test modules (e.g., `tests/test_module_a.py`) |
| **Specialized Repetitive Batch Work** | Dedicated batch validators, code generators | Custom (`define_subagent`) | Per requirement | Per requirement | Conforming batch output artifacts |

---

## 2. Workspace Modes In-Depth

`invoke_subagent` supports three workspace modes:

### 1. `inherit` (Inherit Parent Workspace)
- **Mechanism**: The subagent executes directly within the parent's file system and working directory.
- **When to Use**:
  - Read-only research tasks (`research` subagent default).
  - Write tasks where files modified by different subagents are **strictly disjoint** and have zero side effects on the shared build environment.
- **Risks & Enforcements**:
  - Never allow multiple subagents to write to the same file concurrently; this causes race conditions and file clobbering.

### 2. `branch` (Isolated Git Branch)
- **Mechanism**: The platform provisions an isolated Git branch and working directory cloned from the parent workspace.
- **When to Use**:
  - High-impact refactorings, speculative experiments, or broad code changes.
  - Tasks that might touch overlapping or adjacent files and require isolated verification before integration.
- **Lifecycle**:
  - Upon subagent completion, the parent agent reviews the branch diffs, resolves any logical divergences, and integrates or merges changes into the main workspace.

### 3. `share` (Shared Underlying Repository)
- **Mechanism**: Functions similarly to a `git worktree` or Mercurial `hg share`, sharing the underlying object store while maintaining independent branch state.
- **When to Use**:
  - Scenarios requiring branch-level isolation where the repository size is very large and disk duplication is undesirable.

---

## 3. Model Tier Selection Criteria

| Model Tier | Ideal Workload | Strengths | Trade-offs |
| :--- | :--- | :--- | :--- |
| `flash_lite` / `flash` | Text search, log filtering, boilerplate extraction, API signature gathering | Ultra-fast execution, low overhead, scalable across high subagent counts | Reduced complex abstract reasoning |
| `inherit` (Default) | Standard feature implementation, bug fixes, refactoring, unit test authoring | Identical reasoning power to the parent agent; balanced and reliable | Moderate execution latency |
| `pro` | Core algorithmic derivation, subtle concurrency/race-condition triage, high-risk math | Maximum reasoning capability and deep contextual synthesis | Higher latency per turn |

---

## 4. Conflict Prevention Checklist

Before dispatching subagents via `invoke_subagent`, verify every point:

- [ ] **Disjoint File Sets**: Under `Workspace: "inherit"`, ensure the write targets of Subagent A and Subagent B do not intersect ($\text{Files}_A \cap \text{Files}_B = \emptyset$).
- [ ] **Port & Global Locks**: Confirm that subagents will not attempt to bind the same localhost network port or acquire identical file-based locks simultaneously.
- [ ] **Scratch Directory Isolation**: Verify all subagents are instructed to write scratch/mock files exclusively to `.agent_scratchpad/` (or dedicated subdirectories therein), never to `/tmp`.
- [ ] **Build Configuration Invariant**: Ensure every subagent prompt explicitly prohibits unapproved modifications to build configuration files (`CMakeLists.txt`, `Makefile`, etc.).
