"""
Example usage of the ScanDB class
"""

from scan_db import ScanDB
from datetime import datetime


def main():
    # Initialize database connection
    scan_db = ScanDB()

    # Example: Insert a new scan
    patient_id = "PAT123"  # This should be an ID that exists in your patient table
    scan_datetime = datetime.now()
    consent_given = True
    image_path = "/path/to/scan/image.jpg"
    physician_id = 1  # This should be an ID that exists in your physician table

    scan_id = scan_db.insert_scan(
        patient_id=patient_id,
        scan_datetime=scan_datetime,
        consent_given=consent_given,
        image_path=image_path,
        referring_physician_id=physician_id,
    )

    if scan_id:
        print(f"Scan record inserted with ID: {scan_id}")

        # Retrieve the inserted scan
        scan = scan_db.get_scan_by_id(scan_id)
        if scan:
            print(f"Retrieved scan: {scan}")

        # Get all scans for this patient
        patient_scans = scan_db.get_scans_by_patient_id(patient_id)
        print(f"Found {len(patient_scans)} scans for patient {patient_id}")
    else:
        print("Failed to insert scan record")


if __name__ == "__main__":
    main()
