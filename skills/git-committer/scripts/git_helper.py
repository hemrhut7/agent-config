import subprocess
import sys

def run_command(cmd):
    try:
        result = subprocess.run(cmd, capture_output=True, text=True, check=True, encoding='utf-8')
        return result.stdout.strip()
    except subprocess.CalledProcessError as e:
        print(f"Error: {e.stderr}")
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
        return "No staged changes found. Please run 'git add' first."
    return diff

def execute_commit(message):
    # 執行提交
    return run_command(["git", "commit", "-m", message])

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("--action", choices=["get_diff", "commit"])
    parser.add_argument("--message", type=str)
    args = parser.parse_args()

    if args.action == "get_diff":
        print(get_staged_diff())
    elif args.action == "commit" and args.message:
        print(execute_commit(args.message))