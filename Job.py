import gspread
from pprint import pprint
'''
Eventually, I will need to make a proper database (mongodb or sql) to storage
all this information. Pulling up the data from Google sheet is not ideal since it's a slow
process.

Revisit the idea of have an option to manually update the database (sql or mongo) or automatically
check the google document every 30 seconds or so to find updates in the Google sheet (hash info
to see changes?), transfer any changes to the database and use that database.
'''

class Jobs:
    def __init__(self, title: str, credentials_location: str):
        #  initialize storage
        self.members_dict = {}  # hold the info from each member and their jobs
        #  different storage for no assigned jobs
        self.no_assigned_jobs = {"No assigned jobs": {"points": 0, "jobs":[]}}
        #  connect to google spreadsheet
        self.gc = gspread.service_account(filename=credentials_location)
        self.sheet = self.gc.open(title)  # title: title of the spreadsheet to use
        #  latest sheet in spreadsheet
        self.latest_sheet = self.get_sheet_names()[0]
        #  keep track of points
        self.points = 0
        #  list of members (names need to be unique)
        self.names = set()
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
        if name == "No assigned jobs":
            self.no_assigned_jobs["No assigned jobs"]["jobs"].append((job, points))
            self.no_assigned_jobs["No assigned jobs"]["points"] += points
        else:
            if name not in self.members_dict:
                self.members_dict[name] = {"points": 0}

            if day not in self.members_dict[name]:
                self.members_dict[name][day] = []

            self.members_dict[name][day].append((job, points))
            self.members_dict[name]["points"] += points
            self.points += points
            self.names.add(name)

    def get_no_assigned_jobs(self):
        return dict(self.no_assigned_jobs)
    def get_members_names(self):
        return sorted(list(self.names))

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
        return self.members_dict

a = Jobs("Copy of JS Job Wheel", "./credentials.json")
pprint(a.get_dictionary())
print(a.get_points())
pprint(a.get_no_assigned_jobs())
