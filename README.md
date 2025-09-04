# Technical Test Template

## Getting started

I have modified a basic Flask API template that runs on port `5000` and includes a `pytest` test showing the endpoint working.

### Requirements

- Python 3.12
- [Poetry](https://python-poetry.org/docs/) for dependency management

### Install dependencies

```sh
poetry install
```

### Start API server

```sh
make run
```

### Run tests

```sh
make test
```

## Testing

```sh
curl -XPOST 'http://127.0.0.1:5000/event' -H 'Content-Type: application/json' \
-d '{ }'
```
-----------------------
## Setting up and starting venv
```python -m venv venv
source venv/bin/activate
pip install flask pytest``


## Conditions
The alerts I implemented were put in a separate file to keep the API focused on handling requests and responses. That separation made it easier to write and test the logic clearly. I also wrote pseudocode for each rule before coding it, which helped me understand exactly what I needed to do.


## Testing
Testing was tricky at times. I wrote unit tests in Pytest for both the API and the alert rules. I had to make sure that when my API returned errors (like when no JSON was sent), it returned proper JSON responses if any and the right status codes.

I also got errors like “argument of type ‘int’ is not iterable” because I mixed up argument orders or types in function calls. To fix this, I added debug print statements to check the types and values of the arguments. This helped me identify exactly where the problem was. For example:

    ```python
    print(f"user_id: {user_id} (type {type(user_id)})")
    print(f"user_events: {user_events} (type {type(user_events)})")Catching those helped me improve how I wrote the functions and tests.


## Challenges
The hardest parts were debugging test failures that didn’t give clear error messages and figuring out exactly how to handle the input and output data correctly. It took some trial and error to get the API responses and tests talking to each other properly.

Another one of my struggles was using version control. Going forwards I would do multiple commits throughout my process even if things aren't correct so I can better understand and document my process and learning. Next time i'd do it in stages instead of one large commit when the file was done.



