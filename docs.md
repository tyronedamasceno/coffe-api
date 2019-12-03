# Documentation

Welcome to the **Coffe API**. Here you can manage your harvests and get your storage report.

You can check all registered coffe types and insert new ones if you want.

## How to execute API?

The recommendation is to user Docker and docker-compose.

You just need to clone or download this repository, navigate into folder, then run the following commands:

`$ docker-compose build`

`$ docker-compose up -d`

Now, you have an running API on your localhost on the port 8000.

You may want have a local superuser, so run the command below and follow instructions.

`$ docker-compose run web python manage.py createsuperuser`

You can use the provided credentials to access the admin interface on `https://localhost:8000/admin/`.

## API Endpoints

*obs: all the endpoints require a /api/v1 prefix, ex: localhost:5000/api/v1/users*

*obs: the endpoints requires the header **Authentication** with value "Token <user_token>"*


**/users**

| Method |     Description             |  Parameters  |
| ------ | --------------------------- | ------------ |
|  GET   |  List all the users  |              |
|  POST  |  Create a new user   | *email*, *password*, *name*  |


**/users/{id:integer}**

| Method |     Description             |  Parameters  |
| ------ | --------------------------- | ------------ |
|  GET   |  Retrieve the user with provided id  |              |
|  PATCH  |  Update user information   | *email*, *password*, *name*  |
|  DELETE  |  Delete the user   |  |

**/login/**

*This endpoint response body give the user_token to use on the others requests*

| Method |     Description             |  Parameters  |
| ------ | --------------------------- | ------------ |
|  POST  |  Authenticate an user   | *email*, *password*  |
