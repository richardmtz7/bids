from datetime import datetime
from database.db_mysql import MySQLDatabase

class AuctionService:

    @staticmethod
    def place_bid(user_id, operation_id, amount, interest_rate):
        db = MySQLDatabase()
        db.connect()

        select_operation_query = "SELECT * FROM operations WHERE id = %s AND status = 'active'"
        operation = db.execute_query(select_operation_query, (operation_id,))
        
        if not operation:
            db.disconnect()
            return {"message": "Operation not found or already closed"}, 404

        insert_bid_query = """
            INSERT INTO bids (amount, interest_rate, operation_id, user_id, created_At)
            VALUES (%s, %s, %s, %s, %s)
        """
        db.execute_update(insert_bid_query, (amount, interest_rate, operation_id, user_id, datetime.utcnow()))
        
        db.disconnect()

        return {"message": "Bid placed successfully"}, 201

    @staticmethod
    def list_bids_for_operation(operation_id):
        db = MySQLDatabase()
        db.connect()

        select_bids_query = "SELECT * FROM bids WHERE operation_id = %s"
        bids = db.execute_query(select_bids_query, (operation_id,))
        
        bids_list = [{
            "amount": bid['amount'],
            "interest_rate": bid['interest_rate'],
            "user_id": bid['user_id'],
            "created_at": bid['created_At'].strftime("%Y-%m-%d %H:%M:%S")
        } for bid in bids]

        db.disconnect()

        return bids_list, 200
