# AuthServer

A simple authentication server in Python Flask

## What is this?

This is a simple server where a user can create an account with user, password, first and last name, log into it
and, once logged in, see the account data, modify it or delete it.

### Authentication logic

Authentication here is done via Bearer Tokens; upon login, the user will get a Bearer Token in a cookie that will
identify one particular account and that will last for 2 hours (configurable). For every request that requires being
logged, that Bearer Token should be sent in the same cookie that was received or in the `Authorization` header.

### Server Configuration

All the relevant application configuration values are stored in the `application.conf` files that can be found in
the `resources` directory.

The file system in that directory allows for general configuration properties (the `app` directory) and per environment
configuration properties (the `env` directory).

Finally, there is a `sensitive.conf` (that would normally be ignored but doesn't make sense for the scope of this)
that should be injected directly in to the server and hold things like the database password or the app secret,
which is used for signing token cookies.

### Database migration

Database migration is automatic and run before the server starts by analyzing all the `Model` objects we have
in the application and whether they have changed (or been created). See `manage.py`.

## Running the server

To start the server locally:

1. Have `Docker` installed and running
2. Have `docker-compose` installed
3. Execute the command `make run`

The last step will start two Docker containers, one with the PostgreSQL database and another one with the
Flask app. Once it's up and running, you can access it in `localhost:5000` (see the Postman collection for
examples).

## Testing the application

To run all the unit and integration tests:

1. Run the `make prepare` command to create the virtual environment with all the required libraries.
2. Run `make test`.