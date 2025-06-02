![IMG_6897](https://github.com/user-attachments/assets/c8cbdd66-91b1-4490-8405-dc332ef9fb5c)

## Course:
- Id (PK) (Int)
- Department (Text)
- Number (Int)
## Professor:
- Id - primary key
- Firstname  (Text)
- Lastname (Text)
- Email (Text)
## Class:
- Id (PK) (Integer)
- Course id (FK) (Integer)
- Professor id (FK) (Integer)
## Textbook:
- Id (PK) (Integer)
- Title (Text)
- Author (Text)
- Edition (Text)
## Link:
- LinkID (PK) (Int)
- Created_At (Timestamp)
- TextbookID (FK) (Int)
- URL (Text)

## Join Tables:
ClassBooks -> Join Class & Textbook
