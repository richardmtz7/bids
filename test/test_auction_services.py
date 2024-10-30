import unittest
from unittest.mock import patch, MagicMock
from datetime import datetime
from services.auction_services import AuctionService

class TestAuctionService(unittest.TestCase):

    @patch("database.db_mysql.MySQLDatabase")
    def test_place_bid_success(self, mock_db):
        mock_db_instance = mock_db.return_value

        mock_db_instance.execute_query.return_value = [{'id': 1, 'status': 'active'}]

        mock_db_instance.execute_update.return_value = None
        response, status = AuctionService.place_bid(1, 1, 1000, 5.0)

        self.assertEqual(status, 201)
        self.assertEqual(response["message"], "Bid placed successfully")

    @patch("database.db_mysql.MySQLDatabase")
    def test_place_bid_operation_not_found(self, mock_db):
        mock_db_instance = mock_db.return_value

        mock_db_instance.execute_query.return_value = []

        response, status = AuctionService.place_bid(1, 99, 1000, 5.0)

        self.assertEqual(status, 404)
        self.assertEqual(response["message"], "Operation not found or already closed")

    @patch("database.db_mysql.MySQLDatabase")
    def test_list_bids_for_operation(self, mock_db):
        mock_db_instance = mock_db.return_value

        mock_db_instance.execute_query.return_value = [
            {'amount': 1000, 'interest_rate': 5.0, 'user_id': 1, 'created_at': datetime(2024, 10, 25, 12, 0)}
        ]

        response, status = AuctionService.list_bids_for_operation(1)

        self.assertEqual(status, 200)
        self.assertEqual(len(response), 1)
        self.assertEqual(response[0]["amount"], 1000)
        self.assertEqual(response[0]["interest_rate"], 5.0)

    @patch("database.db_mysql.MySQLDatabase")
    def test_list_bids_for_operation_no_bids(self, mock_db):

        mock_db_instance = mock_db.return_value

        mock_db_instance.execute_query.return_value = []

        response, status = AuctionService.list_bids_for_operation(1)

        self.assertEqual(status, 200)
        self.assertEqual(len(response), 0)

if __name__ == '__main__':
    unittest.main()
