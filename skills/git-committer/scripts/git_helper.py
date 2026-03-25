import subprocess
import sys
import os

def run_command(cmd):
    try:
        result = subprocess.run(cmd, capture_output=True, text=True, check=True, encoding='utf-8')
        return result.stdout.strip()
    except subprocess.CalledProcessError as e:
        # Keep errors separate if needed, but for now we return None to let caller handle
        sys.stderr.write(f"Error executing {' '.join(cmd)}: {e.stderr}\n")
        return None
    except UnicodeDecodeError:
        # Fallback for systems with different default encodings
        result = subprocess.run(cmd, capture_output=True, text=False, check=True)
        return result.stdout.decode('utf-8', errors='replace').strip()

def get_staged_diff():
    # 僅獲取已暫存的變更內容
    diff = run_command(["git", "diff", "--cached"])
    if diff is None:
        return "Error: Could not retrieve staged changes."
    if not diff:
        return ""
    return diff

def get_unstaged_diff():
    # 獲取未暫存的變更內容
    diff = run_command(["git", "diff"])
    if diff is None:
        return "Error: Could not retrieve unstaged changes."
    return diff

def get_status():
    # 獲取 git 狀態摘要
    status = run_command(["git", "status", "-s"])
    if status is None:
        return "Error: Could not retrieve git status."
    return status

def get_log():
    # 獲取最近 5 條提交日誌
    log = run_command(["git", "log", "-n", "5", "--oneline"])
    if log is None:
        return "Error: Could not retrieve git log."
    return log

def get_all_diff():
    # 獲取自上次提交以來的所有變更（暫存 + 未暫存）
    diff = run_command(["git", "diff", "HEAD"])
    if diff is None:
        return "Error: Could not retrieve all changes."
    return diff

def execute_commit(message):
    # 執行提交
    return run_command(["git", "commit", "-m", message])

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("--action", choices=["get_diff", "get_unstaged_diff", "get_status", "get_log", "get_all_diff", "commit"])
    parser.add_argument("--message", type=str)
    parser.add_argument("--file", type=str, help="Output the result to a specified file")
    args = parser.parse_args()

    result_text = ""
    if args.action == "get_diff":
        result_text = get_staged_diff()
        if not result_text:
            result_text = "No staged changes found. Please run 'git add' first."
    elif args.action == "get_unstaged_diff":
        result_text = get_unstaged_diff()
    elif args.action == "get_status":
        result_text = get_status()
    elif args.action == "get_log":
        result_text = get_log()
    elif args.action == "get_all_diff":
        result_text = get_all_diff()
    elif args.action == "commit" and args.message:
        result_text = execute_commit(args.message)

    if result_text:
        if args.file:
            try:
                # Ensure the parent directory exists
                os.makedirs(os.path.dirname(os.path.abspath(args.file)), exist_ok=True)
                with open(args.file, "w", encoding="utf-8") as f:
                    f.write(result_text)
                print(f"Results saved to {args.file}")
            except Exception as e:
                print(f"Error saving to file: {e}")
                print(result_text)
        else:
            print(result_text)