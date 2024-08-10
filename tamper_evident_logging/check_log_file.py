import hashlib
import base64
import os
import sys

def compute_hash(data):
    """Compute a SHA-256 hash of the given data."""
    hasher = hashlib.sha256()
    hasher.update(data.encode('utf-8'))
    return base64.b64encode(hasher.digest()).decode('utf-8')

def check_all_logs():
    log_filename = "hashed_log.txt"
    head_filename = "hashed_header.txt"

    # Check if both files exist
    if not os.path.exists(log_filename) or not os.path.exists(head_filename):
        print(f"failed: {'hashed_header.txt is missing' if not os.path.exists(head_filename) else 'hashed_log.txt is missing'}")
        sys.exit(1)

    if (os.path.getsize(log_filename) == 0):
        print(f"Log file is empty.")
        sys.exit(1)
        
    if (os.path.getsize(head_filename) == 0):
        print(f"Header file is empty.")
        sys.exit(1)

    with open(head_filename, 'r') as head_file:
        expected_hash = head_file.read().strip()

    previous_line_hash = 'begin'
    line_number = 0
    with open(log_filename, 'r') as log_file:
        for line in log_file:
            
            stripped_line = line.strip()  # Remove leading and trailing whitespace
            if len(stripped_line) == 0:
                continue  # Skip the empty line
            
            line_number += 1
            line = line.rstrip('\n')  # Remove the newline at the end for hash computation
            if not line:  # Skip empty lines
                continue
            
            # Split the line to extract its components
            parts = line.split(' - ', 2)
            
            if len(parts) != 2:
                print(f"failed: Line {line_number} is improperly formatted.")
                sys.exit(1)
            
            # Extract the hash in the current line (this should be "begin" if it is the first line)
            current_line_hash = parts[1].split(' ', 1)[0]
            
            # First line, comparing its hash part with 'begin'
            if line_number == 1:  
                if current_line_hash != previous_line_hash:
                    print(f"failed: Line {line_number} does not have 'begin' as previous hash. There may be no starting line.")
                    sys.exit(1)
            
            # For lines after the first line, the hash must be equal to the hash of the ENTIRE previous line
            else:
                if current_line_hash != previous_line_hash:
                    print(f"failed: Hash of line {line_number - 1} hash does not match with the hash in line {line_number}.")
                    sys.exit(1)
            
            # Update previous_line_hash with the hash of the current line
            previous_line_hash = compute_hash(line)

    # Check the last hash against expected_hash from hashed_header.txt
    if expected_hash != previous_line_hash:
        print(f"failed: Last line hash does not match head pointer.")
        sys.exit(1)

    print("valid")
    sys.exit(0)

if __name__ == "__main__":
    if len(sys.argv) > 1:
        print("Usage: check_log_file. Improper number of arguments.")
        sys.exit(1)
    check_all_logs()
