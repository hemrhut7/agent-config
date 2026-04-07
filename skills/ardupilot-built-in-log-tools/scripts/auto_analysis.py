#!/usr/bin/env python3
"""
Auto Analysis Unified Runner
Implements high-performance Data Caching and Smart Downsampling to avoid repeated 
log parsing overhead and matplotlib freezing.
"""

import os
import argparse
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from pymavlink import mavutil
from tqdm import tqdm

class LogAnalyzer:
    def __init__(self, log_file, cache_dir=".logcache"):
        self.log_file = log_file
        self.cache_dir = cache_dir
        self.log_id = os.path.basename(log_file).replace('.bin', '').replace('.tlog', '')
        os.makedirs(self.cache_dir, exist_ok=True)
        
    def _get_cache_path(self):
        return os.path.join(self.cache_dir, f"{self.log_id}_cache.pkl")

    def _parse_and_cache(self, required_types=None):
        if required_types is None:
            required_types = {'ILB', 'ILB3', 'ATT', 'POS', 'XKF1'}
            
        print(f"Parsing log {self.log_file} (First time only)...")
        mlog = mavutil.mavlink_connection(self.log_file)
        file_size = os.path.getsize(self.log_file)
        
        data_store = {k: [] for k in required_types}
        
        last_offset = 0
        pbar = tqdm(total=file_size, unit='B', unit_scale=True, desc="Parsing")
        
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
            # Handle ILB and ILB3 equivalence
            if mtype == 'ILB3': mtype = 'ILB'
                
            if mtype in required_types:
                data_store[mtype].append(msg.to_dict())
                
        pbar.close()
        
        # Convert to DataFrames
        dfs = {}
        for mtype, records in data_store.items():
            if records:
                df = pd.DataFrame(records)
                if 'TimeUS' in df.columns:
                    df['TimeS'] = df['TimeUS'] / 1e6
                    df.sort_values('TimeS', inplace=True)
                    dfs[mtype] = df
                    
        cache_path = self._get_cache_path()
        try:
            pd.to_pickle(dfs, cache_path)
            print(f"Cache saved to {cache_path}")
        except Exception as e:
            print(f"Warning: Failed to save cache: {e}")
            
        return dfs

    def get_dataframes(self, required_types=None):
        cache_path = self._get_cache_path()
        if os.path.exists(cache_path):
            print(f"Loading data from cache: {cache_path}")
            dfs = pd.read_pickle(cache_path)
            
            # Check if cache contains all required types
            if required_types:
                missing = [t for t in required_types if t not in dfs and t != 'ILB'] # Relax ILB/ILB3
                if not missing:
                    return dfs
            else:
                return dfs
                
        # Cache miss or forced reload
        return self._parse_and_cache(required_types)


# --- Downsampling Helper ---
def smart_downsample(df, max_points=10000):
    if len(df) <= max_points:
        return df
    step = len(df) // max_points
    return df.iloc[::step].copy()


# --- Plugins ---
def wrap_180(angle_deg):
    return (angle_deg + 180) % 360 - 180

