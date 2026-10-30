
import pytest

from sqlalchemy import delete
from sqlalchemy.exc import IntegrityError

from app.models.task import Task
from app.crud.crud_operations import (
    create_task,
    get_task_by_id,
    get_all_tasks,
    update_task,
    delete_task,
)


def clean_tasks(db_session):
    """Remove existing test records before each test."""
    db_session.execute(delete(Task))
    db_session.commit()


def test_get_task_by_id_success(db_session):
    clean_tasks(db_session)

    task_data = {
        "title": "Learn FastAPI",
        "description": "Learn API development",
        "priority": "high",
        "status": "pending",
    }

    created_task = create_task(db_session, task_data)

    result = get_task_by_id(db_session, created_task.id)

    assert result is not None
    assert result.id == created_task.id
    assert result.title == "Learn FastAPI"


def test_get_task_by_id_not_found(db_session):
    clean_tasks(db_session)

    result = get_task_by_id(db_session, 99999)

    assert result is None


def test_get_all_tasks_success(db_session):
    clean_tasks(db_session)

    create_task(db_session, {
        "title": "Task One",
        "priority": "low",
        "status": "pending",
    })

    create_task(db_session, {
        "title": "Task Two",
        "priority": "medium",
        "status": "pending",
    })

    create_task(db_session, {
        "title": "Task Three",
        "priority": "high",
        "status": "completed",
    })

    result = get_all_tasks(db_session)

    assert len(result) == 3
    assert result[0].title == "Task One"
    assert result[1].title == "Task Two"
    assert result[2].title == "Task Three"


def test_get_all_tasks_pagination(db_session):
    clean_tasks(db_session)

    for number in range(1, 6):
        create_task(db_session, {
            "title": f"Task {number}",
            "priority": "medium",
            "status": "pending",
        })

    result = get_all_tasks(db_session, skip=2, limit=2)

    assert len(result) == 2
    assert result[0].title == "Task 3"
    assert result[1].title == "Task 4"


@pytest.mark.parametrize(
    ("skip", "limit"),
    [
        (-1, 10),
        (0, 0),
        (0, -1),
    ],
)
def test_get_all_tasks_invalid_pagination(db_session, skip, limit):
    with pytest.raises(ValueError):
        get_all_tasks(db_session, skip=skip, limit=limit)


def test_update_task_success(db_session):
    clean_tasks(db_session)

    task = create_task(db_session, {
        "title": "Learn FastAPI",
        "description": "Original description",
        "priority": "medium",
        "status": "pending",
    })

    updated_task = update_task(
        db_session,
        task.id,
        {"priority": "high"},
    )

    assert updated_task is not None
    assert updated_task.priority == "high"
    assert updated_task.title == "Learn FastAPI"
    assert updated_task.description == "Original description"
    assert updated_task.status == "pending"


def test_update_task_not_found(db_session):
    clean_tasks(db_session)

    result = update_task(
        db_session,
        99999,
        {"priority": "high"},
    )

    assert result is None


def test_update_task_invalid_priority(db_session):
    clean_tasks(db_session)

    task = create_task(db_session, {
        "title": "Learn FastAPI",
        "priority": "medium",
        "status": "pending",
    })

    with pytest.raises(IntegrityError):
        update_task(
            db_session,
            task.id,
            {"priority": "urgent"},
        )

    assert db_session.is_active

    # Verify that rollback preserved the original value.
    db_session.expire_all()

    result = get_task_by_id(db_session, task.id)

    assert result is not None
    assert result.priority == "medium"


def test_delete_task_success(db_session):
    clean_tasks(db_session)

    task = create_task(db_session, {
        "title": "Task to delete",
        "priority": "medium",
        "status": "pending",
    })

    deleted_task = delete_task(db_session, task.id)

    assert deleted_task is not None
    assert deleted_task.id == task.id

    result = get_task_by_id(db_session, task.id)

    assert result is None


def test_delete_task_not_found(db_session):
    clean_tasks(db_session)

    result = delete_task(db_session, 99999)

    assert result is None
