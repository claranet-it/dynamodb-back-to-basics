# DynamoDB Back-to-Basics

## Pre-requisites

- Python 3.12.x
- Poetry 1.8.x

## Tools and Frameworks

- [x] fastapi
- [x] uvicorn
- [x] pytest
- [x] ruff

## Install 

```
make install
```


## Commands

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

Run pre-commit hooks
```
make pre-commit
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