#!/usr/bin/env python3.13
# Copyright (C) 2025 All rights reserved.
# FILENAME:    ~~/src/asyncpg/exceptions.pyi
# VERSION:     0.1.0
# CREATED:     2025-06-26 12:49
# AUTHOR:      Sitt Guruvanich <aekazitt+github@gmail.com>
# DESCRIPTION:
#
# HISTORY:
# *************************************************************

class PostgresMessageMeta(type):
  def __instancecheck__(cls, instance: "PostgresMessage") -> bool:
    """TODO"""

class PostgresMessage(metaclass=PostgresMessageMeta):
  """TODO"""

class PostgresError(PostgresMessage, Exception):
  """TODO"""

class ConnectionDoesNotExistError(PostgresError):
  """Exception raised when connection does not exist."""

  pass

class ConnectionFailureError(PostgresError):
  """Exception raised when connection fails."""

  pass

class QueryCanceledError(PostgresError):
  """Exception raised when query is canceled."""

  pass

class InvalidPasswordError(PostgresError):
  """Exception raised when password is invalid."""

  pass

class InvalidAuthorizationSpecificationError(PostgresError):
  """Exception raised when authorization specification is invalid."""

  pass

class InvalidParameterValueError(PostgresError):
  """Exception raised when parameter value is invalid."""

  pass

class InvalidTransactionStateError(PostgresError):
  """Exception raised when transaction state is invalid."""

  pass

class UndefinedTableError(PostgresError):
  """Exception raised when table is undefined."""

  pass

class UndefinedColumnError(PostgresError):
  """Exception raised when column is undefined."""

  pass

class DuplicateTableError(PostgresError):
  """Exception raised when table already exists."""

  pass

class DuplicateColumnError(PostgresError):
  """Exception raised when column already exists."""

  pass

class UniqueViolationError(PostgresError):
  """Exception raised when unique constraint is violated."""

  pass

class ForeignKeyViolationError(PostgresError):
  """Exception raised when foreign key constraint is violated."""

  pass

class CheckViolationError(PostgresError):
  """Exception raised when check constraint is violated."""

  pass

class NotNullViolationError(PostgresError):
  """Exception raised when not null constraint is violated."""

  pass

class DataError(PostgresError):
  """Exception raised for data errors."""

  pass

class IntegrityError(PostgresError):
  """Exception raised for integrity errors."""

  pass

class OperationalError(PostgresError):
  """Exception raised for operational errors."""

  pass

class ProgrammingError(PostgresError):
  """Exception raised for programming errors."""

  pass

__all__: tuple[str, ...] = (
  "PostgresError",
  "ConnectionDoesNotExistError",
  "ConnectionFailureError",
  "QueryCanceledError",
  "InvalidPasswordError",
  "InvalidAuthorizationSpecificationError",
  "InvalidParameterValueError",
  "InvalidTransactionStateError",
  "UndefinedTableError",
  "UndefinedColumnError",
  "DuplicateTableError",
  "DuplicateColumnError",
  "UniqueViolationError",
  "ForeignKeyViolationError",
  "CheckViolationError",
  "NotNullViolationError",
  "DataError",
  "IntegrityError",
  "OperationalError",
  "ProgrammingError",
)
