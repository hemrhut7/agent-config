import subprocess
import sys
import os

# Threshold for auto-redirection to prevent terminal hanging
MAX_TERMINAL_OUTPUT = 5000 

def run_command(cmd):
    try:
        result = subprocess.run(cmd, capture_output=True, text=True, check=True, encoding='utf-8')
        return result.stdout.strip()
    except subprocess.CalledProcessError as e:
        sys.stderr.write(f"Error executing {' '.join(cmd)}: {e.stderr}\n")
        return None
    except UnicodeDecodeError:
        result = subprocess.run(cmd, capture_output=True, text=False, check=True)
        return result.stdout.decode('utf-8', errors='replace').strip()

def get_staged_diff():
    diff = run_command(["git", "diff", "--cached"])
    if diff is None: return "Error: Could not retrieve staged changes."
    return diff

def get_unstaged_diff():
    diff = run_command(["git", "diff"])
    if diff is None: return "Error: Could not retrieve unstaged changes."
    return diff

def get_status():
    status = run_command(["git", "status", "-s"])
    if status is None: return "Error: Could not retrieve git status."
    return status

def get_log():
    log = run_command(["git", "log", "-n", "5", "--oneline"])
    if log is None: return "Error: Could not retrieve git log."
    return log

def get_diff_stat():
    stat = run_command(["git", "diff", "--cached", "--stat"])
    return stat if stat else ""

def check_conflicts():
    conflicts = run_command(["git", "ls-files", "-u"])
    return conflicts if conflicts else None

def check_submodules():
    if os.path.exists(".gitmodules"):
        status = run_command(["git", "submodule", "status"])
        return status
    return None

def analyze_all():
    report = []
    report.append("# Git Analysis Report")
    
    # 1. Conflicts Pre-flight
    conflicts = check_conflicts()
    if conflicts:
        report.append("## ⚠️ WARNING: Unmerged Conflicts Detected")
        report.append("Please resolve these conflicts before committing:\n" + conflicts)
    
    # 2. Status
    status = get_status()
    report.append("## Status Summary")
    report.append(status if status else "No changes detected.")
    
    # 3. Submodules
    submodules = check_submodules()
    if submodules:
        report.append("## Submodule Status")
        report.append(submodules)
    
    # 4. Diff Stat
    stat = get_diff_stat()
    if stat:
        report.append("## Staged Changes Statistics")
        report.append(stat)
    
    # 5. Recent Logs
    log = get_log()
    report.append("## Recent Commits Context")
    report.append(log)
    
    # 6. Full Diff
    diff = get_staged_diff()
    if diff:
        report.append("## Detailed Staged Diff")
        # Use fenced code block for better readability in artifacts
        report.append(f"```diff\n{diff}\n```")
    
    return "\n\n".join(report)

def handle_output(content, output_file=None):
    if not content:
        return
        
    target_file = output_file
    is_auto_redirected = False
    
    # Auto-redirect if content is too large and no file is specified
    if not target_file and len(content) > MAX_TERMINAL_OUTPUT:
        target_file = ".agent_scratchpad/auto_analysis.md"
        is_auto_redirected = True
        
    if target_file:
        try:
            os.makedirs(os.path.dirname(os.path.abspath(target_file)), exist_ok=True)
            with open(target_file, "w", encoding="utf-8") as f:
                f.write(content)
            
            if is_auto_redirected:
                print(f"⚠️ Output is too large ({len(content)} chars). Automatically saved to: {target_file}")
                print("\n--- Summary Preview ---")
                lines = content.split('\n')
                # Show first 30 lines for context
                for line in lines[:30]:
                    print(line)
                if len(lines) > 30:
                    print("\n... (content truncated, please read the file for full details) ...")
            else:
                print(f"Results saved to {target_file}")
        except Exception as e:
            print(f"Error saving to file: {e}")
            # Fallback to truncated stdout
            print(content[:MAX_TERMINAL_OUTPUT] + "\n... (truncated due to error)")
    else:
        print(content)

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("--action", choices=["get_diff", "get_unstaged_diff", "get_status", "get_log", "get_all_diff", "commit", "analyze_all"])
    parser.add_argument("--message", type=str)
    parser.add_argument("--file", type=str, help="Output the result to a specified file")
    args = parser.parse_args()

    result_text = ""
    if args.action == "get_diff":
        result_text = get_staged_diff()
        if not result_text.strip():
            result_text = "No staged changes found. Please run 'git add' first."
    elif args.action == "get_unstaged_diff":
        result_text = get_unstaged_diff()
    elif args.action == "get_status":
        result_text = get_status()
    elif args.action == "get_log":
        result_text = get_log()
    elif args.action == "get_all_diff":
        result_text = run_command(["git", "diff", "HEAD"])
    elif args.action == "analyze_all":
        result_text = analyze_all()
    elif args.action == "commit" and args.message:
        # Check conflicts before commit
        if check_conflicts():
            result_text = "❌ ABORTED: Unmerged conflicts detected. Please resolve them first."
        else:
            result_text = run_command(["git", "commit", "-m", args.message])

    if result_text:
        handle_output(result_text, args.file)