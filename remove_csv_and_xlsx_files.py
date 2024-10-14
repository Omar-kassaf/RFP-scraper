import os

def remove_csv_and_xlsx_files():
    """Remove all CSV and Excel files from the current working directory."""
    directory = os.getcwd()

    # Remove the original CSV files
    for filename in os.listdir(directory):
        if filename.endswith('.csv'):
            os.remove(os.path.join(directory, filename))
            print(f"Removed: {filename}")

    # Remove the original Excel files
    for filename in os.listdir(directory):
        if filename.endswith('.xlsx'):
            os.remove(os.path.join(directory, filename))
            print(f"Removed: {filename}")