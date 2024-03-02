import gspread
from pprint import pprint

'''
Eventually, I will need to make a proper database (mongodb or sql) to storage
all this information. Pulling up the data from Google sheet is not ideal since it's a slow
process.

Revisit the idea of have an option to manually update the database (sql or mongo) or automatically
check the google document every 30 seconds or so to find updates in the Google sheet (hash info
to see changes?), transfer any changes to the database and use that database.

UPDATE:
The Jobs class pull the information from the google sheet, format it as a dict and
get it ready to be stored in MongoDB atlas, for faster access by the flask server

Example:
data_term = {"Current term name": "name of the current term,
             "No assigned jobs": "Dict with the jobs that haven't been assigned and the total points",
             "Assigned jobs": "Dict with all the jobs assigned, with the name of the member, the jobs and points",
             "General points": "total of points of no assigned and assigned jobs",
             "Members names": "list of names of all the members for the dropdown list in flask"}
'''


class Jobs:
    def __init__(self, title: str, credentials_location: str):
        #  initialize storage
        self.assigned_jobs = {"Total points": 0}  # hold the info from each member and their jobs
        #  different storage for no assigned jobs
        self.no_assigned_jobs = {"Jobs": [], "Total points": 0}
        #  connect to google spreadsheet
        self.gc = gspread.service_account(filename=credentials_location)
        self.sheet = self.gc.open(title)  # title: title of the spreadsheet to use
        #  get all the sheet names but we use the first one that it's the current term.
        self.current_sheet_name = self.get_sheet_names()[0]
        #  keep track of the total points of all the jobs (assigned and no assigned)
        self.points = 0
        #  list of members (names need to be unique)
        self.names = set()
        #  pull information from Google Sheets and creates the dict to be used by mongodb
        self.fill_up_from_sheet()

    def get_points(self) -> int:
        '''
        gets the sum of all the points of ALL the jobs (assigned and unassigned)
        :return: INT
        '''
        return self.points

    def fill_up_from_sheet(self) -> None:
        entire_sheet = self.sheet.worksheet(self.current_sheet_name)  # currently, only selects the most recent job
        # wheel schedule
        for row in entire_sheet.get()[1:]:
            '''
            Currently, there is no established format to fill up the google doc file
            for the job wheel. These inconsistencies need to be fixed by selecting
            an appropriate format and be consistent with it. I added some value checkers to make sure the data
            is stored correctly
            '''
            length = len(row)
            if length < 6:  # every row is sent as a list. If one list has less than 6 items, then one
                # extra is added so it can be processed. This is due to the lack of consitency from the
                # spreadsheet side.
                row.append("")

            job = row[0]
            if job == "":
                continue
            day = row[1]
            name = row[5].strip()
            points = row[4]
            '''
            If points are not presented, it catch the error and set it to zero,
            '''
            try:
                points = float(points)
            except ValueError:
                points = 0

            if not name or name == "NA":
                name = "No assigned jobs"
            else:  # if there is no name, then do not add (for now)
                name = name.capitalize()

            if day and day.capitalize() in ["Monday",
                                            "Tuesday",
                                            "Wednesday",
                                            "Thursday",
                                            "Friday",
                                            "Saturday",
                                            "Sunday",
                                            "Biweekly",
                                            "Weekly",
                                            "Biweekly"]:
                day = day.capitalize()
            else:
                day = "Coord"  # if it's not a day of the week or weekly/bi-weekly job, then is a coord job.
            self.add_job_info(name.capitalize(), day.capitalize(), job.capitalize(), points)

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

            self.no_assigned_jobs["Jobs"].append((day, job, points))
            self.no_assigned_jobs["Total points"] += points
        else:
            if name not in self.assigned_jobs:
                self.assigned_jobs[name] = {"Total points": 0}

            if day not in self.assigned_jobs[name]:
                self.assigned_jobs[name][day] = []

            self.assigned_jobs[name][day].append((job, points))
            self.assigned_jobs[name]["Total points"] += points
            self.names.add(name)
            self.assigned_jobs["Total points"] += points
        self.points += points

    def get_no_assigned_jobs(self) -> dict:
        '''
        Gets all the unassigned jobs (day, job, points)
        :return:
        '''
        return self.no_assigned_jobs

    def get_assigned_jobs(self) -> dict:
        return self.assigned_jobs

    def get_members_names(self):
        return sorted(list(self.names))

    def get_sheet_names(self) -> list:
        return [s.title for s in self.sheet.worksheets()]  # sheet names (to select the current or past sheet)

    def get_full_dict(self):
        data_term = {"Current term name": self.current_sheet_name,
                     "No assigned jobs": self.no_assigned_jobs,
                     "Assigned jobs": self.assigned_jobs,
                     "General points": self.points,
                     "Members names": list(self.names)}
        return data_term

#
# a = Jobs("JS Job Wheel", "./credentials.json")
# pprint(a.get_full_dict())
