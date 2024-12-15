import os
import re
from collections import defaultdict

# Path to the test directory
TESTS_DIR = r"/var/jenkins_home/workspace/SSVAL/Validation/tests"

# Regex patterns to extract Priority, Component, and TCID markers
PRIORITY_PATTERN = r"@pytest\.mark\.Priority\((?:\"(.*?)\"|'(.*?)')\)"
COMPONENT_PATTERN = r"@pytest\.mark\.Component\((?:\"(.*?)\"|'(.*?)')\)"
TCID_PATTERN = r"@pytest\.mark\.TCID\((?:\"(.*?)\"|'(.*?)')\)"

# Output folder to store files
OUTPUT_FOLDER = r"/var/jenkins_home/workspace/SSVAL/output"

# Function to fetch and store filenames based on Priority, Component, and TCID
def fetch_and_store_priority_component_files(test_dir, output_folder):
    # Dictionary to map (priority, component) to a set of filenames
    priority_component_dict = defaultdict(set)
    # Dictionary to map TCIDs to a set of filenames
    tcid_dict = defaultdict(set)
    # Set to store all unique components
    all_components = set()
    # Set to store all unique TCIDs
    all_tcids = set()

    # Walk through the test directory and parse Python files
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

                # Extract Priority, Component, and TCID markers using regex
                priority_matches = re.findall(PRIORITY_PATTERN, content)
                component_matches = re.findall(COMPONENT_PATTERN, content)
                tcid_matches = re.findall(TCID_PATTERN, content)

                # Use the non-empty values from regex matches
                priorities = {match[0] or match[1] for match in priority_matches}
                components = {match[0] or match[1] for match in component_matches}
                tcids = {match[0] or match[1] for match in tcid_matches}

                # Add components and TCIDs to their respective sets
                all_components.update(components)
                all_tcids.update(tcids)

                # Map each combination of priority and component to the file
                for priority in priorities:
                    for component in components:
                        key = (priority, component)
                        priority_component_dict[key].add(file)

                # Map each TCID to the file
                for tcid in tcids:
                    tcid_dict[tcid].add(file)

    # Ensure the output folder exists
    os.makedirs(output_folder, exist_ok=True)

    # Write filenames to separate files based on priority and component
    for (priority, component), files in priority_component_dict.items():
        formatted_priority = priority.capitalize()  # Capitalize priority
        output_file = os.path.join(output_folder, f"{formatted_priority}_{component}.txt")
        print(f"Creating file: {output_file}")
        with open(output_file, "w", encoding="utf-8") as f:
            for filename in sorted(files):
                f.write(f"{filename}\n")

    # Write all unique components to components.txt
    components_file = os.path.join(output_folder, "Components.txt")
    print(f"Creating components file: {components_file}")
    with open(components_file, "w", encoding="utf-8") as f:
        for component in sorted(all_components):
            f.write(f"{component}\n")

    # Write all unique TCIDs to TCID.txt
    tcid_file = os.path.join(output_folder, "TCID.txt")
    print(f"Creating TCID file: {tcid_file}")
    with open(tcid_file, "w", encoding="utf-8") as f:
        for tcid in sorted(all_tcids):
            f.write(f"{tcid}\n")

    # Write filenames to separate files based on TCID
    for tcid, files in tcid_dict.items():
        tcid_file = os.path.join(output_folder, f"{tcid}.txt")
        print(f"Creating TCID file: {tcid_file}")
        with open(tcid_file, "w", encoding="utf-8") as f:
            for filename in sorted(files):
                f.write(f"{filename}\n")

    print(f"Files have been created in {output_folder}")

# Run the function
fetch_and_store_priority_component_files(TESTS_DIR, OUTPUT_FOLDER)
