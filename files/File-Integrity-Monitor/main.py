import hashlib
import time
from datetime import datetime
import os

files_to_monitor = [
    "test1.txt",
    "test2.txt",
    "test3.txt"
]

stored_hashes = {}

def update_baseline(filename, new_hash):
    stored_hashes[filename] = new_hash

    with open("baseline.txt", "w") as baseline:
        for file, file_hash in stored_hashes.items():
            baseline.write(f"{file}:{file_hash}\n")

    print(f"✅ Baseline updated for {filename}")

# Load baseline hashes
with open("baseline.txt", "r") as baseline:
    for line in baseline:
        filename, baseline_hash = line.strip().split(":")
        stored_hashes[filename] = baseline_hash

#prevent repeated alerts for the same file
detected_new_files = set()

print("File Integrity Monitor is running...")
print("Press CTRL + C to stop the program.\n")

while True:

    modified_files = 0

    print("\nChecking file integrity...")

    # Check each file
    for filename in files_to_monitor:
        #check if the file exists
        if not os.path.exists(filename):
            modified_files += 1

            print(f"⚠️ {filename} has been deleted!")

            timestamp = datetime.now().strftime(
                "%Y-%m-%d %H:%M:%S"
            )
            with open("security_log.txt", "a") as log_file:
                log_file.write(
                    f"{timestamp} [CRITICAL] {filename} has been deleted!\n"
                )
            continue

        with open(filename, "r") as file:
            content = file.read()

        current_hash = hashlib.sha256(
            content.encode()
        ).hexdigest()

        timestamp = datetime.now().strftime(
            "%Y-%m-%d %H:%M:%S"
        )

        if current_hash == stored_hashes[filename]:

            print(f"✅ {filename} is unchanged.")

            with open("security_log.txt", "a") as log_file:
                log_file.write(
                    f"{timestamp} [INFO] Integrity verified for {filename}\n"
                )

        else:
            modified_files += 1

            print(f"⚠️ {filename} has been modified!")

            with open("security_log.txt", "a") as log_file:
                log_file.write(
                    f"{timestamp} [WARNING] Integrity violation detected in {filename}\n"
                )
            choice = input(
               f"Do you trust the new version of {filename}? (y/n): "
            ).lower()

            if choice == "y":
               update_baseline(filename, current_hash)

               with open("security_log.txt", "a") as log_file:
                  log_file.write(
                   f"{timestamp} [INFO] Baseline updated for {filename}\n"
            )

    #detect new files
    current_files = os.listdir(".")

    for file in current_files:

        if (
            file.endswith(".txt")
            and file not in stored_hashes
            and file not in ["baseline.txt", "security_log.txt"]
            and file not in detected_new_files
        ):
            detected_new_files.add(file)

            print(f"🆕 New file detected: {file}")

            timestamp = datetime.now().strftime(
                "%Y-%m-%d %H:%M:%S"
            )

            with open("security_log.txt", "a") as log_file:
                log_file.write(
                    f"{timestamp} [WARNING] New file detected: {file}\n"
                )

            
        

    # Detect multiple file changes
    if modified_files >= 2:

        timestamp = datetime.now().strftime(
            "%Y-%m-%d %H:%M:%S"
        )

        with open("security_log.txt", "a") as log_file:
            log_file.write(
                f"{timestamp} [CRITICAL] Multiple file integrity violations detected!\n"
            )

        print("\n🚨 CRITICAL ALERT: Multiple files have changed!")

    print("\nWaiting 10 seconds before the next check...\n")

    time.sleep(10)