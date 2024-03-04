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
        self.data = data
        self.create_schedule()

    '''
    TODO adapt to new gather cells
    '''
    def create_schedule(self):
        for job, day, points, name in self.data[1:]:  # first line holds the name of the term
            day = day.lower().strip()
            job = job.lower().strip()
            name = name.lower().strip()
            if day in ["monday", "tuesday", "wednesday", "thursday", "friday", "saturday", "sunday"]:
                day = day.capitalize()
                name = name.capitalize()
                match job:
                    case "am dishes":
                        self.week[day.capitalize()]["Morning"].append((job.capitalize(), name, points))
                    case "day dishes":
                        self.week[day.capitalize()]["Day"].append((job.capitalize(), name, points))
                    case "night dishes":
                        self.week[day.capitalize()]["Night"].append((job.capitalize(), name, points))
        return self.week

    def get_schedule(self):
        return self.week


# cells = GatherCellsFromGoogle(title="JS Job Wheel").get_cells_data()
# a = CreateSchedule(cells)
# pprint(a.get_schedule())
