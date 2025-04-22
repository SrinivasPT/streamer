import os
import time
import re
import threading
from dotenv import load_dotenv

from classifier import predict_image_file
from wss_server import sync_alert_generator, start_server
from scan_db import ScanDB

# Load environment variables from .env file
load_dotenv()


def process_files(input_folder, num_iterations=None):
    # Check if the input folder exists
    if not os.path.exists(input_folder):
        print(f"Error: Input folder '{input_folder}' does not exist.")
        return

    # Get all files from the input folder
    files = [
        f
        for f in os.listdir(input_folder)
        if os.path.isfile(os.path.join(input_folder, f))
    ]

    # Sort the file names numerically based on the number after the underscore
    def extract_number(filename):
        # Look for pattern _123_ in filename
        match = re.search(r"(\d+)_", filename)
        if match:
            return int(match.group(1))
        return 0

    files.sort(key=extract_number)

    if not files:
        print(f"No files found in '{input_folder}'")
        return

    # If num_iterations is None, run indefinitely
    iteration = 0
    while num_iterations is None or iteration < num_iterations:
        if num_iterations is not None:
            print(f"\nIteration {iteration + 1}:")
        else:
            print(f"\nIteration {iteration + 1} (continuous mode):")

        # Loop through each file
        for file_name in files:
            time.sleep(2)
            file_path = os.path.join(input_folder, file_name)
            print(f"Processing file: {file_name}")

            # Call the classifier on the file
            try:
                result = predict_image_file(file_path)
                print(f"Classification result: {result}")

                if result == "Paralysis":
                    sync_alert_generator(file_name)  # Send alert via WebSocket

                store_in_db(
                    file_name, result
                )  # Store in database (function to be implemented)

            except Exception as e:
                print(f"Error classifying {file_name}: {e}")

        iteration += 1

        # If running indefinitely, add a small delay between iterations
        if num_iterations is None:
            time.sleep(5)


def store_in_db(file_name, result):
    """Store the scan result in the database"""
    try:
        # Extract patient ID from the filename (format: patientid_gender_name.jpg)
        match = re.search(r"^(\d+)_", file_name)
        patient_id = match.group(1) if match else "unknown"
        scan_result = "positive" if result == "Paralysis" else "negative"

        # Create a database connection
        db = ScanDB()

        # Store the scan record
        image_path = os.path.join(os.getenv("INPUT_FOLDER_PATH"), file_name)
        scan_id = db.insert_scan(
            patient_id=patient_id,
            consent_given=True,  # Assuming consent is given
            image_path=image_path,
            scan_result=scan_result,
        )

        if scan_id:
            print(f"Scan record stored in database with ID: {scan_id}")
        else:
            print("Failed to store scan record in database")
    except Exception as e:
        print(f"Error storing scan in database: {e}")


if __name__ == "__main__":
    # Get the input folder path from environment variables
    input_folder = os.getenv("INPUT_FOLDER_PATH")

    # Start the WebSocket server in a separate thread
    server_thread = threading.Thread(
        target=start_server,
        daemon=True,  # This makes the thread exit when the main program exits
    )
    server_thread.start()
    print("WebSocket server started in background")

    # Wait a moment for the server to initialize
    time.sleep(1)

    # Choose the mode:

    # For finite iterations:
    process_files(input_folder, 2)

    # For continuous processing (uncomment this and comment the line above):
    # process_files(input_folder, None)  # None means run indefinitely

    # Keep the main thread alive if you want to prevent the program from exiting
    # This is needed only if you're running in continuous mode
    # while server_thread.is_alive():
    #     time.sleep(1)
