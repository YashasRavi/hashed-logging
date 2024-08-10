import sys
import os
import hashlib
import base64
from datetime import datetime

def compute_hash(data):
    """ Compute a SHA-256 hash of the given data. """
    hasher = hashlib.sha256()
    hasher.update(data.encode('utf-8'))
    return base64.b64encode(hasher.digest()).decode('utf-8')

def add_single_log(log_string):
    # Define the filenames
    log_filename = "hashed_log.txt"
    head_filename = "hashed_header.txt"

    # Read the head pointer (the hash of the last log entry)
    head_pointer = 'begin'
    if os.path.exists(head_filename):
        if (os.path.exists(log_filename) and os.path.getsize(log_filename) > 0):
            with open(head_filename, 'r') as head_file:
                head_pointer = head_file.read().strip() or 'begin'
        else:
            with open(head_filename, 'r') as head_file:
                head_pointer = 'begin'
    elif os.path.exists(log_filename):
        print("Error: hashed_header.txt is missing but hashed_log.txt exists. Cannot verify integrity of the log.")
        sys.exit(1)

    # Create the log entry string with the current timestamp
    timestamp = datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%SZ')
    log_entry = f"{timestamp} - {head_pointer} {log_string}"

    # Append the log entry to log.txt with a newline
    with open(log_filename, 'a') as log_file:
        log_file.write(log_entry + '\n')

    # Compute the hash of the log entry
    hash_digest = compute_hash(log_entry)

    # Write the new hash to loghead.txt
    with open(head_filename, 'w') as head_file:
        head_file.write(hash_digest)

def main():
    if len(sys.argv) != 2:
        print("Usage: add_log_file <log_string>. Wrong number of command line arguments.")
        sys.exit(1)
    
    # Replace newline characters in the log string with spaces
    log_string = sys.argv[1].replace('\n', ' ')
    add_single_log(log_string)

if __name__ == "__main__":
    main()
