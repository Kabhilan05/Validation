import os
import re
from collections import defaultdict

# Paths
TESTS_DIR = "/var/jenkins_home/workspace/SSVAL/Validation/tests"
OUTPUT_FOLDER = "/var/jenkins_home/workspace/SSVAL/output1"

# Regex pattern for extracting markers
MARKER_PATTERN = r"@pytest\.mark\.(\w+)\(\"(.*?)\"\)"

def fetch_and_store_markers_with_files(test_dir, output_folder):
    # Dictionaries to store priority and component data
    priority_dict = defaultdict(lambda: defaultdict(lambda: defaultdict(set)))
    component_dict = defaultdict(lambda: defaultdict(set))

    # Walk through test directory
    for root, _, files in os.walk(test_dir):
        for file in files:
            if file.endswith(".py"):
                file_path = os.path.join(root, file)
                try:
                    with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
                        content = f.read()
                except Exception as e:
                    print(f"Error reading file {file_path}: {e}")
                    continue

                # Extract all matches
                matches = re.findall(MARKER_PATTERN, content)
                print(f"Matches found in {file}: {matches}")

                # State variables
                current_tcid = None
                current_priority = None
                current_component = None

                # Process matches
                for key, value in matches:
                    if key == "TCID":
                        # If a new TCID is encountered, store previous data
                        if current_tcid and current_priority and current_component:
                            priority_dict[current_priority][current_component][current_tcid].add(file)
                            component_dict[current_component][current_tcid].add(file)
                        # Start a new TCID group
                        current_tcid = value
                        current_priority = None
                        current_component = None
                    elif key == "priority" and current_tcid:
                        current_priority = value.lower()
                    elif key == "component" and current_tcid:
                        current_component = value

                # Store the last TCID group
                if current_tcid and current_priority and current_component:
                    priority_dict[current_priority][current_component][current_tcid].add(file)
                    component_dict[current_component][current_tcid].add(file)

    # Debug output
    print("Priority Dictionary:")
    print(priority_dict)
    print("Component Dictionary:")
    print(component_dict)

    # Ensure output folder exists
    os.makedirs(output_folder, exist_ok=True)

    # Save Priority Data
    for priority, components in priority_dict.items():
        priority_file = os.path.join(output_folder, f"{priority}_priority.txt")
        print(f"Creating priority file: {priority_file}")
        with open(priority_file, "w", encoding="utf-8") as pf:
            for component, tcids in components.items():
                pf.write(f"Component: {component}\n")
                for tcid, files in sorted(tcids.items()):
                    tcid_file = os.path.join(output_folder, f"{tcid}.txt")
                    print(f"Creating TCID file: {tcid_file}")
                    with open(tcid_file, "w", encoding="utf-8") as tf:
                        for filename in sorted(files):
                            tf.write(f"{filename}\n")
                    pf.write(f"  TCID: {tcid}\n")
                    for filename in sorted(files):
                        pf.write(f"    - {filename}\n")

    # Save Component Data
    for component, tcids in component_dict.items():
        component_file = os.path.join(output_folder, f"{component}.txt")
        print(f"Creating component file: {component_file}")
        with open(component_file, "w", encoding="utf-8") as cf:
            for tcid, files in sorted(tcids.items()):
                cf.write(f"TCID: {tcid}\n")
                for filename in sorted(files):
                    cf.write(f"  - {filename}\n")

fetch_and_store_markers_with_files(TESTS_DIR, OUTPUT_FOLDER)
