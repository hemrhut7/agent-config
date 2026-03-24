# scripts/profiler_tool.py
import timeit
import statistics
import sys

def benchmark(func_label, stmt, setup, iterations=100):
    """
    執行效能測試並回傳統計結果
    """
    try:
        # 執行測試
        timer = timeit.Timer(stmt, setup=setup)
        
        # 熱身跑一次
        timer.timeit(number=1)
        
        # 正式測試
        results = timer.repeat(repeat=5, number=iterations)
        
        # 計算每輪的平均執行時間
        per_iter_times = [t / iterations for t in results]
        
        return {
            "label": func_label,
            "mean": statistics.mean(per_iter_times),
            "median": statistics.median(per_iter_times),
            "stdev": statistics.stdev(per_iter_times) if len(per_iter_times) > 1 else 0
        }
    except Exception as e:
        return {"label": func_label, "error": str(e)}

if __name__ == "__main__":
    # 此處可供執行者根據任務動態傳入代碼段
    print("--- 效能測試執行中 ---")