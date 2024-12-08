import os
import re
from collections import defaultdict

# Path to the test directory
TESTS_DIR = r"/var/jenkins_home/workspace/SSVAL/Validation"

# Regex pattern to extract custom markers
MARKER_PATTERN = r"@pytest\.mark\.(\w+)\(\"(.*?)\"\)"

# Output folder to store files
OUTPUT_FOLDER = r"/var/jenkins_home/workspace/SSVAL/output"

# Function to fetch and store markers and file names
def fetch_and_store_markers_with_files(test_dir, output_folder):
    # Dictionary to group values and their files by keys
    marker_dict = defaultdict(lambda: defaultdict(set))

    # Walk through test directory and parse Python files
    for root, _, files in os.walk(test_dir):
        for file in files:
            if file.endswith(".py"):
                file_path = os.path.join(root, file)
                with open(file_path, "r", encoding="utf-8") as f:
                    content = f.read()
                
                # Extract markers using regex
                matches = re.findall(MARKER_PATTERN, content)
                for key, value in matches:
                    marker_dict[key][value].add(file)  # Group values by files

    # Ensure output folder exists
    os.makedirs(output_folder, exist_ok=True)

    # Save keys in a file
    keys_file = os.path.join(output_folder, "keys.txt")
    with open(keys_file, "w", encoding="utf-8") as f:
        for key in sorted(marker_dict.keys()):
            f.write(f"{key}\n")
    print(f"Keys stored in: {keys_file}")

    # Save values and file names for each key
    for key, values in marker_dict.items():
        # File for storing marker values
        values_file = os.path.join(output_folder, f"{key}.txt")
        # File for storing file names
        files_file = os.path.join(output_folder, f"{key}_files.txt")
        
        with open(values_file, "w", encoding="utf-8") as vf, open(files_file, "w", encoding="utf-8") as ff:
            file_set = set()  # Track unique file names
            for value, files in sorted(values.items()):
                # Write marker value and associated files to the values file
                vf.write(f"{value}\n")
                # Add associated files to the file set
                file_set.update(files)
            
            # Write unique file names for the key to the files file
            for filename in sorted(file_set):
                ff.write(f"{filename}\n")

        print(f"Values for '{key}' stored in: {values_file}")
        print(f"File names for '{key}' stored in: {files_file}")

# Run the function
fetch_and_store_markers_with_files(TESTS_DIR, OUTPUT_FOLDER)
