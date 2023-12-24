from importlib.metadata import packages_distributions
import sys
import subprocess
import os

def get_pip_list():
    try:
        # Run the pip list command
        result = subprocess.run(['pip', 'list'], capture_output=True, text=True, check=True)

        # Split the output into lines
        lines = result.stdout.strip().split('\n')

        # Create a 2D array to store the package information
        packages = [line.split() for line in lines[2:]]  # Starting from the third line to skip the header

        return packages
    except subprocess.CalledProcessError as e:
        print(f"Error: {e}")
        return None


def is_standard_library_module(module_name):
    return module_name in sys.modules

# read lines of a file
def read_file(filename, output_file):
    with open(filename, 'r') as f:
        for i in f:
            name = ""
            fail = True
            if "from" in i:
                word_after_from = i.split("from")[1].strip()
                name = word_after_from.split(" ")[0].strip()
                
            elif "import" in i:
                word_after_import = i.split("import")[1].strip()
                name = word_after_import.split(" ")[0].strip()


            if is_standard_library_module(name) and name != "":
                print(f"## {name} is part of the Python Standard Library.", file=output_file)
           
            elif name != "":
                try:
                    name = packages_distributions()[name][0]
                except:
                    print(f"#fail to get pip name for {name}", file=output_file)
                    fail = False
                pip_list = get_pip_list()   
                if(fail):  
                    for package in pip_list:
                        if name in package:
                            print(name + "==" + package[1], file=output_file)
                            break
                    else:
                        print(f"#fail to get version for {name}", file=output_file)

# Get the directory of the script
script_directory = os.path.dirname(os.path.abspath(__file__))

# Open the requirements.txt file for writing
output_file_path = os.path.join(script_directory, 'requirements.txt')
with open(output_file_path, 'w') as output_file:
    # Traverse the script directory and its subdirectories
    def traverse_directory(directory):
        for root, dirs, files in os.walk(directory):
            for file in files:
                if file.endswith(".py") and file != os.path.basename(__file__):
                    file_path = os.path.join(root, file)
                    read_file(file_path, output_file)

    # Use the script directory as the starting point for traversal
    traverse_directory(script_directory)

print(f"Requirements written to {output_file_path}")

def rearrange_alphabetically(file_path):
    # Read content from the file
    with open(file_path, 'r') as file:
        lines = file.readlines()

    # Sort the lines alphabetically
    sorted_lines = sorted(lines)

    # Write the sorted content back to the file
    with open(file_path, 'w') as file:
        file.writelines(sorted_lines)

# Example usage:
file_path = 'requirements.txt'  # Replace with the path to your file
rearrange_alphabetically(file_path)
