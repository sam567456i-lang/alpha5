"""Transaction management primitives."""

from __future__ import annotations

from contextlib import contextmanager
from dataclasses import dataclass
from typing import Callable, Iterator

from .exceptions import DatabaseTransactionError

SessionFactory = Callable[[], object]


@dataclass(frozen=True, slots=True)
class TransactionManager:
    """Coordinate commit, rollback, and close for unit-of-work scopes."""

    session_factory: SessionFactory

    @contextmanager
    def transaction(self) -> Iterator[object]:
        """Open a transaction scope around one session."""

        session = self.session_factory()
        try:
            yield session
            session.commit()  # type: ignore
        except Exception as exc:
            try:
                session.rollback()  # type: ignore
            except Exception as rollback_error:
                raise DatabaseTransactionError("Rollback failed.") from rollback_error
            raise DatabaseTransactionError("Transaction failed and was rolled back.") from exc
        finally:
            session.close()  # type: ignore
