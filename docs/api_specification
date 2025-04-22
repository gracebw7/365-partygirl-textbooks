# API Documentation: Textbook Service

## Endpoint 1: `GET /textbooks/search`
Retrieves a list of textbooks based on criteria provided in the **query parameters**.

### Query Parameters:
- `department` (string, optional): Filter textbooks by department.
- `courseNumber` (string, optional): Filter textbooks by course number.
- `professor` (string, optional): Filter textbooks by professor's name.
- `title` (string, optional): Filter textbooks by textbook title.
- `author` (string, optional): Filter textbooks by textbook author.
- `edition` (string, optional): Filter textbooks by textbook edition.
- `sortBy` (string, optional): Sort results by a specific field (e.g., `dateAdded`).
- `sortOrder` (string, optional): Specify the sort order (`asc` or `desc`). Defaults to `desc`.

### Responses:
- `200 OK`: A JSON array of textbook objects (`title`, `author`, `edition`, `links`, `size` optional).
- `400 Bad Request`: Invalid request.
- `404 Not Found`: No matching textbooks.

---

## Endpoint 2: `GET /textbooks/{textbookId}`
Retrieves detailed information for a specific textbook.

### Path Parameter:
- `textbookId` (integer, required): Unique ID of the textbook.

### Responses:
- `200 OK`: JSON object with textbook details.
- `404 Not Found`: Invalid textbook ID.

---

## Endpoint 3: `POST /textbooks`
Adds a new textbook entry to the database.

### Request Body (application/json):
- `department` (string, required)
- `courseNumber` (string, required)
- `professor` (string, required)
- `title` (string, required)
- `author` (string, required)
- `edition` (string, optional)
- `links` (array of URL strings)

### Responses:
- `201 Created`: JSON object with the new textbook entry.
- `400 Bad Request`: Invalid or incomplete request body.
- `409 Conflict`: Duplicate textbook.

---

## Endpoint 4: `GET /textbooks/schedule`
Gets the textbooks and prices for each course in a schedule.

### Request Body (application/json):
An array of course objects:
- `course department` (string, required)
- `course number` (string, required)
- `professor` (string, required)

### Responses:
- `200 OK`: JSON object with textbook info per course.
- `400 Bad Request`: Malformed request or invalid courses.

---

## Endpoint 5: `POST /textbooks/{textbookId}/link`
Adds a new link to an existing textbook entry.

### Path Parameter:
- `textbookId` (integer, required)

### Request Body:
- `link` (string): The URL to be added.

### Responses:
- `204 No Content`: Link successfully added.
- `400 Bad Request`: Invalid or unverified link.
- `404 Not Found`: Invalid textbook ID.

---

## Endpoint 6: `DELETE /textbook/{id}/{linkID}`
Deletes a link from a textbook entry.

### Path Parameters:
- `id` (integer, required): Textbook ID.
- `linkID` (integer, required): Link ID.

### Responses:
- `204 No Content`: Link successfully deleted.
- `404 Not Found`: Invalid textbook or link ID.

---

## Endpoint 7: `POST /course/{textbookID}`
Creates a new course associated with an existing textbook.

### Path Parameter:
- `textbookID` (integer, required)

### Responses:
- `204 No Content`: Course created successfully.
- `400 Bad Request`: Malformed course data.
- `404 Not Found`: Invalid textbook ID.
- `409 Conflict`: Course number already exists.

---

## Endpoint 8: `POST /{courseID}/professor/{textbookID}`
Adds a professor to a course and links the professor/course to a textbook.

### Path Parameters:
- `courseID` (integer, required)
- `textbookID` (integer, required)

### Request Body (application/json):
- `first name` (string, optional)
- `last name` (string, required)

### Responses:
- `200 OK`: JSON object with professor and course/textbook link info.
- `400 Bad Request`: Malformed request or non-existent course/textbook.
- `409 Conflict`: Duplicate professor name.
