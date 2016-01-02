class PartyAnimal:
    x = 0
    name = ''

    # creation (which is common, used to set up variables)
    def __init__(self, nam): # Counstructors can have additional parameters
        self.name = nam
        print self.name, 'constructed'

    def party(self):
        self.x = self.x + 1
        print self.name, 'party count', self.x


class FootballFan(PartyAnimal): # subclass inheriting everything from P.A.
    points = 0

    def touchdown(self):
        self.points = self.points + 7
        self.party()
        print self.name, 'points', self.points


s = PartyAnimal('Sally')
s.party()

j = FootballFan('Jim')
j.party()
j.touchdown()
