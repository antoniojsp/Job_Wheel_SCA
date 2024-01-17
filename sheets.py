import gspread
from pprint import pprint


class Jobs:
    def __init__(self, title:str,  credentials_location:str):
        #  initialize storage
        self.members = {"No assigned jobs": {"points": 0}}  # hold the info from each member and their jobs
        #  connect to spreadsheet
        self.gc = gspread.service_account(filename=credentials_location)
        self.sheet = self.gc.open(title)
        #  latest sheet in spreadsheet
        self.latest_sheet = self.get_sheet_names()[0]
        #  keep track of points
        self.points = 0
        #  pull information from Google Sheets
        self.pull_info_from_sheet()


    def  get_points(self):
        return self.points

    def add_job_info(self, name: str, day: str, job:str, points:float) -> None:
        """
        add a job, indicating the member assigned, the day, the name of the job and how
        mamy points the member gets
        :param name: name of member
        :param day: day of the week, or if it's weekly, biweekly or coord
        :param job: string with name of the job
        :param points: float with value of points per job
        """
        if name not in self.members:
            self.members[name] = {"points": 0}

        if day not in self.members[name]:
            self.members[name][day] = []

        self.members[name][day].append((job, points))
        self.members[name]["points"] += points

    def get_sheet_names(self) -> list:
        return [s.title for s in self.sheet.worksheets()]  # sheet names (to select the current or past sheet)

    def pull_info_from_sheet(self) -> None:
        entire_sheet = self.sheet.worksheet(self.get_sheet_names()[0])  # currently, only selects the most recent job wheel schedule

        for row in entire_sheet.get()[1:]:
            '''
            Currently, there is no established format to fill up the google doc file
            for the job wheel. These inconsistencies need to be fixed by selecting
            an appropriate format. Some tricks have been used to avoid problems due
            the inconsistent former used by the members.
            '''
            length = len(row)
            if length < 6:
                row.append("")

            job = row[0] if row[0] else ""
            day = row[1] if row[1] else ""
            name = row[5] if row[5] else ""
            points = row[4]

            '''
            If points are not added in the google sheet or if no numbers are added, they are set to zero.
            '''
            try:
                points = float(points)
            except ValueError:
                points = 0

            if len(name) > 0:  # if there is no name, then do not add (for now)
                name = name.capitalize()
            else:
                name = "No assigned jobs"

            if day:
                day = day.capitalize()
            else:
                day = "Coord"  # if it's not a day of the week or weekly/bi-weekly job, then is a coord job.
            self.add_job_info(name.capitalize(), day.capitalize(), job.capitalize(), points)

    def dict(self):
        return self.members


a = Jobs("Copy of JS Job Wheel", "./credentials.json")
pprint(a.dict())
print(a.get_points())
