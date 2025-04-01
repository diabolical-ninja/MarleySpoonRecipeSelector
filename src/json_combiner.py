import glob
import json
import os
import sys


def combine_json_files(directory_path, output_file):
    """
    Combine all JSON files in the specified directory into a single JSON array
    and save to the output file.

    Args:
        directory_path: Path to the directory containing JSON files
        output_file: Path to the output file where combined JSON will be saved
    """
    # Check if directory exists
    if not os.path.exists(directory_path):
        print(f"Error: Directory '{directory_path}' not found.")
        return False

    # Find all JSON files in the directory
    json_files = glob.glob(os.path.join(directory_path, "*.json"))

    if not json_files:
        print(f"No JSON files found in '{directory_path}'.")
        return False

    # List to store all JSON objects
    combined_data = []

    # Process each JSON file
    for json_file in json_files:
        file_name = os.path.basename(json_file)
        print(f"Processing {file_name}...")

        try:
            # Read JSON file
            with open(json_file, "r", encoding="utf-8") as f:
                data = json.load(f)
                combined_data.append(data)
        except json.JSONDecodeError:
            print(f"Error: '{file_name}' is not a valid JSON file. Skipping.")
        except Exception as e:
            print(f"Error processing '{file_name}': {str(e)}. Skipping.")

    # Write combined data to output file
    try:
        with open(output_file, "w", encoding="utf-8") as f:
            json.dump(combined_data, f, indent=2)
        print(
            f"\nSuccessfully combined {len(combined_data)} JSON files into '{output_file}'."
        )
        return True
    except Exception as e:
        print(f"Error writing to output file: {str(e)}")
        return False


def main():
    # Check command line arguments
    if len(sys.argv) < 2:
        print("Usage: python json_combiner.py <directory_path> [output_file]")
        print("  <directory_path>: Path to the directory containing JSON files")
        print(
            "  [output_file]: (Optional) Path to the output file, defaults to 'combined.json'"
        )
        sys.exit(1)

    directory_path = sys.argv[1]
    output_file = sys.argv[2] if len(sys.argv) > 2 else "combined.json"

    combine_json_files(directory_path, output_file)


if __name__ == "__main__":
    main()