def run_pva_pipeline(analyzer, out_prefix):
    dfs = analyzer.get_dataframes({'ILB', 'ATT', 'POS', 'XKF1'})
    df_ilb = dfs.get('ILB', pd.DataFrame())
    df_att = dfs.get('ATT', pd.DataFrame())
    df_pos = dfs.get('POS', pd.DataFrame())
    df_xkf1 = dfs.get('XKF1', pd.DataFrame())
    
    if df_ilb.empty:
        print("Error: No ILB data found.")
        return

    print("Aligning PVA Data...")
    t0 = df_ilb['TimeS'].min()
    for df in [df_ilb, df_att, df_pos, df_xkf1]:
        if not df.empty:
            df['TimeS'] = df['TimeS'] - t0
            df.drop_duplicates('TimeS', inplace=True)
            
    df_align = df_ilb.copy()
    t_base = df_ilb['TimeS'].values
    
    # Map ILB variables
    if 'Roll' in df_align.columns:
        df_align['Ref_Roll'] = df_align['Roll'].values
        df_align['Ref_Pitch'] = df_align['Pitch'].values
        df_align['Ref_Yaw'] = df_align['Yaw'].values
        df_align['Ref_VN'] = df_align['VN'].values
        df_align['Ref_VE'] = df_align['VE'].values
        df_align['Ref_VD'] = df_align['VD'].values
        df_align['Ref_Lat'] = df_align['Lat'].values
        df_align['Ref_Lng'] = df_align['Lng'].values
        df_align['Ref_Alt'] = df_align['Alt'].values
        
    # Interpolate Test
    if not df_att.empty:
        df_align['Test_Roll'] = np.interp(t_base, df_att['TimeS'].values, df_att['Roll'].values)
        df_align['Test_Pitch'] = np.interp(t_base, df_att['TimeS'].values, df_att['Pitch'].values)
        yaw_unwrapped = np.unwrap(np.radians(df_att['Yaw'].values))
        interpolated_yaw = np.interp(t_base, df_att['TimeS'].values, yaw_unwrapped)
        df_align['Test_Yaw'] = wrap_180(np.degrees(interpolated_yaw))

    if not df_pos.empty:
        df_align['Test_Lat'] = np.interp(t_base, df_pos['TimeS'].values, df_pos['Lat'].values)
        df_align['Test_Lng'] = np.interp(t_base, df_pos['TimeS'].values, df_pos['Lng'].values)
        df_align['Test_Alt'] = np.interp(t_base, df_pos['TimeS'].values, df_pos['Alt'].values)
        
    if not df_xkf1.empty:
        # Filter Core 0
        df_xkf1 = df_xkf1[df_xkf1.get('C', 0) == 0]
        if not df_xkf1.empty:
            df_align['Test_VN'] = np.interp(t_base, df_xkf1['TimeS'].values, df_xkf1['VN'].values)
            df_align['Test_VE'] = np.interp(t_base, df_xkf1['TimeS'].values, df_xkf1['VE'].values)
            df_align['Test_VD'] = np.interp(t_base, df_xkf1['TimeS'].values, df_xkf1['VD'].values)

    # Calculate Errors
    err_df = df_align[['TimeS', 'TimeUS']].copy()
    
    if 'Test_Roll' in df_align.columns:
        err_df['Err_Roll'] = wrap_180(df_align['Test_Roll'] - df_align['Ref_Roll'])
        err_df['Err_Pitch'] = wrap_180(df_align['Test_Pitch'] - df_align['Ref_Pitch'])
        err_df['Err_Yaw'] = wrap_180(df_align['Test_Yaw'] - df_align['Ref_Yaw'])
        
    if 'Test_VN' in df_align.columns:
        err_df['Err_VN'] = df_align['Test_VN'] - df_align['Ref_VN']
        err_df['Err_VE'] = df_align['Test_VE'] - df_align['Ref_VE']
        err_df['Err_VD'] = df_align['Test_VD'] - df_align['Ref_VD']
        
    if 'Test_Lat' in df_align.columns:
        mean_lat = df_align['Ref_Lat'].mean()
        lat_scale = 111319.5
        lng_scale = 111319.5 * np.cos(np.radians(mean_lat))
        err_df['Err_Lat'] = (df_align['Test_Lat'] - df_align['Ref_Lat']) * lat_scale
        err_df['Err_Lng'] = (df_align['Test_Lng'] - df_align['Ref_Lng']) * lng_scale
        err_df['Err_Alt'] = df_align['Test_Alt'] - df_align['Ref_Alt']
        
    # Generate Stats
    error_cols = [c for c in err_df.columns if c.startswith('Err_')]
    stats = []
    
    # Segment detection based on TimeS gaps > 10s
    time_diff = err_df['TimeS'].diff()
    new_segments = (time_diff > 10.0) | (time_diff < 0)
    err_df['Segment'] = new_segments.cumsum()
    
    for seg in err_df['Segment'].dropna().unique():
        seg_data = err_df[err_df['Segment'] == seg]
        for col in error_cols:
            vals = seg_data[col].dropna()
            if len(vals) < 10: continue
            stats.append({
                'Segment': seg, 'Field': col.replace('Err_', ''),
                'Mean': f"{vals.mean():.4f}", 'Std': f"{vals.std():.4f}",
                'RMSE': f"{np.sqrt((vals**2).mean()):.4f}", 'MaxAbs': f"{vals.abs().max():.4f}"
            })
            
    if stats:
        md_file = f"{out_prefix}_report.md"
        pd.DataFrame(stats).to_markdown(md_file, index=False)
        print(f"Stats saved to {md_file}")

    # Smart Downsampled Plot
    plot_file = f"{out_prefix}_trend.png"
    print(f"Rendering trend plot to {plot_file} (Downsampled for speed)...")
    plot_df = smart_downsample(err_df, max_points=5000)
    
    fig, axes = plt.subplots(3, 1, figsize=(15, 12), sharex=True)
    
    for idx, (groups, title, ylabel) in enumerate([
        (['Err_Roll', 'Err_Pitch', 'Err_Yaw'], "Attitude Errors", "deg"),
        (['Err_VN', 'Err_VE', 'Err_VD'], "Velocity Errors", "m/s"),
        (['Err_Lat', 'Err_Lng', 'Err_Alt'], "Position Errors", "meters")
    ]):
        ax = axes[idx]
        for col, color in zip(groups, ['r', 'g', 'b']):
            if col in plot_df.columns:
                ax.plot(plot_df['TimeS'].values, plot_df[col].values, label=col, color=color, alpha=0.7)
        ax.set_ylabel(ylabel)
        ax.legend(loc='upper right')
        ax.grid(True)
        ax.set_title(title)
        
    axes[2].set_xlabel("Time (s)")
    plt.tight_layout()
    plt.savefig(plot_file)
    print(f"Plot saved to {plot_file}")


def main():
    parser = argparse.ArgumentParser(description="Auto Analysis Unified Runner")
    parser.add_argument("log", help="Path to .bin log file")
    parser.add_argument("--task", choices=['pva'], default='pva', help="Analysis task to run")
    parser.add_argument("--out", default="output/pva_analysis", help="Output prefix")
    args = parser.parse_args()
    
    analyzer = LogAnalyzer(args.log)
    
    if args.task == 'pva':
        os.makedirs(os.path.dirname(args.out) or '.', exist_ok=True)
        run_pva_pipeline(analyzer, args.out)

if __name__ == "__main__":
    main()
