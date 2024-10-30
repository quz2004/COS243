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

