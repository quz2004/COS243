# df2sqlite.py

import sqlite3
import pandas as pd
import logging
from create_course_dataframe import create_course_dataframe, process_xlsx

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[logging.StreamHandler()]
)

def save_to_sqlite(df, database_name='courses.db', table_name='courses'):
    """
    Save DataFrame to SQLite Database
    """
    try:
        logging.info(f"Connecting to database: {database_name}")
        conn = sqlite3.connect(database_name)
        
        logging.info(f"Saving DataFrame to table: {table_name}")
        df.to_sql(table_name, conn, if_exists='replace', index=False)
        
        logging.info("Data successfully saved to SQLite database")
        
        # Verify the data
        row_count = pd.read_sql(f"SELECT COUNT(*) FROM {table_name}", conn).iloc[0,0]
        logging.info(f"Verified {row_count} rows in table {table_name}")
        
        conn.close()
        return True
        
    except Exception as e:
        logging.error(f"Error saving to database: {str(e)}")
        return False

if __name__ == "__main__":
    # Load and process XLSX file
    file_path = "FTCM_Course List_Spring2025.xlsx"
    result = process_xlsx(file_path)

    if result:
        column_names, department_program_courses = result
        
        cleaned_column_names = ['Course Code', 'Course Title', 'Cr', 'Prereq(s)', 
                              'Instructor ', 'Major/ GE/ \nElective', 'Format', 
                              'Mon', 'MonTo', 'Tue', 'TueTo', 'Wed', 'WedTo', 
                              'Thu', 'ThuTo', 'Fri', 'FriTo', 'Sat', 'SatTo', 
                              'Platform', 'New/ Repeat', 'Room']
        
        # Create DataFrame
        df = create_course_dataframe(cleaned_column_names, column_names, department_program_courses)
        
        # Save to SQLite
        if save_to_sqlite(df):
            logging.info("Process completed successfully")
        else:
            logging.error("Failed to save data to SQLite")
    else:
        logging.error("Failed to process XLSX file")