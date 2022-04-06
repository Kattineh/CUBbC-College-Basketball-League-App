import os
import csv
import copy
from collections import defaultdict
import tkinter as tk
import tkinter.ttk as ttk
from tkinter import simpledialog as sd
from tkinter import END, filedialog
import pygubu
from team import Team
from game import Game

PROJECT_PATH = os.path.abspath(os.path.dirname(__file__))
PROJECT_UI = os.path.join(PROJECT_PATH, "cubbc_app.ui")

class CubbcApp:
    def __init__(self, master=None):
        self.master = master
        self.teams = {}
        self.games = []
        self.score_data = None
        self.standing_data = None
        self.builder = builder = pygubu.Builder()
        builder.add_resource_path(PROJECT_PATH)
        builder.add_from_file(PROJECT_UI)
        self.mainwindow = builder.get_object('frame1', master)

        self.Logo_PNG = None
        builder.import_variables(self, ['Logo_PNG'])

        self.s = s = ttk.Style()
        s.configure('TFrame', background='white')
        s.configure('TLabel', background='white')
        # Build the menu submenu from XML
        my_menu = builder.get_object('menu1')
        master.config(menu=my_menu)
        master.title("CuBbc App")
        self.teams_window = builder.get_object("scrollbarhelper1")
        self.teams_window.grid_forget()
        self.teams_menu = builder.get_object("listbox1")

        builder.connect_callbacks(self)

    def new(self):

        self.teams_window.grid(row=2, column=0)
        self.divs = sd.askinteger("Number of Divisions", "How many divisions?")

    def load_standings(self):

        file = filedialog.askopenfile(mode='r', initialdir=PROJECT_PATH,
                                      defaultextension='.csv',
                                      filetypes=[("Excel file", ".csv")])
        team_reader = file.readlines()
        record = False
        div = 0
        for index in range(0, len(list(team_reader))):
            row = list(team_reader)[index].strip().split(",")
            if row[0].find("Div") != -1:
                record = False
                div = int(row[0].split("Div")[1])
            if record and row[0] != "":
                print(row)
                team = Team()
                team.div = div
                team.name = row[0]
                team.played = int(row[1])
                team.won = int(row[2])
                team.lost = int(row[3])
                team.draw = int(row[4])
                team.for_team = int(row[5])
                team.against = int(row[6])
                team.pm = int(row[7])
                team.pts = int(row[8])
                self.teams[team.name] = team
            if row[0] == "":
                record = False
            if row[0].find("Team") != -1:
                record = True
        teams_menu = self.teams_menu
        teams_menu.insert(END, *self.teams.keys())
        self.teams_window.grid(row=2, column=0)
        file.close()

    def load_scores(self):

        file = filedialog.askopenfile(mode='r', initialdir=PROJECT_PATH,
                                      defaultextension='.csv',
                                      filetypes=[("Excel file", ".csv")])
        self.teams_window.grid(row=2, column=0)
        game_reader = file.readlines()
        record = False
        week = 0
        for index in range(0, len(list(game_reader))):
            row = list(game_reader)[index].strip().split(",")
            if row[0].find("Week") != -1:
                record = False
                week = int(row[0].split("Week")[1])
            if record and row[0] != "":
                game = Game()
                game.week = week
                game.college_a = row[0]
                game.college_b = row[1]
                game.score_a = int(row[2])
                game.score_b = int(row[3])
                game.update()
                game.time = row[5]
                game.date = row[6]
                game.div = row[7]
                self.games.append(game)
            if row[0] == "":
                record = False
            if row[0].find("College A") != -1:
                record = True
        file.close()
        self.display()

    def save(self):

            # Scores
            d = defaultdict(list)
            for i in self.games:
                d[i.week].append(i)
            results = []
            for games in list(d.values()):
                title = ['College A', 'College B', 'Score A', 'Score B',
                         'Winner', 'Time', 'Date']
                results.append(["Week"+str(games[0].week)])
                results.append(title)
                games.sort(key=lambda x: (x.date, x.time))
                for game in games:
                    new_list = [game.college_a, game.college_b, game.score_a,
                                game.score_b, game.winner, game.time, game.date,
                                game.div]
                    results.append(new_list)
            self.score_data = results
            self.update_standings()

            # Standings
            d = defaultdict(list)
            for i in list(self.teams.values()):
                d[i.div].append(i)
            results = []
            nums = list(d.keys())
            nums.sort()
            for teams in nums:
                title = ['Team', 'Played', 'Won', 'Lost',
                         'Draw', 'For', 'Against', '+/-', 'Pts.']
                results.append(["Div"+str(d[teams][0].div)])
                results.append(title)
                #teams = copy.deepcopy(list(self.teams.values()))
                d[teams].sort(key=lambda x: (x.pts, x.pm), reverse=True)
                for team in d[teams]:
                    new_list = [team.name, team.played, team.won, team.lost,
                                team.drawn, team.for_team, team.against,
                                team.pm, team.pts]
                    results.append(new_list)
            self.standing_data = results

    def update_standings(self):

        for game in self.games:
            team_a = None
            team_b = None
            if not game.college_a in self.teams.keys():
                team_a = Team()
                team_a.name = game.college_a
                team_a.div = game.div
                self.teams[game.college_a] = team_a
            else:
                team_a = self.teams[game.college_a]
            if not game.college_b in self.teams.keys():
                team_b = Team()
                team_b.name = game.college_b
                team_b.div = game.div
                self.teams[game.college_b] = team_b
            else:
                team_b = self.teams[game.college_b]
            team_a.inc_played()
            team_b.inc_played()
            if game.score_a > game.score_b:
                team_a.inc_won()
                team_b.inc_lost()
            else:
                if game.score_a == game.score_b:
                    team_a.inc_drawn()
                    team_b.inc_drawn()
                else:
                    team_a.inc_lost()
                    team_b.inc_won()
            team_a.inc_for(game.score_a)
            team_a.inc_against(game.score_b)
            team_b.inc_for(game.score_b)
            team_b.inc_against(game.score_a)
            team_a.update_pm()
            team_b.update_pm()
            team_a.update_pts()
            team_b.update_pts()


    def print_scores(self):

        file = filedialog.asksaveasfile(initialdir=PROJECT_PATH,
                                        defaultextension='.csv',
                                        filetypes=[("Excel file", ".csv")])
        name = os.path.basename(file.name)
        with open(name, 'w', newline='') as csvfile:
            csvfile.truncate()
            game_writer = csv.writer(csvfile)
            game_writer.writerows(self.score_data)
        csvfile.close()

    def print_standings(self):

        file = filedialog.asksaveasfile(initialdir=PROJECT_PATH,
                                        defaultextension='.csv',
                                        filetypes=[("Excel file", ".csv")])
        name = os.path.basename(file.name)
        with open(name, 'w', newline='') as csvfile:
            csvfile.truncate()
            team_writer = csv.writer(csvfile)
            team_writer.writerows(self.standing_data)
        csvfile.close()

    def display(self):

        for game in self.games:
            team_a = None
            team_b = None
            if not game.college_a in self.teams.keys():
                team_a = Team()
                team_a.name = game.college_a
                team_a.div = game.div
                self.teams[game.college_a] = team_a
            else:
                team_a = self.teams[game.college_a]
            if not game.college_b in self.teams.keys():
                team_b = Team()
                team_b.name = game.college_b
                team_b.div = game.div
                self.teams[game.college_b] = team_b
            else:
                team_b = self.teams[game.college_b]
        teams_menu = self.teams_menu
        sp = "                        "
        for team in self.teams.keys():
            sp = (25-len(team))*" "
            teams_menu.insert(END, team+sp+str(teams_menu.size()+1))
        self.teams_window.grid(row=2, column=0)


    def insert_team(self):

        name = sd.askstring("Team's Name", "Enter the team's name:")
        div = sd.askinteger("Team's Division", "Enter the team's division:")
        team = Team()
        team.name = name
        team.div = div
        teams_menu = self.teams_menu
        sp = (25-len(name))*" "
        teams_menu.insert(END, name+sp+str(teams_menu.size()))
        self.teams[name] = team

    def insert_game(self):

        name = sd.askstring

    def close(self):
        self.master.quit()  # Closes the app

    def run(self):
        self.mainwindow.mainloop()

if __name__ == '__main__':
    root = tk.Tk()
    app = CubbcApp(root)
    app.run()
