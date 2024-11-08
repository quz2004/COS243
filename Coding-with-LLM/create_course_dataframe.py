from process_xlsx import process_xlsx

import pandas as pd
import re

# Step 1: Convert to DataFrame
def create_course_dataframe(cleaned_column_names, column_names, department_program_courses):
    data = []
    for department, programs in department_program_courses.items():
        for program, courses in programs.items():
            for course in courses:
                row_data = course[:]  # Copy original row
                row_data.append(department)  # Add Department column
                row_data.append(program if program else "N/A")  # Add Program column
                data.append(row_data)
    
    # Add Department and Program to the column names
    extended_column_names = column_names + ["Department", "Program"]
    
    # Create DataFrame
    df = pd.DataFrame(data, columns=extended_column_names)
    # Select columns based on cleaned_column_names
    df = df[cleaned_column_names]

    # strip trailing spaces from column names
    df.columns = df.columns.str.strip()

    return df

# Step 2: Diagnose Inconsistencies in Data
def diagnose_inconsistencies(df):
    # Report missing values
    missing_values = df.isnull().sum()
    print("\nMissing Values Per Column:")
    print(missing_values[missing_values > 0])
    
    # Check unique value counts to spot potential inconsistencies
    print("\nUnique Value Counts Per Column:")
    for column in df.columns:
        unique_vals = df[column].nunique()
        print(f"{column}: {unique_vals} unique values")
    
    # Identify potential misspellings and inconsistent values in key columns
    # Example: Checking for inconsistencies in 'Course Code', 'Instructor', 'Room', etc.
    print("\nInconsistent Patterns and Values:")
    
    # Pattern checks for Course Code (e.g., expecting format like 'MAT101', 'STA421/521')
    inconsistent_course_codes = df[~df['Course Code'].str.match(r'^[A-Z]{3}\d{3}(/\d{3})?$')]
    if not inconsistent_course_codes.empty:
        print("\nInconsistent Course Codes:")
        print(inconsistent_course_codes[['Course Code']].drop_duplicates())
    
    # Check for inconsistent capitalization in 'Instructor' column
    df['Instructor'] = df['Instructor'].str.strip().str.title()
    instructor_inconsistencies = df['Instructor'].value_counts()
    print("\nInstructor Inconsistencies:")
    print(instructor_inconsistencies[instructor_inconsistencies > 1])
    
    # Check for possible misspellings or variations in Room
    print("\nRoom Variations:")
    room_variations = df['Room'].value_counts()
    print(room_variations[room_variations > 1])
    
    # Identify rows with missing key fields that should generally be non-null
    key_columns = ['Course Code', 'Course Title', 'Cr', 'Instructor']
    missing_key_fields = df[df[key_columns].isnull().any(axis=1)]
    if not missing_key_fields.empty:
        print("\nRows with Missing Key Fields:")
        print(missing_key_fields[key_columns])
    
    # Display data types and any anomalies in numeric fields
    print("\nData Types and Anomalies in Numeric Fields:")
    for column in df.select_dtypes(include=['number']).columns:
        print(f"{column} - Min: {df[column].min()}, Max: {df[column].max()}, Unique Values: {df[column].nunique()}")
    
    return df


file_path = "COS243/Coding-with-LLM/FTCM_Course List_Spring2025.xlsx"
result = process_xlsx(file_path)
    
if result:
    column_names, department_program_courses = result
    print(f"Column Names:{column_names}") 
else:
    print(f"Error processing file. {file_path}")
'Instructor', 'Major/ GE/ \nElective', 'Format', 'Mon', 'MonTo',
cleaned_column_names = ['Course Code', 'Course Title', 'Cr', 'Prereq(s)', 
'Instructor ', 'Major/ GE/ \nElective', 'Format', 'Mon', 'MonTo',
 'Tue', 'TueTo', 'Wed', 'WedTo', 'Thu', 'ThuTo', 
'Fri', 'FriTo', 'Sat', 'SatTo', 'Platform', 'New/ Repeat', 'Room']

# Sample usage
# Assuming column_names and department_program_courses are already defined
df = create_course_dataframe(cleaned_column_names, column_names, department_program_courses)
df_cleaned = diagnose_inconsistencies(df)
diagnose_inconsistencies(df_cleaned)
"""
This implementaation has problems, please fix them:
1. In `create_course_dataframe`  Function signature should be `def create_course_dataframe(cleaned_column_names, column_names, department_program_courses):` and the function should create `df` and then use `cleaned_column_names` to select the columns in the dataframe
2. instructor column has a trailing space, it should be removed
"""