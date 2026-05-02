---
name: performance-benchmarking
description: Verify computational performance differences between multiple code implementations. Includes automated test design, statistical data collection, and performance bottleneck analysis. Use when optimizing algorithms, comparing different libraries, or evaluating system scalability.
---

# Performance Benchmarking Skill

This skill is responsible for conducting scientific performance comparisons between different code implementations.

## Core Process

### Step 1: Experimental Design
Before starting the test, you must define:
- **Test Subjects**: Clearly mark Solution A and Solution B.
- **Input Scale**: Define the size of the test data (e.g., n=10, 1000, 1000000).
- **Iteration Count**: Defaults to 100 times to reduce random environmental interference.
**If undefined, you need to confirm with the user.**

### Step 2: Execution
Use `scripts/profiler_tool.py` or the built-in `timeit` module.
- **Warm-up**: Run once before formal timing to eliminate cache effects.
- **Baseline Measurement**: Collect execution time and memory usage.

### Step 3: Conclusion
The conclusion must include the following structure:
1. **Data Statistics**: Mean, Median, and Standard Deviation.
2. **Winner Tagging**: Clearly indicate the solution that performed better at that test scale.
3. **Analysis Advice**: Explain why A is faster than B (e.g., time complexity, memory access, language characteristics).

## Writing Specifications
- **Avoid Single Measurements**: It is strictly forbidden to draw conclusions after running only once.
- **Control Variables**: Ensure all solutions run under exactly the same inputs and environment.
- **Path Specifications**: Script calls must always use `scripts/profiler_tool.py`.