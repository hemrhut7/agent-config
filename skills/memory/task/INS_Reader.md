# Active Tasks — INS_Reader

- [ ] 優化 `runner.py` 高頻迴圈：實作 GNSS Outages 與 Sensor Flags 的向量化預計算，消除迴圈內物件建立與 redundant check。
- [ ] 重構 `ins_gnss_kf.py` 記憶體管理：減少不必要的 `.copy()` 呼叫，並透過物件重用（In-place update）減輕 GC 壓力。
- [ ] 提升時間同步效率：使用 `numpy.searchsorted` 取代 `while` 狀態機進行 $O(\log n)$ 的 GNSS Epoch 映射。
- [ ] 實作 CuPy GPU 加速研究：針對 Batch Optimizer 實作可切換的 CuPy 後端，設計當資料量達到門檻（如 N > 20,000）時自動啟用，並量化評估其加速倍率與數據傳輸開銷。
- [ ] 將 Batch Optimizer 與 EKF 的參數統一進行管理，確保兩方參數的一致性，但需要先進行研究，確認兩者參數的定義、對模型影響是相同的。
