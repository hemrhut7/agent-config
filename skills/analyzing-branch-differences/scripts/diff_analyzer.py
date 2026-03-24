import subprocess
import argparse

def get_branch_diff(base, head):
    """獲取兩個分支間的檔案差異與統計。"""
    try:
        # 獲取變更檔案清單與統計
        summary = subprocess.run(
            ["git", "diff", f"{base}...{head}", "--stat"], 
            capture_output=True, text=True, check=True
        ).stdout
        
        # 獲取具體變更內容（限制大小以防 Token 溢出）
        patch = subprocess.run(
            ["git", "diff", f"{base}...{head}", "--patch-with-stat"], 
            capture_output=True, text=True, check=True
        ).stdout
        
        return f"--- Summary ---\n{summary}\n\n--- Detailed Patch ---\n{patch[:5000]}..."
    except Exception as e:
        return f"Error analyzing diff: {str(e)}"

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--base", required=True, help="Base branch")
    parser.add_argument("--head", required=True, help="Head branch to compare")
    args = parser.parse_args()
    print(get_branch_diff(args.base, args.head))