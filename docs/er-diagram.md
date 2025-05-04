![IMG_6897](https://github.com/user-attachments/assets/c8cbdd66-91b1-4490-8405-dc332ef9fb5c)

## Course:
- Id - primary key (Integer)
- Department (Text)
- Number (Int)
## Professor:
- Id - primary key
- Firstname  (Text)
- Lastname (Text)
## Class:
- Id - primary key (Integer)
- Course id (foreign key reference) (Integer)
- Professor id (foreign key reference) (Integer)
## Textbook:
- Id - primary key (Integer)
- Title (Text)
- Author (Text)
- Edition (Text)
## Link:
- LinkID (PK) (Int)
- TextbookID (FK) (Int)
- URL (Text)

## Join Tables:
ClassBooks -> Join Class & Textbook
