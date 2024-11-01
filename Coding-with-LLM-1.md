```python
csv = """
<csv start>
Fei Tian College - Middletown Spring 2025 Course Schedule (Last Updated 10/23/2024),,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,
1,2,3,4,5,,19,7,8,9,10,11,12,13,14,15,16,17,18,,6,20,,,,,,,,,,,,,
Course Code,Course Title,Cr,Prereq(s),Instructor ,"Major/ GE/ 
Elective",Format,Mon,MonTo,Tue,TueTo,Wed,WedTo,Thu,ThuTo,Fri,FriTo,Sat,SatTo,Platform,New/ Repeat,Room,Ref_Sem_Course,InPopuli,NumOfStu,Duration,DurInMin,CrMin/ Wk,Check Dur,,,,,,
,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,
Applied Math & Statistics,,Cr,Prereq(s),Instructor ,"Major/ GE/ 
Elective",Format,Mon,MonTo,Tue,TueTo,Wed,WedTo,Thu,ThuTo,Fri,FriTo,Sat,SatTo,Platform,New/ Repeat,Room,,,,Duration,DurationInMin,CrMin/Wk,Check,,,,,,
(Bachelor of Science),,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,
,,,,,,,,,,,,,,,,,,,,,,,,,0:00:00,0,0,,,,,,,
MAT106,Calculus II,4,MAT105,Michael Zhao,STA-Y1,Lecture,8:30 AM,9:40 AM,,,8:30 AM,9:40 AM,,,8:30 AM,9:30 AM,,,,,D323,Spring2024,,,3:20:00,200,200,,,,,,,
STA101,Introduction to Statistics,3,None,Michael Zhao,STA-Y1,Lecture,,,10:00 AM,11:15 AM,,,10:00 AM,11:15 AM,,,,,,,D323,Spring2024,,,2:30:00,150,150,,,,,,,
STA211,Statistical Theory and Methods,3,STA202,Kevin Ren,STA-Y2,Lecture,,,12:45 PM,2:00 PM,,,12:45 PM,2:00 PM,,,,,,,D421,Spring2024,,,2:30:00,150,150,,,,,,,
MAT207,Calculus III,3,MAT106,Qihu Zhang,STA-Y2,Lecture,,,,,8:30 AM,9:45 AM,,,8:30 AM,9:45 AM,,,,,,,,,2:30:00,150,150,,,,,,,
STA421/521,Design and Analysis of Experiments,3,STA211,Zhanglin Cui,STA-Y4,Lecture,,,4:00 PM,5:15 PM,,,4:00 PM,5:15 PM,,,,,,,D325,,,,2:30:00,150,150,,,,,,,
,,,,,,,,,,,,,,,,,,,,,,,,,0:00:00,0,0,,,,,,,
,,,,,,,,,,,,,,,,,,,,,,,,,0:00:00,0,0,,,,,,,
,,,,,,,,,,,,,,,,,,,,,,,,,0:00:00,0,0,,,,,,,
(Master of Science),,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,
,,,,,,,,,,,,,,,,,,,,,,,,,0:00:00,0,0,,,,,,,
STA512,Statistical Inference,3,STA502,Kevin Ren,AMS-MS,Lecture,,,12:45 PM,2:00 PM,,,12:45 PM,2:00 PM,,,,,,,D421,Spring2024,,,2:30:00,150,150,,,,,,,
STA421/521,Design and Analysis of Experiments,3,None,Zhanglin Cui,AMS-MS,Lecture,,,4:00 PM,5:15 PM,,,4:00 PM,5:15 PM,,,,,,,D325,Spring2024,,,2:30:00,150,150,,,,,,,
STA571,Advanced Statistical Computing,3,STA512,Kevin Ren,AMS-MS,Lecture,,,,,12:45 PM,2:00 PM,,,12:45 PM,2:00 PM,,,,,D421,,,,2:30:00,150,150,,,,,,,
STA751,Applied Statistics Project or Thesis,6,Dept. Approval,Varies,AMS-MS,IND STU,,,,,,,,,,,,,,,,,,,0:00:00,0,0,,,,,,,
,,,,,,,,,,,,,,,,,,,,,,,,,0:00:00,0,0,,,,,,,
,,,,,,,,,,,,,,,,,,,,,,,,,0:00:00,0,0,,,,,,,
,,,,,,,,,,,,,,,,,,,,,,,,,0:00:00,0,0,,,,,,,
<csv end>

"""
```

