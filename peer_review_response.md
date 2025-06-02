**Search Endpoint Issues**:
We originally had a number of issues with our search, including a split endpoint model and issues if no textbook matching the criteria was found. To address this, we fully rewrote our search endpoint. We combined the two separate endpoints and made each field an optional query parameter. To do this, we changed the search functionality to be written fully in Pythonic SQL. Now, search returns any textbooks matching any of the provided parameters. Additionally, there is a more helpful message if no textbooks are returned.

**Delete Endpoint Comment**:
We received a comment about our delete link endpoints, since we have both "request delete" and a true "delete link". Since this project doesn't have a frontend, it's a bit confusing on why we have both, but the thought is that the user will have access to the request endpoint, and admin will have access to the true delete endpoint. For testing purposes, though, we currently have both.

**Alex Truong Product Ideas**:
We already have a schedule endpoint where users can input a full schedule to get textbooks. Our updated search function also allows for getting textbooks by class.

**Jake Cheung Product Ideas**:
Our search endpoint covers the functionality of get-by-course. We believe we don't necessarily need to delete courses that are no longer offered, since (1) they may be offered again in the future and (2) if they are not offered, no one will be searching for them.
