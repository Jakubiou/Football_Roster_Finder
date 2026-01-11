class Contract:
    '''
    Represents a contractual agreement for a player, including financial and temporal details.
    '''

    def __init__(self, id=None, salary=0.0, type="", valid_from=None, valid_to=None):
        '''
        Initializes a new instance of the Contract model.
        :param id: The unique identifier of the contract (usually provided by the database).
        :param salary: The monetary value of the contract.
        :param type: The category of the contract (e.g., 'PROFESSIONAL', 'AMATEUR', 'LOAN').
        :param valid_from: The start date of the contract's validity.
        :param valid_to: The end date of the contract's validity.
        '''
        self.id = id
        self.salary = salary
        self.type = type
        self.valid_from = valid_from
        self.valid_to = valid_to

    def __repr__(self):
        '''
        Returns a technical, developer friendly string representation of the instance.
        Used primarily for debugging and logging. If __str__ is not defined,
        Python uses this method as a fallback for print().
        :return: A string showing the internal state of the Contract object.
        '''
        return f"Contract(id={self.id}, type='{self.type}', salary={self.salary})"