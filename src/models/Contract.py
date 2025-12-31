class Contract:

    def __init__(self, id=None, salary=0.0, type="", valid_from=None, valid_to=None):
        self.id = id
        self.salary = salary
        self.type = type
        self.valid_from = valid_from
        self.valid_to = valid_to

    def __repr__(self):
        return f"Contract(id={self.id}, type='{self.type}', salary={self.salary})"