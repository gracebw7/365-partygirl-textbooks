## Example Flow 1: ## 
Professor Lucas Pierce has a PDF of his new textbook and wants to add it to the database. He wants to search the textbooks to ensure it was added.
1. Professor submits textbook information: Pierce makes an API call: (POST/api/v1/textbooks)
2. The API checks if the textbook already exists: The server processes the request and determines if a textbook with the same title, author, and edition is already in the database.
   * Scenario A: Textbook Already Exists: The API informs the application with HTTP 409 Conflict.
   * Scenario B: Textbook Does Not Exist: The API successfully adds the new textbook and responds with HTTP 201 Created.
3. Professor searches for textbook: Pierce makes an API call: (GET /textbooks/search) 
 * Request Body (application/json): 
    * `department` (string, optional): “”
    * `courseNumber` (string, optional): “365”
    * `professor` (string, optional): “Lucas Pierce” 
    * `title` (string, optional): “”  
    * `author` (string, optional): “” 
    * `edition` (string, optional): “” 
    * `sortBy` (string, optional): “” 
    * `sortOrder` (string, optional): “” 
    * Scenario A: Query Is Successful: The API informs the application with HTTP 200 and returns JSON containing all textbooks under course 365 and professor Lucas Pierce.
4.Later, to verify the textbook link he posted works Professor Pierce decides to check the textbook entry directly with GET /textbooks/{textbookId}. Having received the textbook ID from the calls above. 

## Example Flow 2: ##

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
5. Note: Clearly, there is an issue with allowing users to directly delete links, so there would likely be a step in between to verify the link is actually broken. 

## Example Flow 3: ##
A student, Patrick, is enrolled in PHYS 142 and wants to download the class textbook. 
1. Student searches for the course: Patrick makes an API call: (GET/api/textbooks/search/{“department: PHYS”, “course”:“142”}/{“title”: “Intro to Phys…”}
2. The API returns any textbooks where the courseNumber matches the query
   * Scenario A: The course and title exists: The API successfully returns the textbook with that title and that course and responds with HTTP 200 OK.
   * Scenario B: A textbook with that course and title doesn’t exist: The API informs the application with HTTP 404 Not Found.
   * Scenario C: A textbook with that course OR that title exists: The API returns the textbooks that match at least one attribute that was queried
3. In this case, say Scenario C occurred and a textbook with that title is found but not that course, the student can then add a course with the existing textbook: Patrick makes the API call POST/api/course/{already existing textbookID}
   * Scenario A:  The API successfully updates the existing textbook with a new course and creates a new course, then  returns HTTP 200 OK
   * Scenario B: The API fails to find the textbook ID and returns HTTP 404 Not Found
4. Patrick also notices that one of the other required text for the course is listed but he was given an updated link: Patrick makes the API call POST/api/textbook/id/link with a JSON body including the new link
   * Scenario A: The API successfully updates the existing textbook with a new link and returns HTTP 204 No Content
   * Scenario B: The API fails to find the textbook ID and returns HTTP 404 Not Found
   * Scenario C: Link not available to be verified, or malformed link and the API returns HTTP 400 bad request.
