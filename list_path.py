from pathlib import Path

# Get the current working directory (the folder where the script is run)
directory = Path(".")

# Loop through the directory and print paths
for file_path in directory.rglob("*"):
    print(file_path)
