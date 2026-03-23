---
name: symbolic-math-engine
description: 使用 math_engine.py 執行精確數學運算。支援符號簡化、偏微分、Jacobian 矩陣、線性代數（含反對稱矩陣生成）。在需要處理導航誤差模型（如 EKF 觀測矩陣）或複雜物理公式推導時使用，嚴禁口頭推理。
---

# 數學運算與符號推導引擎

## 執行工作流
1. **問題定義**：識別數學形式（例如：是純量對向量的微分，還是矩陣相乘）。
2. **符號轉換**：將公式轉為 Python/SymPy 格式。
   - $u/v$ -> `u/v`
   - $C_l^b$ (Rotation Matrix) -> 定義為 `sp.MatrixSymbol('Clb', 3, 3)` 或具體數值陣列。
3. **執行運算腳本**：調用 `scripts/math_engine.py`。
4. **結果呈現**：使用 LaTeX 格式向用戶展示精確結果，並附加推理邏輯。

## 運算能力指南

### A. Jacobian 矩陣 (向量微積分)
用於推導觀測函數 $h(x)$ 對狀態向量 $x$ 的偏導。
- **命令**：`{"task": "derive", "expr": "函数表達式", "vars": ["變數1", "變數2", ...]} `
- **範例**：求 $h = u/v$ 對 $\hat{v}_{air}^b = [u, v, w]^T$ 的 Jacobian。
  ```bash
  python scripts/math_engine.py '{"task": "derive", "expr": "u/v", "vars": ["u", "v", "w"]}'

### B. 反對稱矩陣 (Skew-symmetric)
用於交叉乘積的符號運算，常見於姿態誤差模型 $[v \times]$。
- **命令**：`{"task": "matrix", "a": [[v1], [v2], [v3]], "op": "skew"} `

## 進階應用範例：EKF 側滑角觀測矩陣 $H$ 推導
用戶提供了觀測函數 $h(x) = u/v$，需要推導 $H = \frac{\partial h}{\partial \delta x}$。

- 步驟 A: 計算 $J_v = \frac{\partial h}{\partial \hat{v}_{air}^b}$
   - Agent 執行命令：
      ```
      python scripts/math_engine.py '{"task": "derive", "expr": "u/v", "vars": ["u", "v", "w"]}'
      ```
   - 腳本輸出結果 ($J_v$)：$$ \begin{bmatrix} \frac{1}{v} & -\frac{u}{v^2} & 0 \end{bmatrix} $$

- 步驟 B: 定義誤差項 (由使用者提供邏輯，Agent 記錄)
記錄誤差關係：$\delta v_{air}^b = C_l^b \delta v^l + C_l^b [v_{air}^l \times] \delta \psi$。

- 步驟 C: 組合 H 矩陣 (矩陣乘法符號運算)
Agent 將利用步驟 A 的結果 $J_v$ 與使用者定義的 $C_l^b$ 行列式進行符號相乘 ($J_v \cdot C_l^b$) 以形成完整的 $H$ 矩陣報告。注意事項優先級：當用戶提及「推導」、「Jacobian」、「偏微分」時，必須使用此技能。依賴：執行環境需預裝 sympy, numpy。