## Example Flow 1 ## 
Professor Lucas Pierce has a PDF of his new textbook and wants to add it to the database. He wants to search the textbooks to ensure it was added.
1. Professor submits textbook information: Pierce makes an API call: (POST/api/v1/textbooks)
2. The API checks if the textbook already exists: The server processes the request and determines if a textbook with the same title, author, and edition is already in the database.
   * Scenario A: Textbook Already Exists: The API informs the application with HTTP 409 Conflict.
   * Scenario B: Textbook Does Not Exist: The API successfully adds the new textbook and responds with HTTP 201 Created.
3. Professor searches for textbook: Pierce makes an API call: (GET /textbooks/search) 
 * Request Body (application/json): 
    * `department` (string): “CSC”
    * `courseNumber` (string): “365”
    * `professorFirst` (string): “Lucas"
    * `professorLast` (string) "Pierce” 
    * Scenario A: Query Is Successful: The API informs the application with HTTP 200 and returns JSON containing all textbooks under course 365 and professor Lucas Pierce.
4.Later, to verify the textbook link he posted works Professor Pierce decides to check the textbook entry directly with GET /textbooks/{textbookId}. Having received the textbook ID from the calls above.

## TESTING RESULTS 1

***Uploading Textbook***
CURL:
curl -X 'POST' \
  'https://three65-partygirl-textbooks.onrender.com/textbooks/all_info' \
  -H 'accept: application/json' \
  -H 'access_token: 8a9881b55f0bd902d4a26fad794a856b' \
  -H 'Content-Type: application/json' \
  -d '{
  "title": "Databases 123",
  "author": "Trotter McLemore",
  "edition": "6th",
  "prof_first": "Lucas",
  "prof_last": "Pierce",
  "department": "CSC",
  "course_number": 365,
  "url": "https://imtk.ui.ac.id/wp-content/uploads/2014/02/Fluid-Mechanics-Cengel.pdf"
}'

RESPONSE:
Code: 200
Response Body: {
  "textbook_id": 2,
  "professor_id": 2,
  "course_id": 2,
  "class_id": 2,
  "classbook_id": 1,
  "link_id": 1
}

***Searching for textbook***
CURL:
curl -X 'GET' \
  'https://three65-partygirl-textbooks.onrender.com/search/search_by_prof?department=CSC&number=365&professorFirst=Lucas&professorLast=Pierce' \
  -H 'accept: application/json' \
  -H 'access_token: 8a9881b55f0bd902d4a26fad794a856b'

RESPONSE:
Code: 200
Response Body: {
  "id": 2,
  "title": "Databases 123",
  "author": "Trotter McLemore",
  "edition": "6th",
  "links": [
    "https://imtk.ui.ac.id/wp-content/uploads/2014/02/Fluid-Mechanics-Cengel.pdf"
  ]
}

***Get textbook by ID***
CURL:
curl -X 'GET' \
  'https://three65-partygirl-textbooks.onrender.com/textbooks/textbooks/2' \
  -H 'accept: application/json' \
  -H 'access_token: 8a9881b55f0bd902d4a26fad794a856b'

RESPONSE:
Code: 200
Response Body: {
  "title": "Databases 123",
  "author": "Trotter McLemore",
  "edition": "6th"
}

## Example Flow 2 ##

