from pprint import pprint
from gather_cells import GatherCellsFromGoogle


class CreateSchedule:
    def __init__(self, data: list):
        self.week = {"Sunday": {"Morning": [], "Day": [], "Night": []},
                     "Monday": {"Morning": [], "Day": [], "Night": []},
                     "Tuesday": {"Morning": [], "Day": [], "Night": []},
                     "Wednesday": {"Morning": [], "Day": [], "Night": []},
                     "Thursday": {"Morning": [], "Day": [], "Night": []},
                     "Friday": {"Morning": [], "Day": [], "Night": []},
                     "Saturday": {"Morning": [], "Day": [], "Night": []}
                     }

        self.matrix = []
        self.schedule_per_day = {"Sunday": [],
                                 "Monday": [],
                                 "Tuesday": [],
                                 "Wednesday": [],
                                 "Thursday": [],
                                 "Friday": [],
                                 "Saturday": []
                                 }
        self.data = data
        self.create_schedule_dictionary()
        # self.create_schedule_matrix()
        self.create_schedule_dict_per_day()


    def create_schedule_dictionary(self) -> None:

        for job, day, points, name in self.data[1:]:  # first line holds the name of the term
            # print(job, day, points, name)
            if day in ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]:
                match job:
                    case "Am dishes":
                        self.week[day]["Morning"].append((name, job))
                    case "Day dishes":
                        self.week[day]["Day"].append((name, job))
                    case "Night dishes":
                        self.week[day]["Night"].append((name, job))

    def create_schedule_dict_per_day(self):
        week_days = ["Sunday", "Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday"]
        order_of_day = ["Morning", "Day", "Night"]
        result = []
        for day in week_days:
            dict_jobs_per_day = self.week[day]
            temp = []
            for time in order_of_day:

                for k in dict_jobs_per_day[time]:
                    if k[0]:
                        temp.append(k)
            self.schedule_per_day[day] = temp
            result.append(temp)
        return self.schedule_per_day

    def create_schedule_matrix(self) -> None:
        days = ["Sunday", "Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday"]
        hours = ["Time", "Morning", "Day", "Night", "Night"]
        self.matrix.append(hours)
        for i in days:
            temp = [i]
            current = self.get_schedule_dict()[i]
            for index, val in current.items():
                temp += val
            self.matrix.append(temp)

        self.matrix = list(zip(*self.matrix))

    def get_schedule_dict(self):
        return self.week

    def get_schedule_matrix(self):
        return self.matrix

    def get_schedule_dict_per_day(self):
        return self.schedule_per_day


# cells = GatherCellsFromGoogle(title="JS Job Wheel").get_cells_data()
# a = CreateSchedule(cells)
# pprint(a.get_schedule_dict_per_day())
# for i in a.get_schedule_matrix():
#     print(i)
