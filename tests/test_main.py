from pathlib import Path

import pytest

from firebirdsql_run import (
    CompletedTransaction,
    Connection,
    DBAccess,
    callproc,
    connection,
    execute,
    make_query,
)


@pytest.fixture
def test_db() -> Path:
    return Path("/var/lib/firebird/data/testdb.fdb")


@pytest.mark.online
def test_connection(test_db: Path):
    """Test the connection function."""
    # Define test parameters
    host = "localhost"
    port = 3050
    user = "testuser"
    access = DBAccess.READ_ONLY

    # Create a connection object
    conn = connection(
        host=host,
        port=port,
        db=test_db,
        user=user,
        passwd="testpass",
        access=access,
    )

    # Assert the result
    assert isinstance(conn, Connection)
    assert conn.filename == f"{test_db}"
    assert conn.hostname == host
    assert conn.port == port
    assert conn.user == user
    assert conn.isolation_level == access.value


@pytest.mark.online
def test_execute(test_db: Path):
    """Test execute function."""
    # Define test parameters
    query = "SELECT * FROM rdb$database;"
    host = "localhost"
    port = 3050
    user = "testuser"
    access = DBAccess.READ_ONLY

    # Execute a query
    result = execute(
        query=query,
        host=host,
        port=port,
        db=test_db,
        user=user,
        passwd="testpass",
        access=access,
    )

    # Assert the result
    assert isinstance(result, CompletedTransaction)
    assert result.host == host
    assert result.db == f"{test_db}"
    assert result.port == port
    assert result.user == user
    assert result.access == access.name
    assert result.returncode == 0
    assert result.exception == ""
    assert result.query == query
    assert result.params == ()
    assert result.time > 0
    assert len(result.data) > 0


@pytest.mark.online
def test_execute_with_existing_connection(test_db: Path):
    """Test execute function with an existing connection."""
    # Define test parameters
    query = "SELECT * FROM rdb$database;"
    host = "localhost"
    port = 3050
    user = "testuser"
    access = DBAccess.READ_ONLY

    # Create a connection object
    conn = connection(
        host=host,
        db=test_db,
        port=port,
        user=user,
        passwd="testpass",
        access=access,
    )
    # Execute a query using the existing connection
    result = execute(query=query, use_conn=conn)
    # Close the connection
    conn.close()

    # Assert the result
    assert isinstance(conn, Connection)
    assert conn.filename == f"{test_db}"
    assert conn.hostname == host
    assert conn.port == port
    assert conn.user == user
    assert conn.isolation_level == access.value
    assert isinstance(result, CompletedTransaction)
    assert result.host == host
    assert result.db == f"{test_db}"
    assert result.port == port
    assert result.user == user
    assert result.access == access.name
    assert result.returncode == 0
    assert result.exception == ""
    assert result.query == query
    assert result.params == ()
    assert result.time > 0
    assert len(result.data) > 0


def test_execute_with_exception_with_default_values():
    """Test execute function with default values."""
    # Define test parameters
    query = "SELECT * FROM rdb$database;"

    # Execute a query
    result = execute(query=query)

    # Assert the result
    assert isinstance(result, CompletedTransaction)
    assert result.returncode == 1
    assert result.exception == "Please setup FIREBIRD_KEY in environment variables."
    assert result.query == query
    assert result.params == ()
    assert result.time == 0
    assert isinstance(result.data, list)


def test_execute_with_exception():
    """Test execute function with an exception."""
    # Define test parameters
    query = "SELECT * FROM non_existing_table;"
    host = "localhost"
    db = "NONEXISTENT"
    user = "NONEXISTENT"
    access = DBAccess.READ_ONLY

    # Execute a query
    result = execute(
        query=query,
        host=host,
        db=db,
        user=user,
        passwd="NONEXISTENT",
        access=access,
    )

    # Assert the result
    assert isinstance(result, CompletedTransaction)
    assert result.host == host
    assert result.db == db
    assert result.user == user
    assert result.access == access.name
    assert result.returncode == 1
    assert len(result.exception) > 0
    assert result.query == query
    assert result.params == ()
    assert result.time == 0
    assert result.data == []


def test_make_query():
    """Test make_query function."""
    # Define test parameters
    procname = "PROCNAME"
    params = ("p1", "p2", "p3")

    # Call the function
    query = make_query(procname, params)

    # Assert the result
    assert isinstance(query, str)
    assert query == "EXECUTE PROCEDURE PROCNAME ?,?,?"


def test_callproc_with_exception():
    """Test callproc function with an exception."""
    # Define test parameters
    procname = "PROCNAME"
    params = ("p1", "p2", "p3")
    host = "localhost"
    db = "NONEXISTENT"
    user = "NONEXISTENT"
    access = DBAccess.READ_WRITE

    # Execute a query
    result = callproc(
        procname=procname,
        params=params,
        host=host,
        db=db,
        user=user,
        passwd="NONEXISTENT",
        access=access,
    )

    # Assert the result
    assert isinstance(result, CompletedTransaction)
    assert result.host == host
    assert result.db == db
    assert result.user == user
    assert result.access == access.name
    assert result.returncode == 1
    assert len(result.exception) > 0
    assert result.query == make_query(procname, params)
    assert result.params == params
    assert result.time == 0
    assert result.data == []
