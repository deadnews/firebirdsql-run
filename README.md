# firebirdsql-run

> [Firebirdsql](https://github.com/nakagami/pyfirebirdsql/) wrapper inspired by [subprocess.run](https://docs.python.org/3/library/subprocess.html#subprocess.run)

[![PyPI: Version](https://img.shields.io/pypi/v/firebirdsql-run?logo=pypi&logoColor=white)](https://pypi.org/project/firebirdsql-run)
[![GitHub: Release](https://img.shields.io/github/v/release/deadnews/firebirdsql-run?logo=github&logoColor=white)](https://github.com/deadnews/firebirdsql-run/releases/latest)
[![Documentation](https://img.shields.io/badge/documentation-gray.svg?logo=materialformkdocs&logoColor=white)](https://deadnews.github.io/firebirdsql-run)
[![CI: pre-commit](https://results.pre-commit.ci/badge/github/deadnews/firebirdsql-run/main.svg)](https://results.pre-commit.ci/latest/github/deadnews/firebirdsql-run/main)
[![CI: Main](https://img.shields.io/github/actions/workflow/status/deadnews/firebirdsql-run/main.yml?branch=main&logo=github&logoColor=white&label=main)](https://github.com/deadnews/firebirdsql-run/actions/workflows/main.yml)
[![CI: Coverage](https://img.shields.io/codecov/c/github/deadnews/firebirdsql-run?token=OCZDZIYPMC&logo=codecov&logoColor=white)](https://app.codecov.io/gh/deadnews/firebirdsql-run)

**[Installation](#installation)** • **[Examples](#examples)** • **[Env Variables](#env-variables)**

## Installation

```sh
pip install firebirdsql-run
# or
poetry add firebirdsql-run
```

## Examples

Execute a query with read-only access:

```py
from firebirdsql_run import DBAccess, execute

# Execute a query with read-only access.
result = execute(query="SELECT * FROM table", db="database", access=DBAccess.READ_ONLY)

# Output: List of dictionaries containing the query results.
print(result.data)
```

Execute a query with parameters and log the result:

```py
# Execute a query with parameters.
result = execute(query="INSERT INTO customers (name, age) VALUES (?, ?)", params=("John", 25))

# Log the result.
if result.returncode != 0:
    logger.error(result)
else:
    logger.info(result)
```

Execute a query using the existing connection:

```py
# Create a connection object.
conn = connection(db="database", access=DBAccess.READ_ONLY)
# Execute a query using the existing connection.
result = execute(query="SELECT * FROM table", use_conn=conn)
# Close the connection.
conn.close()

# Output: Named tuple representing the completed transaction.
print(result)
```

An example of a successful transaction:

```py
>>> print(result)
CompletedTransaction(
    host="127.0.0.1",
    db="database",
    user="TWUSER",
    access="READ_ONLY",
    returncode=0,
    exception="",
    query="SELECT * FROM table",
    params=(),
    time=0.001,
    data=[
        {'id': 1, 'name': 'John Doe', 'department': 'Sales'},
        {'id': 2, 'name': 'Jane Smith', 'department': 'Sales'},
    ],
)
```

An example of a failed transaction:

```py
>>> print(result)
CompletedTransaction(
    host="127.0.0.1",
    db="database",
    user="TWUSER",
    access="READ_ONLY",
    returncode=1,
    exception="Dynamic SQL Error\nSQL error code = -204\nTable unknown\ntable\nAt line 1, column 15\n",
    query="SELECT * FROM table",
    params=(),
    time=0.001,
    data=[],
)
```

## Env Variables

```ini
FIREBIRD_KEY=
```

The `FIREBIRD_KEY` environment variable can be overridden with the functions argument `passwd`.
