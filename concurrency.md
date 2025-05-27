# Concurrency Control
---

## Phenomenon 1:  
2 people try to create a new professor with the same email at the same time, this could result in a lost update if not handled properly. To solve this we added a uniqueness constraint to the email field 

## Phenomenon 2 (Phantom Read):  
### **Scenario**  
Two users attempt to create the same textbook (`"Database Systems" by "AuthorX", 3rd Edition`) at the same time. Both transactions check if the textbook exists, and neither sees it because neither has committed yet. Both proceed to insert the textbook, resulting in duplicate entries.  
### **Sequence Diagram**  
```mermaid
sequenceDiagram
    UserA: SELECT id FROM textbooks WHERE title='Database Systems' AND author='AuthorX' AND edition='3rd'
    UserB: SELECT id FROM textbooks WHERE title='Database Systems' AND author='AuthorX' AND edition='3rd'
    DB: No record found
    DB: No record found
    UserA: INSERT INTO textbooks (title, author, edition) VALUES ('Database Systems', 'AuthorX', '3rd')
    UserB: INSERT INTO textbooks (title, author, edition) VALUES ('Database Systems', 'AuthorX', '3rd')
    UserA: Commit
    UserB: Commit
```

## Ensuring Isolation
- PostgreSQL's default isolation level (READ COMMITTED) already prevents dirty reads for us.
1. Schema Uniqueness Constraints:  
- Unique constraints on tables like textbooks, professors, and classbooks ensure that duplicate entries cannot be created, even if concurrency issues occur.
2. Higher Isolation Levels:
- Use SERIALIZABLE isolation for endpoints that are prone to higher levels of concurrency problems to prevent concurrency anomalies.
