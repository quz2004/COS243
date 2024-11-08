import csv
import logging
import re
from openpyxl import load_workbook

# Debug Mode (Set to False for production)
DEBUG_MODE = True

# Logging Configuration
logging.basicConfig(
    level=logging.DEBUG if DEBUG_MODE else logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[
        logging.FileHandler("debug.log"),
        logging.StreamHandler()
    ]
)

def process_xlsx(file_path):
    logging.info(f"Processing XLSX file: {file_path}")
    
    try:
        # Load XLSX content
        wb = load_workbook(filename=file_path)
        sheet = wb.active
        xlsx_content = [[cell.value for cell in row] for row in sheet.rows]
        
        # Initialization
        column_names = []
        department_program_courses = {}
        current_department = None
        current_program = None
        
        # Determine column indices
        header_index = 0
        while header_index < len(xlsx_content):
            if "Course Code" in [x for x in xlsx_content[header_index] if x]:
                break
            header_index += 1
        column_names = xlsx_content[header_index]
        cr_index = [i for i, x in enumerate(column_names) if re.match(r"Cr", str(x))]
        if not cr_index:
            logging.error("Could not find 'Cr' column index.")
            return None
        cr_index = cr_index[0]
        
        # Process rows
        for index, row in enumerate(xlsx_content):
            if index <= header_index:
                continue
            
            # Department Row Detection (Loose pattern for "Cr")
            if row[0] and row[cr_index] and re.match(r"cr", str(row[cr_index]), re.IGNORECASE):
                current_department = row[0]
                department_program_courses.setdefault(current_department, {})
                current_program = None
                logging.debug(f"Detected Department: {current_department}")
            
            # Program Row Detection (Empty "Cr" column)
            elif row[0] and not row[cr_index]:
                current_program = row[0]
                department_program_courses[current_department].setdefault(current_program, [])
                logging.debug(f"Detected Program under {current_department}: {current_program}")
            
            # Course Row Detection (Numeric "Cr" value)
            elif row[0] and isinstance(row[cr_index], (int, float)):
                course_codes = [row[0]]  # Default to single course code
                if "/" in row[0]:  # Handle special case (e.g., "STA421/521")
                    start, end = row[0].split("/")
                    course_codes = [start, start[:3] + end]
                    logging.info(f"Splitting course for row: {repr(row)}")
                    logging.info(f"course_codes: {course_codes}")

                for code in course_codes:
                    new_row = row[:]  # Copy original row
                    new_row[0] = code  # Update course code for each split course

                    # Assign courses to program if exists, otherwise directly to department
                    if current_program:
                        department_program_courses[current_department][current_program].append(new_row)
                    else:
                        department_program_courses[current_department].setdefault(current_department, []).append(new_row)
                logging.debug(f"Added Course(s) {course_codes} under {current_program or 'directly in department'} in {current_department}")
            
            elif row[0]:
                logging.info(f"Skipping row: {repr(row)}")
        
        return (column_names, department_program_courses)
    
    except Exception as e:
        logging.error(f"An error occurred: {str(e)}")
        return None

if __name__ == "__main__":
    file_path = "FTCM_Course List_Spring2025.xlsx"
    result = process_xlsx(file_path)
    
    if result:
        column_names, department_program_courses = result
        print("Column Names:")
        print(column_names)
        print("\nDepartment, Program, Courses:")
        for department, programs in department_program_courses.items():
            print(f"**{department}**")
            for program, courses in programs.items():
                print(f"  *{program}")
                for course in courses:
                    print(f"    - {course}")
    else:
        print("No result returned. Check debug.log for errors.")
