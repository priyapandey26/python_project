import os
import re
from collections import defaultdict

# Function to create output folder if it doesn't exist
def create_output_folder(folder):
    if not os.path.exists(folder):
        os.makedirs(folder)

# Function to save pass content to a file
def save_pass_content(pass_name, content, occurrence, folder):
    # Clean pass name to use in filename
    safe_pass_name = re.sub(r'[^a-zA-Z0-9_-]', '_', pass_name.strip())
    filename = f"{safe_pass_name}_{occurrence}.txt"
    file_path = os.path.join(folder, filename)
    with open(file_path, 'w') as f:
        f.write(content)

# Function to save pass summary
def save_summary(pass_occurrences, folder):
    summary_file = os.path.join(folder, 'pass_summary.txt')
    with open(summary_file, 'w') as f:
        for pass_name, count in pass_occurrences.items():
            f.write(f"{pass_name}: {count} occurrence(s)\n")

# Main function to process the LLVM IR file and extract passes
def process_llvm_ir(file_path, output_folder):
    create_output_folder(output_folder)

    pass_occurrences = defaultdict(int)  # Dictionary to track occurrences of each pass
    current_pass_name = None
    pass_content = []
    
    with open(file_path, 'r') as file:
        for line in file:
            # Check if the line indicates the start of a new pass
            match = re.match(r'^\*\*\* IR Dump After (.+) \*\*\*$', line)
            if match:
                # If there was a previous pass, save its content
                if current_pass_name and pass_content:
                    pass_occurrences[current_pass_name] += 1
                    save_pass_content(current_pass_name, ''.join(pass_content), pass_occurrences[current_pass_name], output_folder)
                    pass_content = []  # Reset content list for the new pass
                
                # Start collecting for the new pass
                current_pass_name = match.group(1).strip()
            else:
                # If we're in a pass, collect the content
                if current_pass_name:
                    pass_content.append(line)
        
        # Save the last pass content if any
        if current_pass_name and pass_content:
            pass_occurrences[current_pass_name] += 1
            save_pass_content(current_pass_name, ''.join(pass_content), pass_occurrences[current_pass_name], output_folder)
    
    # Save the summary of pass occurrences
    save_summary(pass_occurrences, output_folder)

if __name__ == "__main__":
    # Path to the LLVM IR file
    input_file = 'hello.ll'  # Replace this with the actual file path

    # Output folder to store the passes
    output_folder = 'passes'

    # Process the LLVM IR file and extract passes
    process_llvm_ir(input_file, output_folder)
