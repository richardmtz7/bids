class Operation():

    def __init__(self, id, amount_required, annual_interest, deadline, status) -> None:
        self.id = id
        self.amount_required = amount_required
        self.annual_interest = annual_interest
        self.deadline = deadline
        self.status = status

    def to_json(self):
        return {
            'id': self.id,
            'amount_required': self.amount_required,
            'annual_interest': self.annual_interest,
            'deadline': self.deadline,
            'status': self.status
        }