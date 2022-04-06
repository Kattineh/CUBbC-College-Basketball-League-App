
class Game(object):

    def __init__(self):

        self.week = 0
        self.college_a = ""
        self.college_b = ""
        self.score_a = 0
        self.score_b = 0
        self.winner = ""
        self.time = ""
        self.date = ""
        self.div = 0

    def update(self):
        if self.score_a > self.score_b:
            self.winner = self.college_a
        else:
            if self.score_b > self.score_a:
                self.winner = self.college_b
            else:
                self.winner = "draw"
