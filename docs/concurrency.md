# Concurrency Control
---

## Phenomenon 1 (Idempotency Issue on Delete Link):  
### **Scenario**
Two users attempt to delete the same link simultaneously. Both transactions check if the link exists and determine that it does. The first transaction successfully deletes the link, but the second transaction attempts to delete it again and finds that it no longer exists. This could result in an error (e.g., "Link not found").
### **Sequence Diagram**
    participant UserA
    participant DB
    participant UserB

    UserA->>DB: SELECT id FROM links WHERE id=1
    UserB->>DB: SELECT id FROM links WHERE id=1
    DB-->>UserA: Row exists
    DB-->>UserB: Row exists
    UserA->>DB: DELETE FROM links WHERE id=1
    UserB->>DB: DELETE FROM links WHERE id=1
    DB-->>UserA: Row deleted
    DB-->>UserB: No row found (error or no-op)
Solution: Use SELECT ... FOR UPDATE to lock the row before deleting it, ensuring that only one transaction can delete the row at a time preventing an error from being thrown.

## Phenomenon 2 (Non-Repeatable Read on Create Textbook):  
### **Scenario**  
Two users attempt to create the same textbook (`"Database Systems" by "AuthorX", 3rd Edition`) at the same time. Both transactions check if the textbook exists, and neither sees it because neither has committed yet. Both proceed to insert the textbook, resulting in duplicate entries.  
### **Sequence Diagram**  
    UserA: SELECT id FROM textbooks WHERE title='Database Systems' AND author='AuthorX' AND edition='3rd'  
    UserB: SELECT id FROM textbooks WHERE title='Database Systems' AND author='AuthorX' AND edition='3rd'  
    DB: No record found  
    DB: No record found  
    UserA: INSERT INTO textbooks (title, author, edition) VALUES ('Database Systems', 'AuthorX', '3rd')  
    UserB: INSERT INTO textbooks (title, author, edition) VALUES ('Database Systems', 'AuthorX', '3rd')  
    UserA: Commit  
    UserB: Commit  
Solution: Add a unique constraint on title, author, and edition in the textbooks table to prevent duplicates.

## Phenomenon 3 (Non-Repeatable Read on Create Class):  
### **Scenario**  
Phantom Reads in create_course and create_professor: Two transactions could simultaneously check if a course or professor exists and insert the same record, resulting in duplicates. Phantom Read in create_class: Two transactions could simultaneously check if a class exists and insert the same class, resulting in duplicates. 
### **Sequence Diagram**  
    participant UserA
    participant DB
    participant UserB

    UserA->>DB: SELECT id FROM courses WHERE department='CS' AND number=101
    UserB->>DB: SELECT id FROM courses WHERE department='CS' AND number=101
    DB-->>UserA: No record found
    DB-->>UserB: No record found
    UserA->>DB: INSERT INTO courses (department, number) VALUES ('CS', 101)
    UserB->>DB: INSERT INTO courses (department, number) VALUES ('CS', 101)
    UserA->>DB: SELECT id FROM professors WHERE first='John' AND last='Doe'
    UserB->>DB: SELECT id FROM professors WHERE first='John' AND last='Doe'
    DB-->>UserA: No record found
    DB-->>UserB: No record found
    UserA->>DB: INSERT INTO professors (first, last) VALUES ('John', 'Doe')
    UserB->>DB: INSERT INTO professors (first, last) VALUES ('John', 'Doe')
    UserA->>DB: SELECT id FROM classes WHERE course_id=1 AND professor_id=1
    UserB->>DB: SELECT id FROM classes WHERE course_id=1 AND professor_id=1
    DB-->>UserA: No record found
    DB-->>UserB: No record found
    UserA->>DB: INSERT INTO classes (course_id, professor_id) VALUES (1, 1)
    UserB->>DB: INSERT INTO classes (course_id, professor_id) VALUES (1, 1)
    UserA->>DB: Commit
    UserB->>DB: Commit
Solution: Add a unique constraint on the schemas of the tables above to prevent duplicates.

## Ensuring Isolation
- PostgreSQL's default isolation level (READ COMMITTED) already prevents dirty reads for us.
1. Schema Uniqueness Constraints:  
- Unique constraints on tables like textbooks, professors, and classbooks ensure that duplicate entries cannot be created, even if concurrency issues occur.
2. Higher Isolation Levels:
- Use SERIALIZABLE isolation for endpoints that are prone to higher levels of concurrency problems to prevent concurrency anomalies.
3. Use Row Level Locks
- Use SELECT ... FOR UPDATE to lock rows before performing operations like deletes or updates. This ensures that only one transaction can modify or delete a specific row at a time.
