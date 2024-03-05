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
                        self.week[day]["Morning"].append(name)
                    case "Day dishes":
                        self.week[day]["Day"].append(name)
                    case "Night dishes":
                        self.week[day]["Night"].append(name)

    def create_schedule_dict_per_day(self):
        week_days = ["Sunday", "Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday"]
        order_of_day = ["Morning", "Day", "Night"]
        # print(len(week_days))
        result = []
        for i in week_days:
            # print(i)
            dict_jobs_per_day = self.week[i]
            # print(dict_jobs_per_day)
            # print()
            temp = []
            for j in order_of_day:
                print(dict_jobs_per_day)
                print(dict_jobs_per_day[j])
                for k in dict_jobs_per_day[j]:
                    # print(k)
                    temp.append(k)
            # result.append(temp)
            # # print(i)
            # # print(temp)
            for k in temp:
                self.schedule_per_day[i].append(temp)
        print(result)
        return self.schedule_per_day

    def create_schedule_matrix(self) -> None:
        days = ["Sunday", "Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday"]
        hours = ["Time", "Morning", "Day", "Night", "Night"]
        self.matrix.append(hours)
        # print(self.get_schedule_dict())
        for i in days:
            temp = [i]
            current = self.get_schedule_dict()[i]
            # print(current)
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


cells = GatherCellsFromGoogle(title="JS Job Wheel").get_cells_data()
a = CreateSchedule(cells)
pprint(a.get_schedule_dict_per_day())
# for i in a.get_schedule_matrix():
#     print(i)
