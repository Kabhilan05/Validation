# import os
# import re
# from collections import defaultdict

# # Path to the test directory
# TESTS_DIR = r"/var/jenkins_home/workspace/SSVAL/Validation/tests"

# # Regex pattern to extract custom markers
# MARKER_PATTERN = r"@pytest\.mark\.(\w+)\(\"(.*?)\"\)"

# # Output folder to store files
# OUTPUT_FOLDER = r"/var/jenkins_home/workspace/SSVAL/output"

# # Function to fetch and store markers and file names
# def fetch_and_store_markers_with_files(test_dir, output_folder):
#     # Dictionary to group TCIDs and their files by priority and component
#     priority_dict = defaultdict(lambda: defaultdict(lambda: defaultdict(set)))
#     component_dict = defaultdict(lambda: defaultdict(set))

#     # Walk through test directory and parse Python files
#     for root, _, files in os.walk(test_dir):
#         for file in files:
#             if file.endswith(".py"):
#                 file_path = os.path.join(root, file)
#                 print(f"Processing file: {file_path}")
#                 try:
#                     with open(file_path, "r", encoding="utf-8") as f:
#                         content = f.read()
#                 except Exception as e:
#                     print(f"Error reading file {file_path}: {e}")
#                     continue

#                 # Extract markers using regex
#                 matches = re.findall(MARKER_PATTERN, content)
#                 print(f"Matches found in {file}: {matches}")

#                 # Process markers in sequence
#                 current_tcid = None
#                 current_priority = None
#                 current_component = None

#                 for key, value in matches:
#                     print(f"Processing key: {key}, value: {value}")
#                     if key == "TCID":
#                         # Save the previous set if valid
#                         if current_tcid and current_priority and current_component:
#                             priority_dict[current_priority][current_component][current_tcid].add(file)
#                             component_dict[current_component][current_tcid].add(file)
#                         # Start a new TCID group
#                         current_tcid = value
#                         current_priority = None
#                         current_component = None

#                     elif key == "Priority" and current_tcid:
#                         current_priority = value.lower()

#                     elif key == "Component" and current_tcid and current_priority:
#                         current_component = value
#                         # Save the complete set
#                         print(f"Saving TCID: {current_tcid}, Priority: {current_priority}, Component: {current_component}")
#                         priority_dict[current_priority][current_component][current_tcid].add(file)
#                         component_dict[current_component][current_tcid].add(file)
#                         # Reset for the next marker group
#                         current_tcid = None
#                         current_priority = None
#                         current_component = None

#                 # Save any remaining set after the loop
#                 if current_tcid and current_priority and current_component:
#                     print(f"Saving final TCID: {current_tcid}, Priority: {current_priority}, Component: {current_component}")
#                     priority_dict[current_priority][current_component][current_tcid].add(file)
#                     component_dict[current_component][current_tcid].add(file)

#     # Ensure output folder exists
#     os.makedirs(output_folder, exist_ok=True)

#     # Save TCIDs in separate files and group files by priority and component
#     for priority, components in priority_dict.items():
#         priority_file = os.path.join(output_folder, f"{priority}_priority.txt")
#         print(f"Creating priority file: {priority_file}")
#         with open(priority_file, "w", encoding="utf-8") as pf:
#             for component, tcids in components.items():
#                 pf.write(f"Component: {component}\n")
#                 for tcid, files in sorted(tcids.items()):
#                     tcid_file = os.path.join(output_folder, f"{tcid}.txt")
#                     print(f"Creating TCID file: {tcid_file}")
#                     with open(tcid_file, "w", encoding="utf-8") as tf:
#                         for filename in sorted(files):
#                             tf.write(f"{filename}\n")
#                     pf.write(f"  TCID: {tcid}\n")
#                     for filename in sorted(files):
#                         pf.write(f"    - {filename}\n")

#     for component, tcids in component_dict.items():
#         component_file = os.path.join(output_folder, f"{component}.txt")
#         print(f"Creating component file: {component_file}")
#         with open(component_file, "w", encoding="utf-8") as cf:
#             for tcid, files in sorted(tcids.items()):
#                 cf.write(f"TCID: {tcid}\n")
#                 for filename in sorted(files):
#                     cf.write(f"  - {filename}\n")

