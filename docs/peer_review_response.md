# Search Endpoint Issues
We originally had a number of issues with our search, including a split endpoint model and issues if no textbook matching the criteria was found. To address this, we fully rewrote our search endpoint. We combined the two separate endpoints and made each field an optional query parameter. To do this, we changed the search functionality to be written fully in Pythonic SQL. Now, search returns any textbooks matching any of the provided parameters. Additionally, there is a more helpful message if no textbooks are returned.

# Delete Endpoint Comment
We received a comment about our delete link endpoints, since we have both "request delete" and a true "delete link". Since this project doesn't have a frontend, it's a bit confusing on why we have both, but the thought is that the user will have access to the request endpoint, and admin will have access to the true delete endpoint. For testing purposes, though, we currently have both.

# Alex Truong Product Ideas + Additional Post Endpoint
We already have a schedule endpoint where users can input a full schedule to get textbooks. Our updated search function also allows for getting textbooks by class. For the additional departments POST endpoint, department creation is already covered by class/courses/professors/textbooks, and adding a specifc department endpoint would just be confusing.

# Jake Cheung Product Ideas 
Our search endpoint covers the functionality of get-by-course. We believe we don't necessarily need to delete courses that are no longer offered, since (1) they may be offered again in the future and (2) if they are not offered, no one will be searching for them.

# Schedule Fixes
- Schedule now works directly with the database, and thus is easier to understand and debug. Additionally, this removes the ability for an erroneous class or professor to be added
- Fixed the parameter binding on class ID for textbooks
- If no class or textbooks are found endpoint now returns a 404 error
     - Two issues referred to the default functionality and confusion about the endpoint
     - Endpoint is documented in the API Specification, but more could be added to clarify the purpose
- Repaired the return object to include links
- Ensure that the endpoint works with the new schema and class specification (see below)

# Updating classes and response
- For Class object changes, the following:
     - changed number to course number
     - changed prof_first and prof_last to professor_first and professor_last
- Updated anything with the Professor Class (including the class) to work with the new email field

# Added input field validation for classes
- All input fields that are not IDs are now checked (IDs will be checked with the schema constraints)
- The course and professor classes now have field validation 
- This is automatically checked with the POST /course and /professor endpoints and is manually checked with a try/catch for the create class endpoint

