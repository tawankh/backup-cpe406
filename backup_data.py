from azure.storage.blob import BlobServiceClient
import datetime
import schedule
import time

# Azure Blob Storage connection setup
connection_string = "DefaultEndpointsProtocol=https;AccountName=backupdatatemp;AccountKey=y6jiVeA3X/Lqj2MPIVPAUnrYrg0P3OOcP5cSW8s4Okm27ZlrNPgrrFpBQO91VQw7xxIJ7gLIO6Af+AStGAVZzg==;EndpointSuffix=core.windows.net"

blob_service_client = BlobServiceClient.from_connection_string(connection_string)

container_name = "sensor-backups"
container_client = blob_service_client.get_container_client(container_name)

if not container_client.exists():
    container_client.create_container()

def backup_data(data: str, filename: str):
    """
    Backs up sensor data to Azure Blob Storage.
    Args:
        data (str): The data to be backed up (e.g., sensor data in JSON or CSV format).
        filename (str): Name of the file to save in the blob.
    """
    timestamp = datetime.datetime.now(datetime.timezone.utc).strftime("%Y%m%d%H%M%S")
    blob_name = f"{filename}_{timestamp}.json"
    
    blob_client = container_client.get_blob_client(blob_name)
    blob_client.upload_blob(data)
    print(f"Backup successful: {blob_name}")

def job():
    # Replace this with your sensor data fetching logic
    sensor_data = '{"temperature": 25, "humidity": 60}'
    backup_data(sensor_data, "sensor_data_backup")

# Schedule the job to run every day at a specific time (e.g., 10:00 AM)
schedule.every().day.at("10:00").do(job)

print("Scheduled task is running. Press Ctrl+C to exit.")
while True:
    schedule.run_pending()
    time.sleep(1)
