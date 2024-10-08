from kafka import KafkaProducer
import os
import time

# Kafka configuration
KAFKA_TOPIC = 'sentinel_tiff_files'
KAFKA_BOOTSTRAP_SERVERS = 'localhost:9092'

# Initialize Kafka producer
producer = KafkaProducer(bootstrap_servers=KAFKA_BOOTSTRAP_SERVERS)

# Path to the directory containing TIFF files
tiff_directory = '/path/to/tiff/files'

# Produce messages for each TIFF file
while True:
    for filename in os.listdir(tiff_directory):
        if filename.endswith('.tiff') or filename.endswith('.tif'):
            file_path = os.path.join(tiff_directory, filename)
            producer.send(KAFKA_TOPIC, value=file_path.encode('utf-8'))
            print(f'Sent: {file_path}')
    time.sleep(10)  # Adjust the sleep time as needed
