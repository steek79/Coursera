class PartyAnimal:
    x = 0

    def __init__(self): # creation (which is common, used to set up variables)
        print 'I am constructed'

    def party(self):
        self.x = self.x + 1
        print 'So far', self.x

    def __del__(self): # destruction (which is rare)
        print 'I am destructed', self.x


an = PartyAnimal()

an.party()
an.party()
an.party()
