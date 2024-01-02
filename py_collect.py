import os

def gather_python_scripts(directory):
    python_scripts_content = ""
    for filename in os.listdir(directory):
        if filename.endswith(".py"):
            with open(os.path.join(directory, filename), 'r') as file:
                python_scripts_content += f"---{filename}---\n"
                python_scripts_content += file.read()
                python_scripts_content += "\n\n"
    with open(os.path.join(directory, "all_python_scripts.txt"), 'w') as output_file:
        output_file.write(python_scripts_content)

# Run the function in the current directory
gather_python_scripts('.')
