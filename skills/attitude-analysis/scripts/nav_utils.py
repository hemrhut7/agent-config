import numpy as np

def wrap_180(angle):
    """
    Normalize angles to the range [-180, 180] degrees.
    Works for both scalar and numpy arrays.
    """
    return (angle + 180) % 360 - 180

def filter_angular_outliers(time, error, threshold_deg_per_sec=100.0):
    """
    Remove data points from an angular error series that exhibit physically
    unlikely rates of change, often caused by interpolation artifacts
    or timing misalignments between log streams.
    
    Args:
        time: numpy array of timestamps (seconds)
        error: numpy array of angular errors (degrees)
        threshold_deg_per_sec: max allowed rate of change.
        
    Returns:
        Filtered (time, error) arrays.
    """
    if len(time) < 2:
        return time, error
    
    dt = np.diff(time)
    de = wrap_180(np.diff(error))
    
    # Avoid division by zero
    dt[dt == 0] = 1e-9
    rate = np.abs(de / dt)
    
    mask = np.ones(len(time), dtype=bool)
    outlier_indices = np.where(rate > threshold_deg_per_sec)[0]
    
    # Invalidate both points forming the high-rate segment
    for idx in outlier_indices:
        mask[idx] = False
        mask[idx+1] = False
        
    return time[mask], error[mask]

def calculate_interp_error(t_ref, val_ref, t_comp, val_comp, is_angle=True):
    """
    Interpolate comparison data to reference timestamps and calculate error.
    
    Args:
        t_ref: Reference timestamps
        val_ref: Reference values
        t_comp: Comparison timestamps
        val_comp: Comparison values
        is_angle: If True, error is normalized to [-180, 180]
        
    Returns:
        error: val_ref - val_comp_interpolated
    """
    val_comp_interp = np.interp(t_ref, t_comp, val_comp)
    error = val_ref - val_comp_interp
    if is_angle:
        error = wrap_180(error)
    return error
