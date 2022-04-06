

class Team(object):

    def __init__(self):

        self.name = ""
        self.div = 0
        self.played = 0
        self.won = 0
        self.lost = 0
        self.drawn = 0
        self.for_team = 0
        self.against = 0
        self.pm = 0 # +/-
        self.pts = 0

    def update_div(self, num):

        self.div = num

    def inc_played(self):

        self.played += 1

    def inc_won(self):

        self.won += 1

    def inc_lost(self):

        self.lost += 1

    def inc_drawn(self):

        self.drawn += 1

    def inc_for(self, num):

        self.for_team += num

    def inc_against(self, num):

        self.against += num

    def update_pm(self):

        self.pm = self.for_team-self.against

    def update_pts(self):

        self.pts = 2*self.won + self.drawn

    def generate(self):

        result = []
        result.append(self.name)
        result.append(self.played)
        result.append(self.won)
        result.append(self.lost)
        result.append(self.Drawn)
        result.append(self.for_team)
        result.append(self.against)
        result.append(self.pm)
        result.append(self.pts)
        return result
