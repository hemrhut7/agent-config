<!-- SCOPE: Knowledge about threading. Read when related tasks arise. -->
# Threading

### [2026-06-25 13:38] Tags: threading, UI, performance
Fixed CPU busy-waiting in SensorReaderLoop.run by introducing a 1ms sleep when no data is available. Optimized Figures.py transfer method by removing all temporary numpy array allocations and list comprehensions to reduce GIL contention and CPU usage.

### [2026-06-25 13:45] Tags: threading, UI, batching, performance
Implemented signal buffering and batching (at 50 Hz / 20 ms) in SensorReaderQthread to prevent cross-thread event loop queue bloat and GIL contention at 2 kHz data rate. Refactored DataDrawer.transfer in Figures.py to process packets in batches, keeping GUI updates backward compatible.

### [2026-06-25 13:49] Tags: threading, batching, collections, performance
Replaced list buffer with collections.deque in SensorReaderQthread to prevent GC overhead. Implemented dynamic triggers for sending batches (100 Hz or when deque length reaches 20) to keep latency low and prevent drops at 2 kHz data rate. Emitted batches as immutable tuples to ensure thread safety.
