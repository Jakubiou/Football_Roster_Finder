class Position:

    def __init__(self, id=None, name=""):
        '''
        Initializes a new instance of the Position model.
        :param id: The unique identifier of the position (primary key).
        :param name: The shorthand code or name of the position (e.g., 'GK').
        '''
        self.id = id
        self.name = name

    def __repr__(self):
        '''
        Returns a technical, developer friendly string representation of the instance.
        Used primarily for debugging and logging. If __str__ is not defined,
        Python uses this method as a fallback for print().
        :return: A string showing the internal state of the Contract object.
        '''
        return f"Position(id={self.id}, name='{self.name}')"