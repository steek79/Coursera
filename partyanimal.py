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


s = PartyAnimal('Sally')
s.party()

j = PartyAnimal('jim')
j.party()
s.party()

# s and j are independent instances