A student, Grace, is looking to find the link for a textbook for all her courses for a quarter. 
1. Grace searches for textbook links by course: Grace makes the API call (GET /textbooks/schedule) with the response body:
{
{
department: CSC
course: 445
professor:  Frishberg, Daniel
}
…
{...} }
2. API response with a JSON object of various textbook links for each course.
{
{
department: CSC
course: 445
professor:  Frishberg, Daniel
Links: {
{ Title: “Book 1”
Link1: “...”
Link2: “...” }
}
…
{...} }
3. When checking the link, Grace finds that one is broken: Grace calls DELETE /textbook/{id}/{linkID} to remove the link so other users do not encounter errors. 
4. Later, Grace finds a working link and decides to add it to the service: Grace makes the API call POST /textbooks/{textbookId}/link with the body { “link”: “https://…”}. The response is a 204, meaning the link was added successfully

## TESTING RESULTS 2

***Get textbooks by schedule***
CURL:
curl -X 'POST' \
  'https://three65-partygirl-textbooks.onrender.com/schedule/' \
  -H 'accept: application/json' \
  -H 'access_token: 8a9881b55f0bd902d4a26fad794a856b' \
  -H 'Content-Type: application/json' \
  -d '[
  {
    "department": "CSC",
    "number": 365,
    "prof_first": "Lucas",
    "prof_last": "Pierce"
  },
  {
    "department": "CSC",
    "number": 445,
    "prof_first": "Daniel",
    "prof_last": "Frishberg"
  }
]'

RESPONSE:
Code: 200
Response Body: [
  {
    "title": "Databases 123",
    "author": "Trotter McLemore",
    "edition": "6th",
    "links": [
      "https://imtk.ui.ac.id/wp-content/uploads/2014/02/Fluid-Mechanics-Cengel.pdf"
    ]
  },
  {
    "title": "Theory of Computation 123",
    "author": "Trotter McLemore",
    "edition": "6th",
    "links": [
      "http://library1.ga/_ads/688E77D2151C08BC95F47468C2C28FF0"
    ]
  }
]

***Request deletion for link Id 1***
CURL: 
curl -X 'POST' \
  'https://three65-partygirl-textbooks.onrender.com/links/1?description=link%20does%20not%20work' \
  -H 'accept: application/json' \
  -H 'access_token: 8a9881b55f0bd902d4a26fad794a856b' \
  -d ''

RESPONSE:
Code: 200
Response Body: {
  "message": "Deletion request for link 1 created successfully.",
  "request_id": 1
}

***Add new link for textbook Id 1***
CURL: 
curl -X 'POST' \
  'https://three65-partygirl-textbooks.onrender.com/links/?textbook_id=1&url=https%3A%2F%2Fes.b-ok.cc%2Fbook%2F3492387%2F2a3dc5' \
  -H 'accept: application/json' \
  -H 'access_token: 8a9881b55f0bd902d4a26fad794a856b' \
  -d ''

RESPONSE:
Code: 200
Response Body: {
  "link_id": 3
}

## Example Flow 3 ##
A student, Patrick, is enrolled in PHYS 142 and wants to download the class textbook. 
1. Student searches for the course: Patrick makes an API call: (GET/api/textbooks/search/{“department: PHYS”, “course”:“142”}/{“title”: “Intro to Phys…”}
2. The API returns any textbooks where the courseNumber matches the query
   * Scenario A: The course and title exists: The API successfully returns the textbook with that title and that course and responds with HTTP 200 OK.
   * Scenario B: A textbook with that course and title doesn’t exist: The API informs the application with a null response.
   * Scenario C: A textbook with that course OR that title exists: The API returns the textbooks that match at least one attribute that was queried
3. In this case, say Scenario B occurred and a textbook is not found.
4. Patrick also notices that one of the other required text for the course is listed but he was given an updated link: Patrick makes the API call POST/api/textbook/id/link with a JSON body including the new link
   * Scenario A: The API successfully updates the existing textbook with a new link and returns HTTP 204 No Content
   * Scenario B: The API fails to find the textbook ID and returns HTTP 404 Not Found
   * Scenario C: Link not available to be verified, or malformed link and the API returns HTTP 400 bad request.

## TESTING RESULTS 3
***Search for textbook***
CURL:
curl -X 'GET' \
  'https://three65-partygirl-textbooks.onrender.com/search/search_by_prof?department=PHYS&number=142&professorFirst=Scott&professorLast=Fraser' \
  -H 'accept: application/json' \
  -H 'access_token: 8a9881b55f0bd902d4a26fad794a856b'

RESPONSE:
Code: 200
Response Body: null

***Upload link, scenario B***
CURL:
curl -X 'POST' \
  'https://three65-partygirl-textbooks.onrender.com/links/?textbook_id=4&url=https%3A%2F%2Fes.b-ok.cc%2Fbook%2F3492387%2F2a3dc5' \
  -H 'accept: application/json' \
  -H 'access_token: 8a9881b55f0bd902d4a26fad794a856b' \
  -d ''

RESPONSE:
Code: 200
Response Body: {
  "link_id": 6
}
