# 1. Introduction
This task is used as a skill assessment assignment which Q uses in its selection process to determine
the best candidate for the job. All test assignments should be solvable within a maximum of 8 hours by
an experienced developer. These assignments are not a part of any client project and are not a part
(and will not be) of any production project. Q however reserves the right to limit the disclosure of the
assignment contents.
This assignment is aimed at all developers' seniority and experience levels. Try to get the bulk of the
test done, and note down or comment on the things you didn’t have time to tackle. The things you did
have time for should be complete and representable of your skill and we can talk about the other parts
later.

# 2. Assignment
- Create a REST API backend with the Django framework
- Implement CRUD to manage Product entities
- The product entity consists of:
  - id (primary, integer)
  - name (required, string, unique)
  - price (required)
  - rating (required, float, min 0; max 5)
  - updated_at (optional, date)
- Products can be searched by any field

# 3. Expectations
- API has endpoints to create, list, update and delete the products
- API allows to rate the product
- Solution is documented with how to run it and with dummy data/fixtures included
- Every stage of your development is versioned and can be seen in git history
- Code follows PEP 8 coding style
- Listing endpoint has pagination and can be ordered by fields ascending and descending
- API has endpoints to rate the product, store the average rating on the product itself
- API is documented

## Bonus Points
- Enable authentication and make sure each user can rate the product only once
- API documentation is automatically generated, say Swagger / OpenAPI
- Products are full-text searchable. You can use ElasticSearch here, for example. Employ
fuzziness if you want to
- There are tests in place that can be ran and are passing
- The application runs in a dockerized environment and can easily be ran with docker-compose

# 4. Evaluation
Hope you had a bit of fun writing the solution to this test! You can send the solution in a form of a git
repository (whichever one suits you best; GitHub, GitLab, Bitbucket,...).

Good luck!
