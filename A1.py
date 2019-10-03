
class State():

    def __init__(self, cannibalLeft, missionaryLeft, boat, cannibalRight, missionaryRight):
        self.cannibalLeft = cannibalLeft
        self.missionaryLeft = missionaryLeft
        self.boat = boat
        self.cannibalRight = cannibalRight
        self.missionaryRight = missionaryRight
        self.parent = None

    def is_valid(self):
        if self.missionaryLeft >= 0 and self.missionaryRight >= 0:
            if self.cannibalLeft >= 0 and self.cannibalRight >= 0:
                if self.missionaryLeft == 0 or self.missionaryLeft >= self.cannibalLeft:
                    if self.missionaryRight == 0 or self.missionaryRight >= self.cannibalRight:
                        return True
        return False