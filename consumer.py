from pyspark.sql import SparkSession
import rasterio
import numpy as np

# Initialize Spark session
spark = SparkSession.builder \
    .appName('Sentinel2TIFFProcessing') \
    .getOrCreate()

# Kafka configuration
KAFKA_BOOTSTRAP_SERVERS = 'localhost:9092'
KAFKA_TOPIC = 'sentinel_tiff_files'

# Read from Kafka
kafka_df = spark.readStream \
    .format('kafka') \
    .option('kafka.bootstrap.servers', KAFKA_BOOTSTRAP_SERVERS) \
    .option('subscribe', KAFKA_TOPIC) \
    .load()

# Define processing function to calculate NDVI
def process_tiff(file_path):
    with rasterio.open(file_path) as src:
        # Read Red and NIR bands
        red_band = src.read(4)  # Band 4 for Red
        nir_band = src.read(8)  # Band 8 for NIR

        # Calculate NDVI
        ndvi = (nir_band.astype(float) - red_band.astype(float)) / (nir_band + red_band)

        # Handle any potential division by zero
        ndvi[np.isnan(ndvi)] = 0  # Set NaN to 0 or any other value based on your needs

        # Save NDVI as a new TIFF file
        output_file = file_path.replace('.tiff', '_ndvi.tiff')
        with rasterio.open(output_file, 'w', driver='GTiff',
                           height=ndvi.shape[0], width=ndvi.shape[1],
                           count=1, dtype=ndvi.dtype,
                           crs=src.crs, transform=src.transform) as dst:
            dst.write(ndvi, 1)

        print(f'Processed {file_path} and saved NDVI to {output_file}')

# Process each file path
def foreach_batch_function(df, epoch_id):
    for row in df.collect():
        file_path = row['value'].decode('utf-8')
        process_tiff(file_path)

# Write the streaming DataFrame to process each batch
query = kafka_df \
    .writeStream \
    .foreachBatch(foreach_batch_function) \
    .start()

query.awaitTermination()
