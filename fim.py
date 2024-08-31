import os
import hashlib
import json
import logging
from datetime import datetime

# Configurations
MONITOR_DIRECTORY = '/path/to/monitor'  # Directory to monitor
BASELINE_FILE = 'baseline.json'          # File to store the baseline data
LOG_FILE = 'fim.log'                    # Log file for changes
HASH_ALGORITHM = 'sha256'               # Hash algorithm to use (e.g., sha256, md5)

# Initialize logging
logging.basicConfig(filename=LOG_FILE, level=logging.INFO, format='%(asctime)s - %(message)s')

def calculate_hash(file_path, algorithm=HASH_ALGORITHM):
    """Calculate the hash of a file."""
    hasher = hashlib.new(algorithm)
    with open(file_path, 'rb') as f:
        for byte_block in iter(lambda: f.read(4096), b""):
            hasher.update(byte_block)
    return hasher.hexdigest()

def create_baseline(directory):
    """Create a baseline of the files in the specified directory."""
    baseline = {}
    for dirpath, dirnames, filenames in os.walk(directory):
        for filename in filenames:
            file_path = os.path.join(dirpath, filename)
            if os.path.isfile(file_path):
                try:
                    file_info = os.stat(file_path)
                    file_hash = calculate_hash(file_path)
                    baseline[file_path] = {
                        'size': file_info.st_size,
                        'mtime': file_info.st_mtime,
                        'hash': file_hash
                    }
                except (FileNotFoundError, PermissionError) as e:
                    logging.error(f"Error accessing file {file_path}: {e}")
    return baseline

def save_baseline(baseline, filename=BASELINE_FILE):
    """Save the baseline data to a file."""
    with open(filename, 'w') as f:
        json.dump(baseline, f)

def load_baseline(filename=BASELINE_FILE):
    """Load the baseline data from a file."""
    if not os.path.exists(filename):
        return {}
    with open(filename, 'r') as f:
        return json.load(f)

def detect_changes(baseline, directory):
    """Detect changes in the files compared to the baseline."""
    current_state = create_baseline(directory)
    changes = {}
    for file_path, attrs in current_state.items():
        if file_path not in baseline:
            changes[file_path] = 'New File'
        else:
            for key in attrs:
                if attrs[key] != baseline[file_path][key]:
                    changes[file_path] = 'Modified'
                    break
    
    for file_path in baseline:
        if file_path not in current_state:
            changes[file_path] = 'Deleted'
    
    return changes

def log_changes(changes):
    """Log detected changes to a file and optionally print alerts."""
    for file_path, change_type in changes.items():
        message = f"{change_type} detected: {file_path}"
        logging.info(message)
        print(message)  # Simulating alert

def main():
    # Load the existing baseline
    baseline = load_baseline()

    # Detect changes
    changes = detect_changes(baseline, MONITOR_DIRECTORY)

    if changes:
        # Log changes
        log_changes(changes)
    else:
        logging.info('No changes detected.')

    # Update baseline after checking
    save_baseline(create_baseline(MONITOR_DIRECTORY))

if __name__ == "__main__":
    main()
