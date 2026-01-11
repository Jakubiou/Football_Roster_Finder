class Team:

    def __init__(self, id=None, name="", league="", founded_year=None, budget=0.0):
        '''
        Initializes a new instance of the Team model.
        :param id: The unique identifier of the team (primary key).
        :param name: The name of the football club.
        :param league: The league the team plays in (e.g., '1. LIGA', '2. LIGA').
        :param founded_year: The year the club was established.
        :param budget: The total seasonal or transfer budget of the team.
        '''
        self.id = id
        self.name = name
        self.league = league
        self.founded_year = founded_year
        self.budget = budget

    def __repr__(self):
        '''
        Returns a technical, developer friendly string representation of the instance.
        Used primarily for debugging and logging. If __str__ is not defined,
        Python uses this method as a fallback for print().
        :return: A string showing the internal state of the Contract object.
        '''
        return f"Team(id={self.id}, name='{self.name}', league='{self.league}')"