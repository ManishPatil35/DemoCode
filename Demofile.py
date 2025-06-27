import os
import time
import re
from datetime import datetime

def get_recent_csv_files(folder_path, minutes=15):
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

def extract_date_from_filename(fname):
    # Format 25Jun2025
    match = re.search(r'(\d{2}[A-Za-z]{3}\d{4})', fname)
    if match:
        try:
            dt = datetime.strptime(match.group(1), '%d%b%Y')
            return dt.strftime('%d%m%Y')
        except:
            pass

    # Format 250625
    match = re.search(r'(\d{2})(\d{2})(\d{2})', fname)
    if match:
        try:
            dt = datetime.strptime(match.group(0), '%d%m%y')
            return dt.strftime('%d%m%Y')
        except:
            pass

    return datetime.now().strftime('%d%m%Y')  # fallback to today

def get_renamed_filename(original_filename):
    fname = original_filename.lower()
    date_part = extract_date_from_filename(original_filename)

    # Infer file type
    if 'bulk' in fname:
        file_type = 'bulk'
    elif 'block' in fname:
        file_type = 'block'
    elif 'pit' in fname or 'insider' in fname:
        file_type = 'Insider'
    else:
        return None

    # Infer source
    if 'bse' in fname or '_' in original_filename:  # Bulk_25Jun2025 → BSE
        source = 'BSE'
    elif original_filename.lower() in ['bulk.csv', 'block.csv']:
        source = 'NSE'
    elif 'nse' in fname:
        source = 'NSE'
    elif 'sebi' in fname:
        source = 'BSE'  # Default SEBI PIT to BSE unless explicitly NSE
    else:
        source = 'NSE'  # fallback

    return f"{file_type}_{source}_{date_part}.csv"

def rename_recent_files(folder_path, minutes=15):
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
            print(f"⚠ Skipped: {original_name} (unrecognized pattern)")

    return renamed_files
