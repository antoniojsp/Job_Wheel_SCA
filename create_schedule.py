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

        self.data = data
        self.create_schedule_dictionary()
        self.create_schedule_matrix()

    def create_schedule_dictionary(self) -> None:

        for job, day, points, name in self.data[1:]:  # first line holds the name of the term
            # print(job, day, points, name)
            if day in ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]:
                match job:
                    case "Am dishes":
                        self.week[day]["Morning"].append((name))
                    case "Day dishes":
                        self.week[day]["Day"].append((name))
                    case "Night dishes":
                        self.week[day]["Night"].append((name))

    """
    TODO
    """

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


# cells = GatherCellsFromGoogle(title="JS Job Wheel").get_cells_data()
# a = CreateSchedule(cells)
# # pprint(a.get_schedule_dict())
# for i in a.get_schedule_matrix():
#     print(i)
