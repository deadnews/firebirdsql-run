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
from tests.conftest import FirebirdConfig


@pytest.mark.integr
def test_connection(firebird_container: FirebirdConfig):
    """Test the connection function."""
    cfg = firebird_container
    access = DBAccess.READ_ONLY

    conn = connection(
        host=cfg.host,
        port=cfg.port,
        db=cfg.db,
        user=cfg.user,
        passwd=cfg.passwd,
        access=access,
    )

    assert isinstance(conn, Connection)
    assert conn.filename == f"{cfg.db}"
    assert conn.hostname == cfg.host
    assert conn.port == cfg.port
    assert conn.user == cfg.user
    assert conn.isolation_level == access.value


@pytest.mark.integr
def test_execute(firebird_container: FirebirdConfig):
    """Test execute function."""
    cfg = firebird_container
    query = "SELECT * FROM rdb$database;"
    access = DBAccess.READ_ONLY

    result = execute(
        query=query,
        host=cfg.host,
        port=cfg.port,
        db=cfg.db,
        user=cfg.user,
        passwd=cfg.passwd,
        access=access,
    )

    assert isinstance(result, CompletedTransaction)
    assert result.host == cfg.host
    assert result.db == f"{cfg.db}"
    assert result.port == cfg.port
    assert result.user == cfg.user
    assert result.access == access.name
    assert result.returncode == 0
    assert result.exception == ""
    assert result.query == query
    assert result.params == ()
    assert result.time > 0
    assert len(result.data) > 0


@pytest.mark.integr
def test_execute_with_existing_connection(firebird_container: FirebirdConfig):
    """Test execute function with an existing connection."""
    cfg = firebird_container
    query = "SELECT * FROM rdb$database;"
    access = DBAccess.READ_ONLY

    conn = connection(
        host=cfg.host,
        db=cfg.db,
        port=cfg.port,
        user=cfg.user,
        passwd=cfg.passwd,
        access=access,
    )
    result = execute(query=query, use_conn=conn)
    conn.close()

    assert isinstance(conn, Connection)
    assert conn.filename == f"{cfg.db}"
    assert conn.hostname == cfg.host
    assert conn.port == cfg.port
    assert conn.user == cfg.user
    assert conn.isolation_level == access.value
    assert isinstance(result, CompletedTransaction)
    assert result.host == cfg.host
    assert result.db == f"{cfg.db}"
    assert result.port == cfg.port
    assert result.user == cfg.user
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
