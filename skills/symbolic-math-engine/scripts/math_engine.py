import sympy as sp
import numpy as np
import json
import sys

class MathEngine:
    """高級符號與數值運算引擎，支援導航誤差模型推導"""
    
    @staticmethod
    def derive(expression, variables, order=1):
        """
        執行微分或雅可比矩陣(Jacobian)。
        variables: str (單個變數) 或 list of str (向量變數，用於 Jacobian)
        """
        try:
            expr = sp.sympify(expression)
            
            # 處理雅可比矩陣 (步驟 A: scalar complex function w.r.t vector)
            if isinstance(variables, list):
                vars_vec = sp.Matrix([sp.Symbol(v) for v in variables])
                # SymPy 的 jacobian 需要 function 也是 Matrix 形式
                res = sp.Matrix([expr]).jacobian(vars_vec)
            else:
                # 單變數微分
                var = sp.Symbol(variables)
                res = sp.diff(expr, var, order)
                
            return {"latex": sp.latex(res), "pretty": str(res), "type": str(type(res))}
        except Exception as e:
            return {"error": f"微分失敗: {str(e)}"}

    @staticmethod
    def matrix_ops(matrix_a, matrix_b=None, op="det"):
        """線性代數運算，支援反對稱矩陣生成"""
        try:
            # 處理特殊操作：生成反對稱矩陣 (Skew-symmetric,用於步驟 C)
            if op == "skew":
                v = sp.Matrix(matrix_a)
                if v.shape != (3, 1) and v.shape != (1, 3):
                    return {"error": "Skew操作僅支援 3x1 或 1x3 向量"}
                res = sp.Matrix([[0, -v[2], v[1]],
                                   [v[2], 0, -v[0]],
                                   [-v[1], v[0], 0]])
                return {"latex": sp.latex(res), "result": str(res)}

            # 標準矩陣操作
            ma = sp.Matrix(matrix_a)
            if op == "det":
                res = ma.det()
            elif op == "inv":
                res = ma.inv()
            elif op == "eigen":
                res = ma.eigenvals()
            elif op == "multiply" and matrix_b:
                mb = sp.Matrix(matrix_b)
                res = ma * mb
            else:
                return {"error": "未知的矩陣操作或缺少 Matrix B"}
            
            return {"latex": sp.latex(res), "result": str(res), "type": str(type(res))}
        except Exception as e:
            return {"error": f"矩陣運算失敗: {str(e)}"}

if __name__ == "__main__":
    # CLI 介面增強，解析 variables 列表
    try:
        input_data = json.loads(sys.argv[1])
        engine = MathEngine()
        task = input_data.get('task')

        if task == 'derive':
            # 支援單個字串或字串列表
            print(json.dumps(engine.derive(input_data['expr'], input_data['vars'])))
        elif task == 'matrix':
            print(json.dumps(engine.matrix_ops(input_data.get('a'), input_data.get('b'), input_data['op'])))
        else:
            print(json.dumps({"error": "未知的任務類型"}))
            
    except Exception as e:
        print(json.dumps({"error": f"輸入解析或執行錯誤: {str(e)}"}))