# Algorithm Development & Verification Protocol

為確保演算法（如 INS/GNSS 鬆緊耦合、EKF 觀測模型、感測器校準、航向融合等）開發過程中的科學嚴謹度、統計顯著性與系統穩定性，所有開發、最佳化與 Bug 修復工作必須嚴格遵循本規範。

---

## 1. 嚴禁樣本數量過少 (Prohibition of Insufficient Sample Verification)
- **統計代表性要求**：
  - 嚴禁僅憑單一資料集（Single Dataset）、單一段斷訊（Single Outage Window）或單一測試情境宣稱演算法獲得改善或通過驗證。
  - 對於具備多資料集的場景（如 Android 智慧手機車載資料、SBG 道路測試、ILB VTOL 固定翼飛行測試），**驗證時必須評估全量資料集或具代表性的多工況樣本群**（至少涵蓋不同動態工況：靜止、直線高速、急轉彎、長/短遮蔽等），以避免局部過擬合（Overfitting）或掩蓋特定工況下的極端異常（Corner Cases）。
- **極端異常檢驗 (Extreme / Outlier Case Stress Testing)**：
  - 評估指標必須同時包含平均指標（RMSE、Mean Error）與極值指標（Max Error、95th/99th Percentile），嚴禁僅以平均值掩蓋單次斷訊飆升或航向發散等極端狀況。

---

## 2. 嚴禁報喜不報憂 (Comprehensive Analysis: Both Improvements and Regressions)
- **雙向性能揭露 (Full Disclosure of Gains and Degradations)**：
  - 嚴禁只著重分析特定工況下的指標改善，而故意忽略或省略其他資料集、其他斷訊段或相鄰狀態的性能劣化。
  - 當演算法在某些情境改善但在其他情境出現退化時，**必須詳實記錄退化幅度、觸發條件與物理/數學根因**（例如：磁力計在無硬鐵環境下能改善航向，但在強鐵磁畸變區若未完成 2D 中心校準則會產生相位調變誤差）。
- **權衡與適用邊界 (Trade-offs & Operational Boundaries)**：
  - 所有新演算法或參數調整，必須明確界定其「適用工況邊界」與「失效保護機制（Fail-safe）」，確保在不利條件下濾波器具備降級或拒收能力，不致導致全系統發散。

---

## 3. 驗證報告儲存與交付規範 (Documentation & Persistence Standard)
- **專案目錄標準存檔**：
  - 每次重大演算法修改、架構重構或性能評估完成後，**必須將驗證分析結果以 Markdown 格式儲存於專案資料夾下**（例如 `doc/` 或對應的分析目錄，如 `doc/Algorithm_Verification_Report_*.md`）。
- **報告必備內容**：
  1. **測試對象與配置**：評估之演算法版本、狀態維度、感測器啟用設定、參數配置。
  2. **測試資料集清單**：所有參與評估之資料集 ID、時間長度、工況描述。
  3. **量化對比數據表**：包含 Baseline vs. 改善後的各資料集指標（RMSE、Max Error、執行耗時）。
  4. **劣化與異常分析**：若有任何指標劣化，必須逐一列出並說明根因。
  5. **回歸測試狀態**：註明 `pytest` 與既有基準腳本（如 VTOL、SBG、ArduPilot）之無回歸驗證結果。
