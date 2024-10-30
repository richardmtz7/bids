class Bid():
    def __init__(self, id, amount, interest_rate, operation_id, user_id, created_At) -> None:
        self.id = id
        self.amount = amount
        self.interest_rate = interest_rate
        self.operation_id = operation_id
        self.user_id = user_id
        self.created_At = created_At
    
    def to_json(self):
        return{
            'id': self.id,
            'amount': self.amount,
            'interest_rate': self.interest_rate,
            'operation_id': self.operation_id,
            'user_id': self.user_id,
            'created_At': self.created_At
        }