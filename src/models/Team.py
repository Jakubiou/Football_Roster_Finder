class Team:

    def __init__(self, id=None, name="", league="", founded_year=None, budget=0.0):
        self.id = id
        self.name = name
        self.league = league
        self.founded_year = founded_year
        self.budget = budget

    def __repr__(self):
        return f"Team(id={self.id}, name='{self.name}', league='{self.league}')"