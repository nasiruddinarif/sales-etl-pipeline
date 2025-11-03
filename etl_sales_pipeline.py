# ********************************
#   IMPORT LIBRARIES
# ********************************
import pandas as pd
import datetime
import logging
import time
# ********************************
#   SETUP LOGGING
# ********************************
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)
# ********************************
#   CREATE CSV FILE
# ********************************

# Create a simple DataFrame
data = {
    'Date' : ['2024-01-01', '2024-01-02', '2024-01-03'],
    'Store' : ['KL', 'Penang', 'KL'],
    'Product' : ['Chocolate', 'Almond', 'Cornflake'],
    'Sales' : [120, None, 200],
    'Quantity' : [5, 3, None]
}

df = pd.DataFrame(data)

# Save to csv on my desktop
df.to_csv(r'C:\Users\Admin\Desktop\sales_data.csv', index=False)

# ********************************
#   EXTRACT FUNCTION
# ********************************

def extract(file_path):
    # Extract data from CSV file
    try:
        data = pd.read_csv(file_path)
        logging.info("✅ Data extracted successfully.")
        return data
    except Exception as e:
        logging.error(f"❌ Extraction failed: {e}")
        raise

# ********************************
#   TRANSFORM FUNCTION
# ********************************
def transform(data):
    try:
        # Fill missing numerical value with 0
        data['Sales'] = data['Sales'].fillna(0)
        data['Quantity'] = data['Quantity'].fillna(0)

        # Rename column
        data = data.rename(columns={'Store': 'Store_Location'})

        # Add a new calculated column
        data['Total_Value'] = data['Sales'] * data['Quantity']

        # Sort by sales descending
        data = data.sort_values(by='Sales', ascending=False)

        # lowercase all column name
        data.columns = data.columns.str.lower()

        logging.info("✅ Data Transformed Successfully!")
        logging.info(f"Data Summary: {data.shape[0]} rows, {data.shape[1]} columns.")
        logging.info(f"Columns: {list(data.columns)}")
        return data
    except Exception as e:
        logging.error(f"❌ Transformation failed: {e}")
        raise

def validate(data):
    if data['sales'].lt(0).any():
        logging.warning("⚠️ Some sales values are negative!")
    if data.isnull().any().any():
        logging.warning("⚠️ Missing values still exist!")

# ********************************
#   LOAD FUNCTION
# ********************************
def load(data, output_folder, mode="replace"):
    # Save clean data to CSV with timestamp
    try:
        import os
        os.makedirs(output_folder, exist_ok=True)

        timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        output_path = fr"{output_folder}\clean_sales_{timestamp}.csv"
        data.to_csv(output_path, index=False)
        logging.info(f"✅ Data loaded successfully at: {output_path}")
        return output_path
    except Exception as e:
        logging.error(f"❌ Loading failed: {e}")
        raise

# ********************************
#   MAIN PIPELINE FUNCTION
# ********************************
def run_etl():
    # Run the full ETL pipeline.
    input_path = r"D:\Data Engineer Portfolio\Sales pipeline\sales_data.csv"
    output_folder = r"D:\Data Engineer Portfolio\Sales pipeline"
   
    start_time = time.time()
    logging.info("🚀 Starting ETL pipeline...")

    # Extract
    raw_data = extract(input_path)

    # Transform
    clean_data = transform(raw_data)

    # Validate
    validate(clean_data)

    # Load
    load(clean_data, output_folder, mode="replace")

    duration = round(time.time() - start_time, 2)
    logging.info("🎉 ETL pipeline completed successfully!")
    logging.info(f"🎉 ETL completed in {duration} seconds.")

# ********************************
#   EXECUTE
# ********************************
if __name__ == "__main__":
    run_etl()