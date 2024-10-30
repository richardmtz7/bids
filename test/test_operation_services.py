import unittest
from unittest.mock import patch, MagicMock
from datetime import datetime, timedelta
from services.operation_services import OperationService

@patch("database.db_mysql.MySQLDatabase")
def test_create_operation_success(mock_db):
    mock_db_instance = mock_db.return_value
    mock_db_instance.execute_update.return_value = None

    operation_service = OperationService() 
    response, status = operation_service.create_operation(10000, 5.0, datetime(2025, 1, 1))
    assert status == 201
    assert response["message"] == "Operation created successfully"

@patch("database.db_mysql.MySQLDatabase")
def test_list_active_operations(mock_db):
    mock_db_instance = mock_db.return_value

    mock_db_instance.execute_query.return_value = None
    operation_service = OperationService() 
    operation_service.create_operation(20000, 3.0, datetime(2025, 1, 10))

    response, status = OperationService.list_active_operations()

    assert status == 200
    assert len(response) == 2
    assert response[0]["id"] == response[0]["id"]
    assert response[1]["annual_interest"] == 3.0

@patch("database.db_mysql.MySQLDatabase")
def test_close_operation_if_applicable(mock_db):

    mock_db_instance = mock_db.return_value

    mock_db_instance.execute_query.return_value = [{'id': 1, 'deadline': datetime.utcnow() - timedelta(days=1), 'status': 'active'}]
    mock_db_instance.execute_update.return_value = None

    response, status = OperationService.close_operation_if_applicable(11)

    assert status == 200
    assert response["message"] == "Operation closed successfully"

@patch("database.db_mysql.MySQLDatabase")
def test_close_operation_not_found(mock_db):

    mock_db_instance = mock_db.return_value

    mock_db_instance.execute_query.return_value = []

    response, status = OperationService.close_operation_if_applicable(99)

    assert status == 404
    assert response["message"] == "Operation not found or already closed"

@patch("database.db_mysql.MySQLDatabase")
def test_close_operation_already_closed(mock_db):

    mock_db_instance = mock_db.return_value
    mock_db_instance.execute_query.return_value = [{'id': 1, 'deadline': datetime.utcnow() - timedelta(days=1), 'status': 'closed'}]

    response, status = OperationService.close_operation_if_applicable(1)

    assert status == 404
    assert response["message"] == "Operation not found or already closed"
