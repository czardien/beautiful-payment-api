# Beautiful Payment API

This package contains a RESTful API to provide card tokenisation and sale data. See API documentation at:

* http://beautiful-payment-api.herokuapp.com/docs/

## Features

* The `/tokens/` endpoint allows users to get a token,
* The `/sales/` endpoint allows users to post a sale or get sales data given an id.

## Illustrated flow

Feel free to follow Swagger's `try it out` at: http://beautiful-payment-api.herokuapp.com/docs/. Below is an illustrated flow:

* Client requests token from Server; Server requests token from Gateway:

Request:
```
curl -X GET "http://beautiful-payment-api.herokuapp.com/v1/tokens/" -H  "accept: application/json"
```

* Client requests payment method nonce from Gateway using the token; not illustrated here as this only involves a client-side integration.
* Client posts transaction data to Server; Server posts transaction to Gateway:

Request:

```
curl -X POST "http://beautiful-payment-api.herokuapp.com/v1/sales" -H  "accept: application/json" -H  "Content-Type: application/json" -d "{\"amount\":\"10.0\",\"payment_method_nonce\":\"fake-valid-nonce\"}"
```

Response:

```
{
  "sale_id": "5t5yertc"
}
```

* Client requests sale data from Server; Server requests sale data from Gateway:

Request:

```
curl -X GET "http://beautiful-payment-api.herokuapp.com/v1/sales/5t5yertc" -H  "accept: application/json"
```

Response:

```
{
  "sale": {
    "amount": 10,
    "created_at": "2020-04-29T16:38:49"
  }
}
```

## Operations

##### Platform

We currently deploy the service as a serverless app / dyno on [Heroku](https://devcenter.heroku.com/categories/dynos).

##### CI

We currently provide automatic checks as a `pre-push` [git hook](https://git-scm.com/book/en/v2/Customizing-Git-Git-Hooks).

##### Deployment

We currently provide a utility suite to handle deployment as targets in: `Makefile.deploy`. Deployment is done using docker containers. To run with appropriate privileges:

```
make deploy
```

##### Database

We initially supported connection to Postgres through SQLAlchemy however with research it appeared that it was possible to skip storing token or sales data altogether.

## Local development

Requirements:
* A `make` executable,
* A `python3` executable,
* A `docker-compose` executable,

Install dependencies, recommended through a virtual environment, for instance at the root of the project:

```
python3 -m venv beautiful && source beautiful/bin/activate && pip install -r dev-requirements.txt
```

##### Run checks

A checks battery exists and consists of linting, type checking, unit testing and coverage. Run:

```
make checks
```

##### Run local instance

We provide a `docker-compose.yml` file for local development purpose. Run:

```
make up
```

Proceed by navigating to: http://localhost:5000/docs. Get the logs by running:

```
make logs
```

Tear down the local instance with:

```
make down
```

## Todo

* Add logging
* Handling error: `flask_application.register_error_handler(Exception, handle_error_function)`,
* Update error message for POST /v1/sales
* Return payload for found transaction in GET /v1/sales/<sale_id>
