import hashlib
import time
from datetime import datetime
import os
import json
from colorama import init, Fore, Style

# Initialize colorama
init(autoreset=True)

# ==========================
# Load Configuration
# ==========================
with open("config.json", "r") as config_file:
    config = json.load(config_file)

required_keys = [
    "monitored_folder",
    "scan_interval",
    "dangerous_extensions"
]

for key in required_keys:
    if key not in config:
        raise Exception(
            f"Missing configuration value: {key}"
        )

MONITORED_FOLDER = config["monitored_folder"]
SCAN_INTERVAL = config["scan_interval"]
DANGEROUS_EXTENSIONS = config["dangerous_extensions"]

# ==========================
# Variables
# ==========================
stored_hashes = {}
detected_new_files = set()
detected_deleted_files = set()

# Statistics
files_checked = 0
modified_count = 0
deleted_count = 0
new_files_count = 0
critical_alerts = 0


# ==========================
# Functions
# ==========================
def get_files_to_monitor():
    files = []

    if not os.path.exists(MONITORED_FOLDER):
        os.makedirs(MONITORED_FOLDER)

    for file in os.listdir(MONITORED_FOLDER):
        full_path = os.path.join(
            MONITORED_FOLDER,
            file
        )

        if os.path.isfile(full_path):
            files.append(full_path)

    return files


def save_baseline():
    with open("baseline.txt", "w") as baseline:
        for file, file_hash in stored_hashes.items():
            baseline.write(
                f"{file}:{file_hash}\n"
            )


def create_baseline():
    for filename in get_files_to_monitor():

        with open(filename, "r") as file:
            content = file.read()

        file_hash = hashlib.sha256(
            content.encode()
        ).hexdigest()

        stored_hashes[filename] = file_hash

    save_baseline()

    print(
        Fore.GREEN +
        "✅ Baseline created successfully."
    )


def update_baseline(filename, new_hash):
    stored_hashes[filename] = new_hash

    save_baseline()

    print(
        Fore.GREEN +
        f"✅ Baseline updated for {filename}"
    )


# ==========================
# Setup
# ==========================
if not os.path.exists(MONITORED_FOLDER):
    os.makedirs(MONITORED_FOLDER)

    print(
        Fore.YELLOW +
        f"📁 Created monitoring folder: "
        f"{MONITORED_FOLDER}"
    )

if not os.path.exists("baseline.txt"):
    print(
        Fore.CYAN +
        "⚠️ baseline.txt not found."
    )

    print(
        Fore.CYAN +
        "Creating baseline automatically..."
    )

    create_baseline()

# Load baseline
with open("baseline.txt", "r") as baseline:
    for line in baseline:

        line = line.strip()

        if not line:
            continue

        filename, baseline_hash = line.split(":", 1)

        stored_hashes[filename] = baseline_hash


# ==========================
# Startup
# ==========================
print("=" * 50)
print(
    Fore.CYAN +
    "FILE INTEGRITY MONITOR STARTED"
)
print("=" * 50)

print(
    f"Monitoring folder: "
    f"{MONITORED_FOLDER}"
)

print(
    f"Scan interval: "
    f"{SCAN_INTERVAL} seconds"
)

print(
    "Dangerous extensions: "
    + ", ".join(DANGEROUS_EXTENSIONS)
)

print(
    Fore.CYAN +
    "\nPress CTRL + C to stop.\n"
)


