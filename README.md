# DynamoDB Back-to-Basics

## Pre-requisites

- Python 3.12.x
- Poetry 1.8.x

## Tools and Frameworks

- [x] fastapi
- [x] uvicorn
- [x] pytest
- [x] ruff

## Use Cases

- [x] Get details of an E-Bike and related Bookings​
- [x] Get Bookings for a specific User
- [x] Retrieve all available E-Bikes​
- [x] Get details of a specific Booking​
- [x] Create a new Booking​
- [x] Update an existing Booking​
- [x] Delete an existing Booking​


## Commands

Install
```
make make install
```

Start local server
```
make start-local
```

Lint
```
make lint
```

Lint and fix
```
make lint-fix
```

Format
```
make format
```

Launch tests
```
make test
```

Launch test with coverage
```
make coverage
```


## Debug (vscode)

- Install debugpy extension
- Add the following configuration to your launch.json

```json
{
    "version": "0.2.0",
    "configurations": [
        {
            "name": "Python: FastAPI",
            "type": "debugpy",
            "request": "launch",
            "module": "uvicorn",            
            "args": [
                "app.main:app",
                "--reload",
                "--port",
                "3000"
            ]
        }
    ]
}
```