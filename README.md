# backend_test

## Installation
To install the project it is necessary to:
1. Clone the repository
2. Build and run docker containers
```bash
docker-compose up
```

During the container building, **startup.sh** file will automatically execute the following actions:
- make migrations;
- collect static content (for django admin);
- run server.


## Usage
### Admin panel
For the convenience of data manipulation you can use [django admin panel](http://127.0.0.1:8080/admin/).
Before the usage of admin panel, it is necessary to create superuser:
```bash
python manage.py createsuperuser
```
As example, you can use the following credentials:
```bash
login: admin
password: admin
```
### CRUD+Listing model
To use the CRUD+Listing model, use the following endpoints:
```bash
http://127.0.0.1:8080/users/ GET - list of all users
http://127.0.0.1:8080/users/ POST - create a new user
http://127.0.0.1:8080/users/{id} GET - get the profile of user by id
http://127.0.0.1:8080/users/{id} PUT - modify the profile of user by id
http://127.0.0.1:8080/users/{id} DELETE - delete the profile of user by id
```
### Additional endpoints
1. **get_friends** endpoint returns all friends profiles of the specified user by id
```bash
http://127.0.0.1:8080/users/{id}/get_friends/
```
2. **get_shorter_connection** endpoin returns the shorter connection between two specified users using an array of Ids.
```bash
http://127.0.0.1:8080/users/get_shorter_connection/?start_id={first_id}&end_id={second_id}
```
the endpoint returns **400 Bad Reques** in the following cases:
- if there is no user in database by specified id
- if the shortest path doesn't exist (the specified users are not linked)

### Seeder script
The script is located on path **backend_task/mysite/social_network/management/commands/executeseederscript.py**

To execute the seeder script, use the following command in the docker container
```bash
python manage.py executeseederscript --profilesTotal {num_1} --friendsTotal {num_2}
```
For profiles generation **https://randomuser.me/** API has been used

### Tests
To run tests, use the following command in the docker container
```bash
python manage.py test social_network/tests/
```