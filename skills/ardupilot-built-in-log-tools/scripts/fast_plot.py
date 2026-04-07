#!/usr/bin/env python3
"""
Fast Plotter for ArduPilot Logs
A high-performance alternative to mavgraph.py using single-pass parsing and Pandas.
Usage: fast_plot.py <log> "MSG1.Field1" "MSG2.Field2" --output out.png
"""

import os
import argparse
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from pymavlink import mavutil
from tqdm import tqdm
from collections import defaultdict

def parse_args():
    parser = argparse.ArgumentParser(description="Fast ArduPilot Log Plotter")
    parser.add_argument("log", help="Path to .bin log file")
    parser.add_argument("fields", nargs="+", help="Fields to plot, format: MSG.Field (e.g. ATT.Roll)")
    parser.add_argument("--output", "-o", default="plot.png", help="Output PNG file")
    parser.add_argument("--title", "-t", help="Plot title")
    parser.add_argument("--condition", "-c", help="Condition for filtering (not fully implemented in fast mode)")
    return parser.parse_args()

def main():
    args = parse_args()
    
    # Extract message types and fields
    targets = defaultdict(set)
    requested_fields = []
    for f in args.fields:
        if '.' not in f:
            print(f"Invalid field format: {f}. Use MSG.Field")
            continue
        mtype, mfield = f.split('.', 1)
        targets[mtype].add(mfield)
        requested_fields.append((mtype, mfield))

    # Add TimeUS to all targets
    for mtype in targets:
        targets[mtype].add('TimeUS')

    print(f"Opening log: {args.log}")
    mlog = mavutil.mavlink_connection(args.log)
    file_size = os.path.getsize(args.log)
    pbar = tqdm(total=file_size, unit='B', unit_scale=True, desc="Parsing")
    
    msgs_data = defaultdict(list)
    last_offset = 0
    
    while True:
        msg = mlog.recv_msg()
        if msg is None:
            break
            
        try:
            curr_offset = mlog.offset
        except:
            curr_offset = last_offset
            
        pbar.update(curr_offset - last_offset)
        last_offset = curr_offset
        
        mtype = msg.get_type()
        if mtype in targets:
            m_dict = msg.to_dict()
            # Only keep requested fields to save memory
            filtered_dict = {k: v for k, v in m_dict.items() if k in targets[mtype]}
            msgs_data[mtype].append(filtered_dict)
            
    pbar.close()
    
    if not msgs_data:
        print("No requested data found in log.")
        return

    # Convert to DataFrames
    dfs = {}
    for mtype, data in msgs_data.items():
        df = pd.DataFrame(data)
        if 'TimeUS' in df.columns:
            df['TimeS'] = df['TimeUS'] / 1e6
            df.sort_values('TimeS', inplace=True)
            df.drop_duplicates('TimeS', inplace=True)
            dfs[mtype] = df

    # Plotting
    plt.figure(figsize=(12, 6))
    
    # Use the first valid message type as the master time base
    master_time_base = None
    for mtype, field in requested_fields:
        if mtype in dfs and not dfs[mtype].empty:
            master_time_base = dfs[mtype]['TimeS'].values
            break

    if master_time_base is None:
        print("No valid time data found.")
        return
    
    for mtype, field in requested_fields:
        if mtype not in dfs or field not in dfs[mtype].columns:
            continue
            
        df = dfs[mtype].copy()
        
        # Gap Detection: Insert NaNs if TimeS delta > 1s
        dt = df['TimeS'].diff()
        gap_indices = df.index[dt > 1.0].tolist()
        if gap_indices:
            nan_rows = []
            for idx in gap_indices:
                nan_row = df.loc[idx].copy()
                nan_row['TimeS'] = df.loc[idx, 'TimeS'] - 0.001
                nan_row[field] = np.nan
                nan_rows.append(nan_row)
            df = pd.concat([df, pd.DataFrame(nan_rows)]).sort_values('TimeS').reset_index(drop=True)

        # Plotting - convert to numpy to avoid pandas/matplotlib indexing errors
        plt.plot(df['TimeS'].values, df[field].values, label=f"{mtype}.{field}", alpha=0.8)

    plt.xlabel("Time (s)")
    plt.ylabel("Value")
    plt.title(args.title or f"Fast Plot: {args.log}")
    plt.legend()
    plt.grid(True, alpha=0.3)
    plt.tight_layout()
    plt.savefig(args.output)
    print(f"Plot saved to {args.output}")

if __name__ == "__main__":
    main()
