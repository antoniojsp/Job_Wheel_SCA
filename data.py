import gspread
import pandas as pd
from pprint import pprint
from math import isnan


class Jobs:
    def __init__(self, sheet_id: str, sheet_name: str):
        self.members = {"No assigned jobs": []}
        self.sheet_id = sheet_id
        self.sheet_name = sheet_name
        self.pull_info_from_sheet()

    def add_job(self, name: str, job: str, day: str, points: int):
        if name not in self.members:
            self.members[name] = {"points": 0}

        if day not in self.members[name]:
            self.members[name][day] = []

        self.members[name][day].append((job, points))
        self.members[name]["points"] += points

    def no_assigned_jobs(self, job: str) -> None:
        self.members["No assigned jobs"].append(job)

    def pull_info_from_sheet(self) -> None:
        url = f'https://docs.google.com/spreadsheets/d/{self.sheet_id}/gviz/tq?tqx=out:csv&sheet={self.sheet_name}'
        df = pd.read_csv(url)

        for i in range(len(df)):
            job = df.values[i][0]
            day = df.values[i][1]
            name = df.values[i][5]
            points = float(df.values[i][4]) if not isnan(df.values[i][4]) else 0

            if isinstance(name, str):  # if there is no name, then do not add (for now)
                name = name.capitalize()
                if isinstance(day, str):
                    day = day.capitalize()
                else:
                    day = "Coord"  # if it's not a day of the week or weekly/bi-weekly job, then is a coord job.
                self.add_job(name.capitalize(), job.capitalize(), day.capitalize(), points)
            else:
                self.no_assigned_jobs((day, job, points))

    def dict(self):
        return self.members


SHEET_ID = '11trob6GMCskw1qbvILMPKBeJlKxTh_b_PfG9Iy80uVo'
SHEET_NAME = 'WINTER_2024'
temp = Jobs(SHEET_ID, SHEET_NAME)
pprint(temp.dict())
