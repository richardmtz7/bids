from flask import Blueprint, request, jsonify
from services.auction_services import AuctionService

auction_bp = Blueprint('auction_bp', __name__)

@auction_bp.route('/bid', methods=['POST'])
def place_bid():
    data = request.get_json()

    required_fields = ["user_id", "operation_id", "amount", "interest_rate"]
    if not data or not all(field in data for field in required_fields):
        return jsonify({"message": "Missing required data"}), 400
    
    try:
        response, status = AuctionService.place_bid(
            user_id=data['user_id'],
            operation_id=data['operation_id'],
            amount=data['amount'],
            interest_rate=data['interest_rate']
        )
        return jsonify(response), status
    except ValueError as e:
        return jsonify({"message": str(e)}), 400

@auction_bp.route('/bids/<int:operation_id>', methods=['GET'])
def list_bids(operation_id):
    response, status = AuctionService.list_bids_for_operation(operation_id)
    return jsonify(response), status
