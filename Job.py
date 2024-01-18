import gspread
from pprint import pprint


class Jobs:
    def __init__(self, title: str, credentials_location: str):
        #  initialize storage
        self.members = {"No assigned jobs": {"points": 0}}  # hold the info from each member and their jobs
        #  connect to google spreadsheet
        self.gc = gspread.service_account(filename=credentials_location)
        self.sheet = self.gc.open(title)  # title: title of the spreadsheet to use
        #  latest sheet in spreadsheet
        self.latest_sheet = self.get_sheet_names()[0]
        #  keep track of points
        self.points = 0
        #  pull information from Google Sheets
        self.fill_up_from_sheet()

    def get_points(self):
        return self.points

    def add_job_info(self, name: str, day: str, job: str, points: float) -> None:
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
        self.points += points

    def get_sheet_names(self) -> list:
        return [s.title for s in self.sheet.worksheets()]  # sheet names (to select the current or past sheet)

    def fill_up_from_sheet(self) -> None:
        entire_sheet = self.sheet.worksheet(self.get_sheet_names()[0])  # currently, only selects the most recent job
        # wheel schedule

        for row in entire_sheet.get()[1:]:
            '''
            Currently, there is no established format to fill up the google doc file
            for the job wheel. These inconsistencies need to be fixed by selecting
            an appropriate format and be consistent with it. I added some value checkers to make sure the data
            is mostly correct
            '''
            length = len(row)
            if length < 6:  # every row is sent as a list. If one list has less than 6 items, then one
                # extra is added so it can be processed. This is due to the lack of consitency from the
                # spreadsheet side.
                row.append("")

            job = row[0]
            day = row[1]
            name = row[5]
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

            if day and day.capitalize() in ["Monday",
                                            "Tuesday",
                                            "Wednesday",
                                            "Thursday",
                                            "Friday",
                                            "Saturday",
                                            "Sunday",
                                            "Biweekly",
                                            "Weekly"]:
                day = day.capitalize()
            else:
                day = "Coord"  # if it's not a day of the week or weekly/bi-weekly job, then is a coord job.
            self.add_job_info(name.capitalize(), day.capitalize(), job.capitalize(), points)

    def get_dictionary(self) -> dict:
        return self.members


# a = Jobs("Copy of JS Job Wheel", "./credentials.json")
# pprint(a.get_dictionary())
# print(a.get_points())
