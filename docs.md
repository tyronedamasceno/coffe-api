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
