class Player:

    def __init__(self, id=None, name="", birth_date=None, height=0.0, active=True):
        '''
        Initializes a new instance of the Player model.
        :param id: The unique identifier of the player (primary key).
        :param name: The full name of the player.
        :param birth_date: The player's date of birth.
        :param height: The player's height (usually in centimeters or meters).
        :param active: Flag indicating if the player is currently active in the squad.
        '''
        self.id = id
        self.name = name
        self.birth_date = birth_date
        self.height = height
        self.active = active

    def __repr__(self):
        '''
        Returns a technical, developer friendly string representation of the instance.
        Used primarily for debugging and logging. If __str__ is not defined,
        Python uses this method as a fallback for print().
        :return: A string showing the internal state of the Contract object.
        '''
        return f"Player(id={self.id}, name='{self.name}', height={self.height})"