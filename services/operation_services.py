from datetime import datetime
from models.Operation import Operation
from database.db_mysql import MySQLDatabase

class OperationService:

    @staticmethod
    def create_operation(amount_required, annual_interest, deadline):

        db = MySQLDatabase()
        db.connect()

        insert_query = """
            INSERT INTO operations (amount_required, annual_interest, deadline, status)
            VALUES (%s, %s, %s, %s)
        """
        db.execute_update(insert_query, (amount_required, annual_interest, deadline, 'active'))
        db.disconnect()

        return {"message": "Operation created successfully"}, 201

    @staticmethod
    def list_active_operations():
        db = MySQLDatabase()
        db.connect()

        select_query = "SELECT * FROM operations WHERE status = 'active'"
        active_operations = db.execute_query(select_query)

        operations_list = [{
            "id": op['id'],
            "amount_required": op['amount_required'],
            "annual_interest": op['annual_interest'],
            "deadline": op['deadline'].strftime("%Y-%m-%d")
        } for op in active_operations]
        
        db.disconnect()
        
        return operations_list, 200

    @staticmethod
    def close_operation_if_applicable(operation_id):
        db = MySQLDatabase()
        db.connect()

        select_query = "SELECT * FROM operations WHERE id = %s"
        operation = db.execute_query(select_query, (operation_id,))
        
        if operation:
            operation = operation[0]
            deadline = operation['deadline']
            status = operation['status']

            if datetime.utcnow() > deadline or status == 'closed':
                update_query = "UPDATE operations SET status = 'closed' WHERE id = %s"
                db.execute_update(update_query, (operation_id,))
                db.disconnect()
                return {"message": "Operation closed successfully"}, 200
        
        db.disconnect()
        return {"message": "Operation not found or already closed"}, 404
