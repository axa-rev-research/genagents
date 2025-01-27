import os
import json

def load_json_file(file_path):
    with open(file_path, 'r') as file:
        data = json.load(file)
    return data

def scan_folders(base_folder, variable_name, variable_values):
    matching_folders = []

    # List subfolders in the given base folder
    subfolders = [f.path for f in os.scandir(base_folder) if f.is_dir()]

    # Iterate over each subfolder
    for subfolder in subfolders:
        scratch_file_path = os.path.join(subfolder, 'scratch.json')
        
        # Check if scratch.json exists in the subfolder
        if os.path.exists(scratch_file_path):
            # Load the JSON file
            data = load_json_file(scratch_file_path)
            
            # Check if the variable exists and has one of the specified values
            if variable_name in data and data[variable_name] in variable_values:
                matching_folders.append(subfolder)

    return matching_folders

if __name__ == "__main__":
    # Example usage
    base_folder = './agent_bank/populations/gss_agents'
    variable_name = 'age'
    #variable_values = ['742 Evergreen Terrace']
    # generate a list of values betweeh 50 and 75 included
    variable_values = [i for i in range(50, 76)]

    matching_folders = scan_folders(base_folder, variable_name, variable_values)
    # Print how many folders have been found
    print("Folders with matching variable values:")

    for folder in matching_folders:
        print(folder)

    print(f"Found {len(matching_folders)} folders with matching variable values.")