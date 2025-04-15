**User Story 1:** As a student preparing materials for an upcoming class, I want to be able to search for a textbook link I need by course number and professor, so that I can ensure I get the book that matches my class needs. 

**Exception:** Professor or course does not exist
 - If the user searches for a textbook using a course number of professor that is not in the database, the API will return an error stating that no matching results exist and asking the user to double-check the given course number and professor.

**User Story 2:** As a student preparing materials for a full schedule of upcoming courses, I want to be able to search for all my textbooks at one time by entering my entire class schedule and receiving links for all the textbooks I need, so that I can easily find all my textbooks for a quarter in one place.

**Exception:** Improper formatting of classes
 - One possible error here is if when entering their schedule, the user misformats some of their schedule details leading to issues with the mismatched subject, course number, professor, etc. If this error occurs the API will return an error saying that there was an issue finding 1 or more of the classes (the rest will be returned properly). In the error, the troublesome request will be listed making it easy for the user to correct a faulty entry. 

**User Story 3:** As a student who recently received the syllabus for my class, I want to find a link to the required textbook by entering the name, author, and edition of a certain textbook, so that I can access the test I need and be sure the information matches my syllabus. 

**Exception:** The textbook doesn’t exist in the database
 - If the requested textbook cannot be found in the database the API will return an error message stating that the book in question could not be found along with a reprint of the request in case of any typos. Additionally, the API can do some submission standardizing and checking of any partial matches in the event the full textbook title is not given.

**User Story 4:** As a student registering for new classes, I want to see how expensive a class textbook would be if not in the database to inform my class decisions.

**Exception:** Price data isn’t in the database and cannot be found elsewhere.
 - If the user was trying to find the price for a single textbook, inform them that it cannot be found. If the user was trying to find the price for an entire schedule, give them the estimated cost but note in the response that the cost of some textbook(s) couldn’t be found.

**User Story 5:** As a student looking for a textbook, I want to see multiple link options for a single textbook, so that I can choose the most reliable or convenient source and have a backup in case one link is broken.

**Exception:** Only one link or no link exists for the textbook in the database.
 - If the database query result includes fewer than 2 links, the API should return the available links and provide the user the additional location to find links to the requested textbook as well as the option to submit a new link if found.

**User Story 6:** As a professor with a PDF of a textbook, I want to make sure that my class textbook is in the database so my students can access it easily. 

**Exception:** The textbook already exists in the database.
 - If the textbook is already in the database with a link to a pdf, show the user the current entry and allow them to add an additional link to the book. 

**User Story 7:** As a student searching for a difficult-to-find textbook, I want to be able to view links from Anna’s Archive or similar open library sources so I can access resources that other students haven’t uploaded yet.

**Exception:** The web scraper can’t find a source
 - If the textbook can’t be found on Anna’s Archive the frontend could just suggest the user manually search Anna’s Archive or some other library and provide links to the home pages of those sites.

**User Story 8:** As a student or general user who has resources to share, I want to be able to add a professor and specific course to which I can upload a resource. 

**Exception:** Course or professor already exists in the database (append) 
 - If a course or professor already exists in the database, the user should be redirected to add a new resource to the course or professor's page instead of creating a new course & professor.

**User Story 9:** As a student or general user, I want to know that the links I’m clicking on to access my textbook are both safe and still work.

**Exception:** Link status is unknown by our program.
 - We will write code to attempt to remove faulty links and allow faulty links to be reported, but if a link is possibly dangerous or has an unknown status, we will flag it so the user knows.

**User Story 10:** As a user with an older computer, I want to see the size of the textbook so I know how much space it is going to require on my device.

**Exception:** Textbook size information is unavailable.
 - The response should indicate that the size is "Not Available" or "Size Unknown" for that entry.

**User Story 11:** As a student, I want to sort textbook search results by the most recently added links so that I can quickly see the newest resources available.

**Exception:** The date-added information is missing for some textbook entries.
- Place these entries either at the beginning or end of the sorted list, with a clear visual indicator (e.g., a note or a different styling) that the addition date is unavailable.

**User Story 12:** As a student, I want to see the date when a textbook link was added to the database so that I can have more context about the recency and potential validity of the link.

**Exception:** The "date added" information is in an incorrect or unreadable format.
 - Display a standardized message for such cases, such as "Date Unavailable" or "Invalid Date Format."