```python

prompt2 = """

Below are a few lines in csv from spreadsheet "FTCM_Course List_Spring2025.xlsx"

rows are like:
<row>
Applied Math & Statistics,,Cr,Prereq(s),Instructor <......>
</row>
are departments.

rows like 
<row>
(Bachelor of Science),,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,
</row>
are programs under the departments.

Otherwise rows like 
<row>
MAT106,Calculus II,4,MAT105,Michael Zhao,STA-Y1,Lecture,8:30 AM,9:40 AM,,,8:30 AM,9:40 AM,,,8:30 AM,9:30 AM,,,,,D323,Spring2024,,,3:20:00,200,200,,,,,,,
</row>
are courses.

one department can have multiple program sections, each program row is followed by course rows.

Please identify patterns and suggest your algorithm in plain language to read xlsx file  by rows and
1. get column names as list from row 3
2. extract department name
3. extract program name
4. get a list of rows as csv follow that program 
5. ignore other rows

output a tuple with column name in task 1 as list and a dictionary like:
{"<department name>" : {
"program1" :[list of course rows],
"program2" :[list of course rows]
}}

"""
```

```python
prompt3 = """

Now write complete python code with error logged in a file for debugging purposes if DEBUG mode is on.

Note: 
0. Since this is manually created file, always expect to have values being mixed case and misspelling etc.
1. one department can have multiple program sections, each program row is followed by course rows.
2. department row as "Cr" column with value "Cr" and 
3. program row has empty column for "Cr"
4. course row has integer value for "cr"
5. Use loose pattern to allow "Cr" spelled in different case.
6. Course code may have special case like "STA421/521", in which case we split into 2 courses, "STA421" and "STA521" and other fields for two courses are the same.



"""
```

## Code from LLM

```python

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
        cr_index = [i for i, x in enumerate(column_names) if re.match(r"cr", str(x), re.IGNORECASE)]
        if not cr_index:
            logging.error("Could not find 'Cr' column index.")
            raise IndexError("Could not find 'Cr' column index.")
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
            
            # Course Row Detection (Integer "Cr" value)
            elif row[0] and isinstance(row[cr_index], int):
                course_codes = [row[0]]  # Default to single course code
                if "/" in row[0]:  # Handle special case (e.g., "STA421/521")
                    start, end = row[0].split("/")
                    prefix = re.match(r"[A-Za-z]+", start).group()
                    course_codes = [f"{prefix}{i}" for i in range(int(start[len(prefix):]), int(end[len(prefix):]) + 1)]
                
                for code in course_codes:
                    new_row = row[:]  # Copy original row
                    new_row[0] = code  # Update course code for each split course
                    department_program_courses[current_department][current_program].append(new_row)
                logging.debug(f"Added Course(s) {course_codes} under {current_program} in {current_department}")
        
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


```

```python
prompt3 ="""

Convert the data into pandas dataframe `df`, set all fields as string, add new columns: Department and Program
We want to clean up the data: identify possible inconsistency in values, missspelling, missing field etc. 
Write a python program to process `df` to help diagnose possible inconsistency.

"""
```

## Use exception to catch error and detailed traceback info

```python
import traceback
import sys
import linecache

def print_context(filename, line_number, num_back=3):
    start = max(1, line_number - num_back)
    for i in range(start, line_number + 1):
        line = linecache.getline(filename, i).rstrip()
        print(f"{'>' if i == line_number else ' '} {i:4d} {line}")

def custom_traceback(exc_type, exc_value, tb, limit=3):
    traceback_lines = []
    traceback_lines.append("Traceback (most recent call last):\n")
    
    while tb and limit > 0:
        frame = tb.tb_frame
        filename = frame.f_code.co_filename
        line_number = tb.tb_lineno
        function_name = frame.f_code.co_name
        
        traceback_lines.append(f"  File \"{filename}\", line {line_number}, in {function_name}\n")
        traceback_lines.append("    Context:\n")
        
        context_lines = []
        print_context(filename, line_number)
        
        tb = tb.tb_next
        limit -= 1
    
    traceback_lines.append(f"{exc_type.__name__}: {exc_value}\n")
    return "".join(traceback_lines)

def exception_info(e):
    print(f"Error occurred: {e}")
    
    exc_type, exc_value, exc_traceback = sys.exc_info()
    print(custom_traceback(exc_type, exc_value, exc_traceback, limit=3))

def divide(a, b):
    return a / b



def main():
    divide(4, 0)



try:
    main()
except Exception as e:
    exception_info(e)

```

## Add except with traceback info

```python
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
            
            # Course Row Detection (Integer "Cr" value)
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
                    department_program_courses[current_department][current_program].append(new_row)
                logging.debug(f"Added Course(s) {course_codes} under {current_program} in {current_department}")
            elif row[0]:
                logging.info(f"Skipping row: {repr(row)}")
        
        return (column_names, department_program_courses)
    
    except Exception as e:
        logging.error(f"An error occurred: {str(e)}")
        exception_info(e)
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

```
