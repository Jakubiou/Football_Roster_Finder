class Player:

    def __init__(self, id=None, name="", birth_date=None, height=0.0, active=True):
        self.id = id
        self.name = name
        self.birth_date = birth_date
        self.height = height
        self.active = active

    def __repr__(self):
        return f"Player(id={self.id}, name='{self.name}', height={self.height})"