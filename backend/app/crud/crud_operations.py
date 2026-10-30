
from typing import Any

from sqlalchemy import select
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError

from app.models.task import Task


def create_task(db: Session, task_data: dict) -> Task:
    """
    Create and save a new task in the database.

    Args:
        db: SQLAlchemy database session.
        task_data: Dictionary containing task information.

    Returns:
        The newly created Task instance.

    Raises:
        SQLAlchemyError: If a database operation fails.
    """
    try:
        new_task = Task(**task_data)

        db.add(new_task)
        db.commit()
        db.refresh(new_task)

        return new_task

    except SQLAlchemyError:
        db.rollback()
        raise


def get_task_by_id(db: Session, task_id: int) -> Task | None:
    """
    Retrieve a task using its primary key.

    Args:
        db: SQLAlchemy database session.
        task_id: ID of the task to retrieve.

    Returns:
        The matching Task instance, or None if not found.

    Raises:
        SQLAlchemyError: If a database operation fails.
    """
    try:
        statement = select(Task).where(Task.id == task_id)

        result = db.execute(statement)

        return result.scalar_one_or_none()

    except SQLAlchemyError:
        db.rollback()
        raise


def get_all_tasks(
    db: Session,
    skip: int = 0,
    limit: int = 10,
) -> list[Task]:
    """
    Retrieve tasks with pagination.

    Args:
        db: SQLAlchemy database session.
        skip: Number of records to skip.
        limit: Maximum number of records to retrieve.

    Returns:
        A list of Task instances.

    Raises:
        ValueError: If pagination arguments are invalid.
        SQLAlchemyError: If a database operation fails.
    """
    if skip < 0:
        raise ValueError("skip cannot be negative")

    if limit < 1:
        raise ValueError("limit must be greater than zero")

    try:
        statement = (
            select(Task)
            .order_by(Task.id)
            .offset(skip)
            .limit(limit)
        )

        result = db.execute(statement)

        return list(result.scalars().all())

    except SQLAlchemyError:
        db.rollback()
        raise


def update_task(
    db: Session,
    task_id: int,
    task_data: dict[str, Any],
) -> Task | None:
    """
    Update an existing task using only supplied fields.

    Args:
        db: SQLAlchemy database session.
        task_id: ID of the task to update.
        task_data: Dictionary containing fields to update.

    Returns:
        The updated Task instance, or None if not found.

    Raises:
        SQLAlchemyError: If a database operation fails.
    """
    try:
        statement = select(Task).where(Task.id == task_id)

        result = db.execute(statement)

        task = result.scalar_one_or_none()

        if task is None:
            return None

        for field, value in task_data.items():
            setattr(task, field, value)

        db.commit()
        db.refresh(task)

        return task

    except SQLAlchemyError:
        db.rollback()
        raise


def delete_task(db: Session, task_id: int) -> Task | None:
    """
    Delete an existing task using its primary key.

    Args:
        db: SQLAlchemy database session.
        task_id: ID of the task to delete.

    Returns:
        The deleted Task instance, or None if not found.

    Raises:
        SQLAlchemyError: If a database operation fails.
    """
    try:
        statement = select(Task).where(Task.id == task_id)

        result = db.execute(statement)

        task = result.scalar_one_or_none()

        if task is None:
            return None

        db.delete(task)
        db.commit()

        return task

    except SQLAlchemyError:
        db.rollback()
        raise
