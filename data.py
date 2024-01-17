import gspread
from pprint import pprint


class Jobs:
    def __init__(self, credentials):
        self.credentials = credentials
        self.members = {"No assigned jobs": {"points": 0}} # starts by adding jobs that are not covered
        self.pull_info_from_sheet(credentials)

    def add_job(self, name: str, day: str, jobs_points: tuple[str, str]) -> None:
        """
        add a job, indicating the member assigned, the day, the name of the job and how
        mamy points the member gets
        :param name: name of member
        :param day: day of the week, or if it's weekly, biweekly or coord
        :param jobs_points:
        :return:
        """
        if name not in self.members:
            self.members[name] = {"points": 0}

        if day not in self.members[name]:
            self.members[name][day] = []

        self.members[name][day].append(jobs_points)
        self.members[name]["points"] += jobs_points[1]

    def pull_info_from_sheet(self, credentials: str) -> None:
        gc = gspread.service_account(filename=credentials)

        sh = gc.open("Copy of JS Job Wheel")
        sheet_names = [s.title for s in sh.worksheets()]
        a = sh.worksheet(sheet_names[0])

        for row in a.get()[1:]:
            length = len(row)
            if length < 6:
                row.append("")

            job = row[0] if row[0] else ""
            day = row[1] if row[1] else ""
            name = row[5] if row[5] else ""
            points = row[4]
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
            job_points = (job, points)
            self.add_job(name.capitalize(), day.capitalize(), job_points)

    def dict(self):
        return self.members


a = Jobs("./credentials.json")
pprint(a.dict())
num = 0
for i in a.dict():
    num += a.dict()[i]["points"]

print(num)
