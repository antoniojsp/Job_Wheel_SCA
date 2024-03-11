from pprint import pprint
from gather_cells import GatherCellsFromGoogle


class MemberJobs:
    def __init__(self, data: list):
        self.data: list[str] = data
        self.assigned_jobs: dict = {"Total points": 0}  # hold the info from each member and their jobs
        #  different storage for no assigned jobs
        self.no_assigned_jobs: dict = {"Jobs": [], "Total points": 0}
        #  current term's sheet name
        self.current_sheet_name: str = data[0]
        #  keep track of the total points of all the jobs (assigned and no assigned)
        self.points: float = 0
        #  list of members (names need to be unique)
        self.names: set[str] = set()
        #  pull information from Google Sheets and creates the dict to be used by mongodb
        self.fill_up_from_sheet()

    def fill_up_from_sheet(self) -> None:
        # wheel schedule
        for job, day, points, name in self.data[1:]:
            '''
            Currently, there is no established format to fill up the google doc file
            for the job wheel. These inconsistencies need to be fixed by selecting
            an appropriate format and be consistent with it. I added some value checkers to make sure the data
            is stored correctly
            '''

            '''
            If points are not presented, it catch the error and set it to zero,
            '''
            try:
                points: float = float(points)
            except ValueError:
                points: float = 0

            if not name or name == "NA":
                name = "No assigned jobs"

            week_days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday", "Biweekly",
                         "Weekly", "Biweekly"]

            if day not in week_days:
                day = "Coord"  # if it's not a day of the week or weekly/bi-weekly job, then is a coord job.

            # print(name, day, job, points)
            self.add_job_info(name, day, job, points)

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
        return self.current_sheet_name

    def get_full_dict(self):
        data_term: dict[str:list] = {"Current term name": self.current_sheet_name,
                                     "No assigned jobs": self.no_assigned_jobs,
                                     "Assigned jobs": self.assigned_jobs,
                                     "General points": self.points,
                                     "Members names": list(self.names)}
        return data_term


if __name__ == "__main__":
    cells = GatherCellsFromGoogle(title="JS Job Wheel").get_cells_data()
    a = MemberJobs(cells).get_full_dict()
    pprint(a)
