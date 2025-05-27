# API Documentation: Textbook Service

## Endpoint 1: `GET /search/`
Retrieves a list of textbooks based on criteria provided in the **query parameters**.

### Request Body:
- `department` (string, optional): Filter textbooks by department.
- `number` (string, optional): Filter textbooks by course number.
- `professorFirst` (string, optional): Filter textbooks by professor's name.
- `professorLast` (string, optional): Filter textbooks by professor's name.
- `title` (string, optional): Filter textbooks by textbook title.
- `author` (string, optional): Filter textbooks by textbook author.
- `edition` (string, optional): Filter textbooks by textbook edition.

### Responses:
- `200 OK`: A JSON array of textbook objects (`title`, `author`, `edition`, `links`).
- `422 Validation error`: Invalid request.
---

## Endpoint 2: `GET /textbooks/{textbookId}`
Retrieves detailed information for a specific textbook.

### Path Parameter:
- `textbookId` (integer, required): Unique ID of the textbook.

### Responses:
- `200 OK`: JSON object with textbook details.
- `422 Validation Error`: Invalid query.
- `404 Not Found`: Invalid textbook ID.

---

## Endpoint 3: `POST /textbooks/`
Adds a new textbook entry to the database.

### Request Body (application/json):
- `title` (string, required)
- `author` (string, required)
- `edition` (string, optional)

### Responses:
- `200 Successful`: JSON object with the new textbook entry.
- `400 Bad Request`: Invalid or incomplete request body.
- `409 Conflict`: Duplicate textbook.

---

## Endpoint 4: `POST /schedule/`
Gets the textbooks for each course in a schedule.

### Request Body (application/json):
An array of course objects:
- `department` (string, required)
- `number` (string, required)
- `professor first` (string, required)
- `professor last` (string, required)
- `professor email` (string, required)

### Responses:
- `200 OK`: JSON object with textbook info per course.
- `400 Bad Request`: Malformed request or invalid courses.
- `404 Not Found`: If there are no classes/textbooks in the database to return

---

## Endpoint 5: `POST /links/`
Adds a new link to an existing textbook entry.

### Request Body:
- `textbookId` (integer, required)
- `link` (string): The URL to be added.

### Responses:
- `204 No Content`: Link successfully added.
- `400 Bad Request`: Invalid or unverified link.
- `404 Not Found`: Invalid textbook ID.

---

## Endpoint 6: `DELETE /links/{linkID}`
Deletes a link from a textbook entry.

### Path Parameters:
- `linkID` (integer, required): Link ID.

### Responses:
- `204 No Content`: Link successfully deleted.
- `404 Not Found`: Invalid textbook or link ID.

---

## Endpoint 7: `GET /textbooks/`
Gets all textbooks in database.

### Responses:
- `200 Successful Response`: JSON of textbooks.

---

## Endpoint 8: `GET /textbooks/{textBookId}/links`
Gets all links for given textbook ID.

### Path Parameters:
- `textbookID` (integer, required): Textbook ID.

### Responses:
- `204 No Content`: Link successfully deleted.
- `404 Not Found`: Invalid textbook or link ID.

---

## Endpoint 9: `GET /links/`
Gets all links in database.

### Responses:
- `200 Successful Response`: JSON of links.

---

## Endpoint 10: `GET /links/{linkID}`
Get a link by ID

### Path Parameters:
- `linkID` (integer, required): Link ID.

### Responses:
- `204 No Content`: Link successfully deleted.
- `404 Not Found`: Invalid textbook or link ID.

---

## Endpoint 11: `POST /links/{linkID}`
Request link deletion.

### Request Body:
- `linkID` (integer, required): Link ID.
- `description` (string, required): description of link issue.

### Responses:
- `204 No Content`: Link successfully deleted.
- `404 Not Found`: Invalid textbook or link ID.

---
