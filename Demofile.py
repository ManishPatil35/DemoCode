import os
import time
from datetime import datetime

def get_recent_csv_files(folder_path, minutes=15):
    """
    Get .csv files modified within the last 'minutes' from folder_path.
    """
    now = time.time()
    recent_files = []

    for fname in os.listdir(folder_path):
        if fname.lower().endswith(".csv"):
            full_path = os.path.join(folder_path, fname)
            if os.path.isfile(full_path):
                modified_time = os.path.getmtime(full_path)
                age_minutes = (now - modified_time) / 60
                if age_minutes <= minutes:
                    recent_files.append(full_path)
    return recent_files

def get_renamed_filename(original_filename):
    """
    Return new standardized filename based on the filename pattern.
    """
    today_str = datetime.now().strftime("%d%m%Y")
    fname = original_filename.lower()

    if "bulk" in fname and "bse" in fname:
        return f"bulk_BSE_{today_str}.csv"
    elif "block" in fname and "bse" in fname:
        return f"block_BSE_{today_str}.csv"
    elif fname == "bulk.csv":
        return f"bulk_NSE_{today_str}.csv"
    elif fname == "block.csv":
        return f"block_NSE_{today_str}.csv"
    elif "pit" in fname and ("sebi" in fname or "bse" in fname):
        return f"Insider_BSE_{today_str}.csv"
    elif "pit" in fname and "nse" in fname:
        return f"Insider_NSE_{today_str}.csv"
    else:
        return None  # Unrecognized pattern

def rename_recent_files(folder_path, minutes=15):
    """
    Detect and rename recently downloaded .csv files.
    Returns list of renamed file paths.
    """
    recent_files = get_recent_csv_files(folder_path, minutes)
    renamed_files = []

    if not recent_files:
        print("⚠ No recent .csv files found.")
        return renamed_files

    for full_path in recent_files:
        original_name = os.path.basename(full_path)
        new_name = get_renamed_filename(original_name)

        if new_name:
            new_path = os.path.join(folder_path, new_name)
            if not os.path.exists(new_path):
                os.rename(full_path, new_path)
                renamed_files.append(new_path)
                print(f"✅ Renamed: {original_name} → {new_name}")
            else:
                print(f"⚠ Skipped: {new_name} already exists")
        else:
            print(f"⚠ Skipped: {original_name} (unrecognized naming pattern)")

    return renamed_files