#     # Debugging dictionaries
#     print("Priority Dictionary:")
#     for priority, components in priority_dict.items():
#         print(f"Priority: {priority}")
#         for component, tcids in components.items():
#             print(f"  Component: {component}")
#             for tcid, files in tcids.items():
#                 print(f"    TCID: {tcid}, Files: {files}")

#     print("Component Dictionary:")
#     for component, tcids in component_dict.items():
#         print(f"Component: {component}")
#         for tcid, files in tcids.items():
#             print(f"  TCID: {tcid}, Files: {files}")

# # Run the function
# fetch_and_store_markers_with_files(TESTS_DIR, OUTPUT_FOLDER)



# import os
# import re
# from collections import defaultdict

# # Path to the test directory
# TESTS_DIR = r"/var/jenkins_home/workspace/SSVAL/Validation/tests"

# # Regex pattern to extract custom markers
# MARKER_PATTERN = r"@pytest\.mark\.(\w+)\((?:\"(.*?)\"|'(.*?)')\)"

# # Output folder to store files
# OUTPUT_FOLDER = r"/var/jenkins_home/workspace/SSVAL/output"

# # Function to fetch and store markers and file names
# def fetch_and_store_markers_with_files(test_dir, output_folder):
#     # Dictionary to group TCIDs and their files by priority and component
#     priority_dict = defaultdict(lambda: defaultdict(lambda: defaultdict(set)))
#     component_dict = defaultdict(lambda: defaultdict(set))
#     keys_dict = defaultdict(set)  # Dictionary to store all keys and their values

#     # Walk through test directory and parse Python files
#     for root, _, files in os.walk(test_dir):
#         for file in files:
#             if file.endswith(".py"):
#                 file_path = os.path.join(root, file)
#                 print(f"Processing file: {file_path}")
#                 try:
#                     with open(file_path, "r", encoding="utf-8") as f:
#                         content = f.read()
#                 except Exception as e:
#                     print(f"Error reading file {file_path}: {e}")
#                     continue

#                 # Extract markers using regex
#                 matches = re.findall(MARKER_PATTERN, content)
#                 print(f"Matches found in {file}: {matches}")

#                 # Process markers in sequence
#                 current_tcid = None
#                 current_priority = None
#                 current_component = None

#                 for key, double_quoted_value, single_quoted_value in matches:
#                     # Use the non-empty value
#                     value = double_quoted_value or single_quoted_value
#                     print(f"Processing key: {key}, value: {value}")

#                     # Store keys (no values needed now)
#                     keys_dict[key] = None

#                     if key == "TCID":
#                         # Save the previous set if valid
#                         if current_tcid and current_priority and current_component:
#                             priority_dict[current_priority][current_component][current_tcid].add(file)
#                             component_dict[current_component][current_tcid].add(file)
#                         # Start a new TCID group
#                         current_tcid = value
#                         current_priority = None
#                         current_component = None

#                     elif key == "Priority" and current_tcid:
#                         current_priority = value.lower()

#                     elif key == "Component" and current_tcid and current_priority:
#                         current_component = value
#                         # Save the complete set
#                         print(f"Saving TCID: {current_tcid}, Priority: {current_priority}, Component: {current_component}")
#                         priority_dict[current_priority][current_component][current_tcid].add(file)
#                         component_dict[current_component][current_tcid].add(file)
#                         # Reset for the next marker group
#                         current_tcid = None
#                         current_priority = None
#                         current_component = None

#                 # Save any remaining set after the loop
#                 if current_tcid and current_priority and current_component:
#                     print(f"Saving final TCID: {current_tcid}, Priority: {current_priority}, Component: {current_component}")
#                     priority_dict[current_priority][current_component][current_tcid].add(file)
#                     component_dict[current_component][current_tcid].add(file)

#     # Ensure output folder exists
#     os.makedirs(output_folder, exist_ok=True)