# ==========================
# Main Loop
# ==========================
try:

    while True:

        modified_files = 0

        print(
            Fore.BLUE +
            "\nChecking file integrity...\n"
        )

        files_to_monitor = get_files_to_monitor()

        # ----------------------
        # Detect Deleted Files
        # ----------------------
        for stored_file in list(stored_hashes.keys()):

            if (
                not os.path.exists(stored_file)
                and stored_file not in detected_deleted_files
            ):

                detected_deleted_files.add(
                    stored_file
                )

                deleted_count += 1
                critical_alerts += 1
                modified_files += 1

                timestamp = datetime.now().strftime(
                    "%Y-%m-%d %H:%M:%S"
                )

                print(
                    Fore.RED +
                    f"❌ CRITICAL: "
                    f"{stored_file} was deleted!"
                )

                with open(
                    "security_log.txt",
                    "a"
                ) as log_file:
                    log_file.write(
                        f"{timestamp} "
                        f"[CRITICAL] "
                        f"{stored_file} "
                        f"was deleted.\n"
                    )

                stored_hashes.pop(
                    stored_file,
                    None
                )

                save_baseline()

        # ----------------------
        # Check Files
        # ----------------------
        for filename in files_to_monitor:

            files_checked += 1

            timestamp = datetime.now().strftime(
                "%Y-%m-%d %H:%M:%S"
            )

            # New file detection
            if (
                filename not in stored_hashes
                and filename not in detected_new_files
            ):

                detected_new_files.add(
                    filename
                )

                new_files_count += 1

                extension = os.path.splitext(
                    filename
                )[1].lower()

                with open(
                    "security_log.txt",
                    "a"
                ) as log_file:

                    if (
                        extension
                        in DANGEROUS_EXTENSIONS
                    ):

                        critical_alerts += 1

                        print(
                            Fore.RED +
                            f"🚨 CRITICAL: "
                            f"Suspicious file detected: "
                            f"{filename}"
                        )

                        log_file.write(
                            f"{timestamp} "
                            f"[CRITICAL] "
                            f"Suspicious file detected: "
                            f"{filename}\n"
                        )

                    else:

                        print(
                            Fore.MAGENTA +
                            f"🆕 New file detected: "
                            f"{filename}"
                        )

                        log_file.write(
                            f"{timestamp} "
                            f"[WARNING] "
                            f"New file detected: "
                            f"{filename}\n"
                        )

                continue

            # Calculate current hash
            with open(
                filename,
                "r"
            ) as file:
                content = file.read()

            current_hash = hashlib.sha256(
                content.encode()
            ).hexdigest()

            # Compare hashes
            if (
                current_hash
                == stored_hashes.get(
                    filename
                )
            ):

                print(
                    Fore.GREEN +
                    f"✅ INFO: "
                    f"{filename} "
                    f"is unchanged."
                )

                with open(
                    "security_log.txt",
                    "a"
                ) as log_file:
                    log_file.write(
                        f"{timestamp} "
                        f"[INFO] "
                        f"Integrity verified for "
                        f"{filename}\n"
                    )

            else:

                modified_files += 1
                modified_count += 1

                print(
                    Fore.YELLOW +
                    f"⚠️ WARNING: "
                    f"{filename} "
                    f"has been modified!"
                )

                with open(
                    "security_log.txt",
                    "a"
                ) as log_file:
                    log_file.write(
                        f"{timestamp} "
                        f"[WARNING] "
                        f"Integrity violation "
                        f"detected in "
                        f"{filename}\n"
                    )

                choice = input(
                    f"Do you trust the "
                    f"new version of "
                    f"{filename}? "
                    f"(y/n): "
                ).lower()

                if choice == "y":

                    update_baseline(
                        filename,
                        current_hash
                    )

                    with open(
                        "security_log.txt",
                        "a"
                    ) as log_file:
                        log_file.write(
                            f"{timestamp} "
                            f"[INFO] "
                            f"Baseline updated "
                            f"for {filename}\n"
                        )

        # ----------------------
        # Multiple Changes Alert
        # ----------------------
        if modified_files >= 2:

            critical_alerts += 1

            timestamp = datetime.now().strftime(
                "%Y-%m-%d %H:%M:%S"
            )

            with open(
                "security_log.txt",
                "a"
            ) as log_file:
                log_file.write(
                    f"{timestamp} "
                    f"[CRITICAL] "
                    f"Multiple file "
                    f"integrity violations "
                    f"detected!\n"
                )

            print(
                Fore.RED +
                Style.BRIGHT +
                "\n🚨 CRITICAL ALERT: "
                "Multiple files "
                "have changed!"
            )

        print(
            f"\nWaiting "
            f"{SCAN_INTERVAL} "
            f"seconds before "
            f"the next check...\n"
        )

        time.sleep(
            SCAN_INTERVAL
        )

except KeyboardInterrupt:

    print("\n")
    print("=" * 50)
    print(
        Fore.CYAN +
        "FILE INTEGRITY "
        "MONITOR SUMMARY"
    )
    print("=" * 50)

    print(
        f"Files checked: "
        f"{files_checked}"
    )

    print(
        f"Modified files: "
        f"{modified_count}"
    )

    print(
        f"Deleted files: "
        f"{deleted_count}"
    )

    print(
        f"New files detected: "
        f"{new_files_count}"
    )

    print(
        f"Critical alerts: "
        f"{critical_alerts}"
    )

    print("=" * 50)

    print(
        Fore.CYAN +
        "\nStopping File "
        "Integrity Monitor..."
    )

    print(
        Fore.GREEN +
        "Goodbye 👋"
    )