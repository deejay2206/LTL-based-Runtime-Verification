import os
import sys
import pandas as pd
import csv

def fetch_rows_before_label(csv_file, label_value, n):
    # Read the CSV file into a pandas DataFrame
    df = pd.read_csv(csv_file)

    fetched_instance_paths = []

    # Find indices where 'ATT_FLAG' is equal to the specified label_value
    label_indices = df.index[df['ATT_FLAG'] == label_value]

    # Create the 'Output' folder if it doesn't exist
    output_folder = "Output"
    os.makedirs(output_folder, exist_ok=True)

    for i, index in enumerate(label_indices):
        start_index = max(0, index - n)
        end_index = index
        instance = df.iloc[start_index:end_index + 1]  # Include the label row

        # Save the instance to a temporary CSV file
        instance_filename = os.path.join(output_folder, f"inst_{i}.csv")
        instance.to_csv(instance_filename, index=False)
        fetched_instance_paths.append(instance_filename)

    return fetched_instance_paths

def process_csv_file(instance_file):
    os.system("python3 runtime_monitor.py -i 45")
    with open(instance_file, "r") as f:
        #print(instance_file)
        data = csv.reader(f)
        next(data, None)  # skip the headers

        for row in data:
            ints = [round(float(s)) for s in row]
            #print(ints)
            cmd_args = " ".join(map(str, ints[:45]))
            os.system(f"python3 runtime_monitor.py -a {cmd_args}")

def main():
    if len(sys.argv) != 5:
        print("Usage: python3 script.py csv_file label_value n property_csp")
        sys.exit(1)

    csv_file = sys.argv[1]
    label_value = int(sys.argv[2])
    n = int(sys.argv[3])
    property_csp = sys.argv[4]

    fetched_instance_paths = fetch_rows_before_label(csv_file, label_value, n)

    for instance_path in fetched_instance_paths:
        process_csv_file(instance_path)

    os.system(f"python3 runtime_monitor.py -c -p {property_csp}")

if __name__ == "__main__":
    main()
