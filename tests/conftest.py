"""Pytest configuration and fixtures for integration tests."""

from collections.abc import Generator
from pathlib import Path
from typing import NamedTuple

import pytest
from testcontainers.core.container import DockerContainer
from testcontainers.core.wait_strategies import LogMessageWaitStrategy


class FirebirdConfig(NamedTuple):
    """Configuration for connecting to Firebird test database."""

    host: str
    port: int
    db: Path
    user: str
    passwd: str


@pytest.fixture
def firebird_container(request: pytest.FixtureRequest) -> Generator[FirebirdConfig, None, None]:
    """Start Firebird container for integration tests."""
    if request.node.get_closest_marker("integr") is None:
        pytest.skip("requires integr marker")

    container = DockerContainer("firebirdsql/firebird:5")
    container.with_exposed_ports(3050)
    container.with_env("FIREBIRD_DATABASE", "testdb.fdb")
    container.with_env("FIREBIRD_USER", "testuser")
    container.with_env("FIREBIRD_PASSWORD", "testpass")
    container.waiting_for(LogMessageWaitStrategy("Starting Firebird"))

    with container:
        host = container.get_container_host_ip()
        port = int(container.get_exposed_port(3050))

        yield FirebirdConfig(
            host=host,
            port=port,
            db=Path("/var/lib/firebird/data/testdb.fdb"),
            user="testuser",
            passwd="testpass",
        )
