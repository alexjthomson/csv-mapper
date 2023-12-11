# CSV Mapper - Review
This document organises some thoughts about the project after completing the
development, testing, deployment, and patching stages for the application.

## Missing Features
The requirements document written initially specified a column configuration
table that would allow columns within a CSV source to be re-mapped and
transformed into more useful data. This feature has since been scrapped since it
is too impractical to implement on the application. Instead, this should be done
by middleware software before it gets to the Django application. Implementing
this into the Django application would increase the overhead of requesting graph
data by an order of magnitude since additional database interactions would be
required, additional data transformations would be required, among other issues.

## Django Difficulties
Django proved to be a useful and efficient means of getting a web application
working quickly. That being said, it proved to be difficult when trying to get a
2nd database to work. The documentation was unclear about how to go about this.
This was a large time-waste trying to figure out, wasting a total of 4 hours of
development time.

## Refactoring
After completing large parts of the application, I would refactor what I had
just written to reduce reuse of the same code. This was a good way of developing
since it allowed me to write messy code quickly to get the application working.
After writing the messy code, I could look at what I had re-written multiple
times (such as querying the database) and re-write the code in a clean, generic,
object-oriented way that could be used to reduce the amount of repeated code.

## Python & Django
Before this project, I had not used python for any large projects; I had also
never used Django. I adopted the technologies quickly and had little to no sever
issues with them. I would recommend both of them as solid technologies for
developing applications quickly.

---

## Conclusion
Other than the highlighted areas above, development was smooth. The application
did not take long to develop since I already had experience with the
Linux-Docker ecosystem and developing websites with Bootstrap.