#     # Save TCIDs in separate files and group files by priority and component
#     for priority, components in priority_dict.items():
#         priority_file = os.path.join(output_folder, f"{priority}_priority.txt")
#         print(f"Creating priority file: {priority_file}")
#         with open(priority_file, "w", encoding="utf-8") as pf:
#             for component, tcids in components.items():
#                 pf.write(f"Component: {component}\n")
#                 for tcid, files in sorted(tcids.items()):
#                     tcid_file = os.path.join(output_folder, f"{tcid}.txt")
#                     print(f"Creating TCID file: {tcid_file}")
#                     with open(tcid_file, "w", encoding="utf-8") as tf:
#                         for filename in sorted(files):
#                             tf.write(f"{filename}\n")
#                     pf.write(f"  TCID: {tcid}\n")
#                     for filename in sorted(files):
#                         pf.write(f"    - {filename}\n")

#     for component, tcids in component_dict.items():
#         component_file = os.path.join(output_folder, f"{component}.txt")
#         print(f"Creating component file: {component_file}")
#         with open(component_file, "w", encoding="utf-8") as cf:
#             for tcid, files in sorted(tcids.items()):
#                 cf.write(f"TCID: {tcid}\n")
#                 for filename in sorted(files):
#                     cf.write(f"  - {filename}\n")

#     # Save only the keys (no values) to a file
#     keys_file = os.path.join(output_folder, "keys.txt")
#     print(f"Creating keys file: {keys_file}")
#     with open(keys_file, "w", encoding="utf-8") as kf:
#         for key in sorted(keys_dict.keys()):
#             kf.write(f"{key}\n")

#     # Debugging dictionaries
#     print("Priority Dictionary:")
#     for priority, components in priority_dict.items():
#         print(f"Priority: {priority}")
#         for component, tcids in components.items():
#             print(f"  Component: {component}")
#             for tcid, files in tcids.items():
#                 print(f"    TCID: {tcid}, Files: {files}")

#     print("Component Dictionary:")
#     for component, tcids in component_dict.items():
#         print(f"Component: {component}")
#         for tcid, files in tcids.items():
#             print(f"  TCID: {tcid}, Files: {files}")

# # Run the function
# fetch_and_store_markers_with_files(TESTS_DIR, OUTPUT_FOLDER)



import os
import re
from collections import defaultdict

# Path to the test directory
TESTS_DIR = r"/var/jenkins_home/workspace/SSVAL/Validation/tests"

# Regex patterns to extract Priority and Component markers
PRIORITY_PATTERN = r"@pytest\.mark\.Priority\((?:\"(.*?)\"|'(.*?)')\)"
COMPONENT_PATTERN = r"@pytest\.mark\.Component\((?:\"(.*?)\"|'(.*?)')\)"

# Output folder to store files
OUTPUT_FOLDER = r"/var/jenkins_home/workspace/SSVAL/output"

# Function to fetch and store filenames based on Priority and Component
def fetch_and_store_priority_component_files(test_dir, output_folder):
    # Dictionary to map (priority, component) to a set of filenames
    priority_component_dict = defaultdict(set)

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

                # Extract Priority and Component markers using regex
                priority_matches = re.findall(PRIORITY_PATTERN, content)
                component_matches = re.findall(COMPONENT_PATTERN, content)

                # Use the non-empty values from regex matches
                priorities = {match[0] or match[1] for match in priority_matches}
                components = {match[0] or match[1] for match in component_matches}

                # Map each combination of priority and component to the file
                for priority in priorities:
                    for component in components:
                        key = (priority.lower(), component)
                        priority_component_dict[key].add(file)

    # Ensure the output folder exists
    os.makedirs(output_folder, exist_ok=True)

    # Write filenames to separate files based on priority and component
    for (priority, component), files in priority_component_dict.items():
        output_file = os.path.join(output_folder, f"{priority}_{component}.txt")
        print(f"Creating file: {output_file}")
        with open(output_file, "w", encoding="utf-8") as f:
            for filename in sorted(files):
                f.write(f"{filename}\n")
    print(f"Files have been created in {output_folder}")

# Run the function
fetch_and_store_priority_component_files(TESTS_DIR, OUTPUT_FOLDER)






