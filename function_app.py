import logging
import datetime
from azure.storage.blob import BlobServiceClient
import azure.functions as func

app = func.FunctionApp()

connection_string = "DefaultEndpointsProtocol=https;AccountName=backupdatatemp;AccountKey=y6jiVeA3X/Lqj2MPIVPAUnrYrg0P3OOcP5cSW8s4Okm27ZlrNPgrrFpBQO91VQw7xxIJ7gLIO6Af+AStGAVZzg==;EndpointSuffix=core.windows.net"
container_name = "sensor-backups"
blob_service_client = BlobServiceClient.from_connection_string(connection_string)
container_client = blob_service_client.get_container_client(container_name)

@app.timer_trigger(schedule="0 0 0 * * *", arg_name="myTimer", run_on_startup=False, use_monitor=False)
def backup_trigger(myTimer: func.TimerRequest) -> None:
    if myTimer.past_due:
        logging.info('The timer is past due!')

    logging.info('Python timer trigger function executed.')

    timestamp = datetime.datetime.now(datetime.timezone.utc).strftime("%Y%m%d%H%M%S")
    blob_name = f"sensor_data_backup_{timestamp}.json"

    sensor_data = '{"temperature": 25, "humidity": 60}'

    try:
        # Upload sensor data as a blob in Azure Blob Storage
        blob_client = container_client.get_blob_client(blob_name)
        blob_client.upload_blob(sensor_data)
        logging.info(f"Backup successful: {blob_name}")
    except Exception as e:
        logging.error(f"Failed to backup data: {str(e)}")
