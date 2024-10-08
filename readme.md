
# Sentinel-2 TIFF Processing Pipeline

This repository contains a Kafka and PySpark pipeline for processing Sentinel-2 TIFF files and calculating the Normalized Difference Vegetation Index (NDVI). The pipeline reads TIFF files, calculates NDVI, and saves the results as new TIFF files.

## Overview

- **Kafka Producer**: Monitors a specified directory for TIFF files and sends their paths to a Kafka topic.
- **Kafka Consumer**: Reads file paths from the Kafka topic, processes each TIFF file to calculate NDVI, and saves the result as a new TIFF file.

## Prerequisites

- Apache Kafka (installed and running)
- Apache Spark with PySpark (installed)
- Python 3.x with the following libraries:
    - `kafka-python`
    - `pyspark`
    - `rasterio`
    - `numpy`

## Setup Instructions

1. **Clone the Repository**:

     ```bash
     git clone <repository-url>
     cd <repository-name>
     ```

2. **Install Required Python Libraries**:

     ```bash
     pip install kafka-python pyspark rasterio numpy
     ```

3. **Configure Kafka**:

     Ensure that Kafka is running and create the topic for file paths:

     ```bash
     kafka-topics.sh --create --topic sentinel_tiff_files --bootstrap-server localhost:9092 --partitions 1 --replication-factor 1
     ```

4. **Set Up the Producer**:

     Open the `kafka_producer.py` file and modify the `tiff_directory` variable to point to the directory containing your Sentinel-2 TIFF files.

5. **Run the Kafka Producer**:

     Execute the producer script to start sending file paths to Kafka:

     ```bash
     python producer.py
     ```

6. **Run the Kafka Consumer**:

     Open the `kafka_consumer.py` file. No modifications are needed unless you want to change configurations. Execute the consumer script to start processing TIFF files:

     ```bash
     python consumer.py
     ```

## Code Structure

- `kafka_producer.py`: The script that reads TIFF files from a directory and sends their paths to a Kafka topic.
- `kafka_consumer.py`: The script that consumes file paths from Kafka, reads the TIFF files, calculates NDVI, and saves the result as a new TIFF file.

## NDVI Calculation

NDVI is calculated using the formula:

\[ \text{NDVI} = \frac{(\text{NIR} - \text{Red})}{(\text{NIR} + \text{Red})} \]

- **NIR**: Near-Infrared band (Band 8)
- **Red**: Red band (Band 4)

## Output

The processed NDVI results are saved in the same directory as the input TIFF files with the suffix `_ndvi.tiff`.

## Troubleshooting

- Ensure that your Kafka broker is running and that you have created the necessary topic.
- Check that the paths to the TIFF files are correctly set.
- If you encounter issues, check the console output for errors and adjust the logging as needed.