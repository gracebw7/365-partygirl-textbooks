**Fake Data Modeling**

Python file for adding data: ____

**Performance Results**

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

**Performance Tuning**
