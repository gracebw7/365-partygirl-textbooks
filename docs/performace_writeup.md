# Fake Data Modeling

Python file for adding data: populate.py

# Adding Data

Rows Added:
 - 500 professors to professor table
 - 1000 courses to courses table
 - 10,000 classes to classes table
 - 100,000 textbooks to textbooks table
 - 1,000,000 links to links table

We believe this is a fairly reasonable setup. There are 500 professors that each teach 2 courses. Each course has 10 sections (a single professor teaching 20
sections might be a bit unreasonable, but not increadibly so for the purpose of scale testing). Then, we pretend that each class has 10 textbooks. If we 
allow a "textbook" to also be any sort of reading needed for the class, this seems fairly reasonable for English-focused classes. Finally, we allowed each textbook
to have 10 links. Considering how many links one could easily find on the internet for each textbook, this isn't too crazy. So overall, even though there
are a few places where our service might not scale in exactly this way, it seems likely that we will scale much more in the textbooks and links tables rather
than in professors and classes.

# Performance Results
## Textbooks
- Get All Textbooks: 0.0059 ms
- Create Textbook: 0.0094 ms
- Get Textbook By Id: 0.0209 ms
- Get Textbook Links: 0.0288 ms

## Schedule
- Find By Schedule: 0.229 ms (SLOWEST ENDPOINT)

## Search
- Get Search Textbook: 0.106 ms

## Links
- Get All Links: 0.02099 ms
- Create Link: 0.0654 ms
- Get Link By Id: 0.02029 ms
- Request Deletion: 0.0347 ms
- Delete Link: 0.027 ms

## Courses
- Get All Courses: 0.0054 ms
- Create Course: 0.0281 ms
- Get Course By Id: 0.0299 ms

## Professors
- Get All Professors: 0.0041 ms
- Create Professor: 0.0321 ms
- Get Professor By Id: 0.0147 ms

## Classes
- Get All Classes: 0.0056
- Create Class: 0.0245
- Get Class By Id: 0.0133

## Classbooks
- Get All Classbooks: 0.0035
- Create Classbook: 0.0325
- Get Classbook By Id: 0.0122

# Performance Tuning
```SQL
CREATE INDEX idx_textbook_classes_class_id
ON textbook_classes (class_id);
```
