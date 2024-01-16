import pandas as pd
from pprint import pprint

# https://docs.google.com/spreadsheets/d/1XTb5lM1OOd4PNZ0O4FawsYIH1We6f-WH9lEkUV6yp0w/edit?usp=sharing
SHEET_ID = '11trob6GMCskw1qbvILMPKBeJlKxTh_b_PfG9Iy80uVo'
SHEET_NAME = 'WINTER_2024'
url = f'https://docs.google.com/spreadsheets/d/{SHEET_ID}/gviz/tq?tqx=out:csv&sheet={SHEET_NAME}'
df = pd.read_csv(url)
'''
{"antonio":{"monday":["day dishes"]
            "tuesday":["night dishes", "mop"]
            "friday":["cook"]}
'''


class Jobs:
    def __init__(self):
        self.member = {}

    def add_job(self, name: str, job: str, day: str, points:int):
        if name not in self.member:
            self.member[name] = {"points": 0}

        if day not in self.member[name]:
            self.member[name][day] = []

        self.member[name][day].append((job, points))
        self.member[name]["points"] += points

    def gather(self):
        for i in range(len(df)):
            job = df.values[i][0]
            day = df.values[i][1]
            name = df.values[i][5]
            points = df.values[i][4]
            if isinstance(name, str):  # if there is no name, then do not add (for now)
                name = name.capitalize()
                if isinstance(day, str):
                    day = day.capitalize()
                else:
                    day = "Coord"
                self.add_job(name.capitalize(), job.capitalize(), day.capitalize(), points)

    def dict(self):
        return self.member


temp = Jobs()

pprint(temp.dict())
