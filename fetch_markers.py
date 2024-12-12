import os
import re
from collections import defaultdict

# Path to the test directory
TESTS_DIR = r"/var/jenkins_home/workspace/SSVAL/Validation/tests"

# Regex pattern to extract custom markers
MARKER_PATTERN = r"@pytest\.mark\.(\w+)\(\"(.*?)\"\)"

# Output folder to store files
OUTPUT_FOLDER = r"/var/jenkins_home/workspace/SSVAL/output1"

# Function to fetch and store markers and file names
def fetch_and_store_markers_with_files(test_dir, output_folder):
    # Dictionary to group TCIDs and their files by priority and component
    priority_dict = defaultdict(lambda: defaultdict(lambda: defaultdict(set)))
    component_dict = defaultdict(lambda: defaultdict(set))

    # Walk through test directory and parse Python files
    for root, _, files in os.walk(test_dir):
        for file in files:
            if file.endswith(".py"):
                file_path = os.path.join(root, file)
                print(f"Processing file: {file_path}")
                try:
                    with open(file_path, "r", encoding="utf-8") as f:
                        content = f.read()
                except Exception as e:
                    print(f"Error reading file {file_path}: {e}")
                    continue

                # Extract markers using regex
                matches = re.findall(MARKER_PATTERN, content)
                print(f"Matches found in {file}: {matches}")

                # Track markers by order of appearance
                current_tcid = None
                current_priority = None
                current_component = None

                for key, value in matches:
                    print(f"Processing key: {key}, value: {value}")
                    if key == "TCID":
                        # Save the previous group if all values are set
                        if current_tcid and current_priority and current_component:
                            print(f"Saving TCID: {current_tcid}, Priority: {current_priority}, Component: {current_component}")
                            priority_dict[current_priority][current_component][current_tcid].add(file)
                            component_dict[current_component][current_tcid].add(file)

                        # Reset for the new TCID
                        current_tcid = value
                        current_priority = None
                        current_component = None

                    elif key == "priority" and current_tcid:
                        current_priority = value.lower()

                    elif key == "component" and current_tcid and current_priority:
                        current_component = value
                        # Save immediately since all conditions are now met
                        print(f"Saving TCID: {current_tcid}, Priority: {current_priority}, Component: {current_component}")
                        priority_dict[current_priority][current_component][current_tcid].add(file)
                        component_dict[current_component][current_tcid].add(file)
                        # Reset for next match
                        current_tcid = None
                        current_priority = None
                        current_component = None

    # Ensure output folder exists
    os.makedirs(output_folder, exist_ok=True)

    # Save TCIDs in separate files and group files by priority and component
    for priority, components in priority_dict.items():
        # Create a single file for the priority group
        priority_file = os.path.join(output_folder, f"{priority}_priority.txt")
        print(f"Creating priority file: {priority_file}")
        with open(priority_file, "w", encoding="utf-8") as pf:
            for component, tcids in components.items():
                pf.write(f"Component: {component}\n")
                for tcid, files in sorted(tcids.items()):
                    # Save each TCID in its own file
                    tcid_file = os.path.join(output_folder, f"{tcid}.txt")
                    print(f"Creating TCID file: {tcid_file}")
                    with open(tcid_file, "w", encoding="utf-8") as tf:
                        for filename in sorted(files):
                            tf.write(f"{filename}\n")

                    # Write TCID details into the priority file
                    pf.write(f"  TCID: {tcid}\n")
                    for filename in sorted(files):
                        pf.write(f"    - {filename}\n")

        print(f"Priority group '{priority}' stored in: {priority_file}")

    # Save components in separate files
    for component, tcids in component_dict.items():
        component_file = os.path.join(output_folder, f"{component}.txt")
        print(f"Creating component file: {component_file}")
        with open(component_file, "w", encoding="utf-8") as cf:
            for tcid, files in sorted(tcids.items()):
                cf.write(f"TCID: {tcid}\n")
                for filename in sorted(files):
                    cf.write(f"  - {filename}\n")

    # Debug output to verify dictionaries
    print("Priority Dictionary:")
    for priority, components in priority_dict.items():
        print(f"Priority: {priority}")
        for component, tcids in components.items():
            print(f"  Component: {component}")
            for tcid, files in tcids.items():
                print(f"    TCID: {tcid}, Files: {files}")

    print("Component Dictionary:")
    for component, tcids in component_dict.items():
        print(f"Component: {component}")
        for tcid, files in tcids.items():
            print(f"  TCID: {tcid}, Files: {files}")

# Run the function
fetch_and_store_markers_with_files(TESTS_DIR, OUTPUT_FOLDER)
