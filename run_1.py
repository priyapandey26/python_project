import csv

# File paths
input_file_path = 'out'  # Update this to your actual input file path
output_csv_path = 'output.csv'  # Update this to your desired output file path

# Initialize variables
total_tests = None
unsupported = None
passed = None
expectedly_failed = None
test_results = []

# Read the input file and parse necessary data
with open(input_file_path, 'r') as infile:
    lines = infile.readlines()

# Process each line to extract test results and stats
for line in lines:
    # Check for lines with PASS, UNSUPPORTED, or FAIL status
    if line.startswith("PASS:") or line.startswith("UNSUPPORTED:") or line.startswith("FAIL:") or line.startswith("XFAIL:"):
        parts = line.split(' ')
        # Extract full path and status
        status = parts[0].replace(":", "")
        full_path = parts[3]
        
        # Split the path to get the directory path and the filename separately
        path_parts = full_path.rsplit('/', 1)
        if len(path_parts) == 2:
            file_path, filename = path_parts[0] + '/', path_parts[1]
        else:
            file_path, filename = '', full_path  # If no '/' found, the path is just the filename

        # Store the result
        test_results.append([filename, status, file_path])

    # Extract total tests and stats
    if "Total Discovered Tests:" in line:
        total_tests = line.split(':')[-1].strip()
    if "Unsupported" in line:
        unsupported = line.split(':')[-1].split('(')[0].strip()
    if "Passed" in line:
        passed = line.split(':')[-1].split('(')[0].strip()
    if "Expectedly Failed" in line:
        expectedly_failed = line.split(':')[-1].split('(')[0].strip()

# Write to CSV
with open(output_csv_path, 'w', newline='') as csvfile:
    writer = csv.writer(csvfile)
    
    # Write header
    writer.writerow(["Filename", "Status", "PATH"])
    
    # Write the parsed filename, status, and path for each test
    for result in test_results:
        writer.writerow(result)
    
    # Write the summary at the end
    writer.writerow([])
    writer.writerow(["Total Discovered Tests:", total_tests])
    writer.writerow(["Unsupported:", f"{unsupported} ({float(unsupported)/int(total_tests) * 100:.2f}%)"])
    writer.writerow(["Passed:", f"{passed} ({float(passed)/int(total_tests) * 100:.2f}%)"])
    writer.writerow(["Expectedly Failed:", f"{expectedly_failed} ({float(expectedly_failed)/int(total_tests) * 100:.2f}%)"])

print(f"CSV written to {output_csv_path}")
