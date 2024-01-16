import pandas as pd
from pprint import pprint

# https://docs.google.com/spreadsheets/d/1XTb5lM1OOd4PNZ0O4FawsYIH1We6f-WH9lEkUV6yp0w/edit?usp=sharing
SHEET_ID = '1XTb5lM1OOd4PNZ0O4FawsYIH1We6f-WH9lEkUV6yp0w'
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

    def add_job(self, name: str, job: str, day: str):
        if name not in self.member:
            self.member[name] = {}

        if day not in self.member[name]:
            self.member[name][day] = []

        self.member[name][day].append(job)

    def dict(self):
        return self.member


temp = Jobs()

for i in range(len(df)):

    job = df.values[i][0]
    day = df.values[i][1]
    name = df.values[i][5]
    # if isinstance(job, str) and isinstance(day, str) and isinstance(name, str):
    #     temp.add_job(name.capitalize(), job.capitalize(), day.capitalize())
    # else:
    #     temp.add_job(name, job, day)


pprint(temp.dict())
