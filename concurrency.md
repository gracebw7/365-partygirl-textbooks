# Phenomenon 1:  
2 people try to create a new professor with the same email at the same time, this could result in a lost update if not handled properly. To solve this we added a uniqueness constraint to the email field 

# Phenomenon 2 (Phantom Read):

# Ensuring Isolation
- PostgreSQL's default isolation level (READ COMMITTED) already prevents dirty reads for us.
1. Schema Uniqueness Constraints:  
- Unique constraints on tables like textbooks, professors, and classbooks ensure that duplicate entries cannot be created, even if concurrency issues occur.
2. Higher Isolation Levels:
- Use SERIALIZABLE isolation for endpoints that are prone to higher levels of concurrency problems to prevent concurrency anomalies.
