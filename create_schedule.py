from pprint import pprint
from gather_cells import GatherCellsFromGoogle


class CreateSchedule:
    def __init__(self, data: list):
        self.daily_turns = {"Sunday": {"Am dishes": [], "Day dishes": [], "Night dishes": []},
                            "Monday": {"Am dishes": [], "Day dishes": [], "Night dishes": []},
                            "Tuesday": {"Am dishes": [], "Day dishes": [], "Night dishes": []},
                            "Wednesday": {"Am dishes": [], "Day dishes": [], "Night dishes": []},
                            "Thursday": {"Am dishes": [], "Day dishes": [], "Night dishes": []},
                            "Friday": {"Am dishes": [], "Day dishes": [], "Night dishes": []},
                            "Saturday": {"Am dishes": [], "Day dishes": [], "Night dishes": []}
                            }

        self.calendar_matrix = []
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
        self.create_schedule_matrix()
        self.create_schedule_dict_per_day()

    def create_schedule_dictionary(self) -> None:
        '''
        First, gather all the cells data and sort them in place by day and turn (morning, day and night)
        '''
        week_days: list[str] = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
        for job, day, points, name in self.data[1:]:  # first line holds the name of the term
            if day in week_days:
                match job:
                    case "Am dishes":
                        self.daily_turns[day]["Am dishes"].append((name, job))
                    case "Day dishes":
                        self.daily_turns[day]["Day dishes"].append((name, job))
                    case "Night dishes":
                        self.daily_turns[day]["Night dishes"].append((name, job))

        '''
        Second, it counts how people are assigned per day for a turn, storage the greatest  number of people
        assigned for one day and then add extra white space in the matrix for that turn everyday, so it
        is display evenly in the calendar
        '''

        times: list[str] = ["Am dishes", "Day dishes", "Night dishes"]
        max_shifts_per_day: {str: int} = {"Am dishes": 0, "Day dishes": 0, "Night dishes": 0}
        for i in week_days:
            for j in times:
                max_shifts_per_day[j] = max(max_shifts_per_day[j], len(self.daily_turns[i][j]))

        for i in week_days:
            for j in times:
                if len(self.daily_turns[i][j]) < max_shifts_per_day[j]:
                    t = max_shifts_per_day[j] - len(self.daily_turns[i][j])
                    for _ in range(t):
                        self.daily_turns[i][j].append(("", j))

    def create_schedule_dict_per_day(self) -> None:
        week_days: list[str] = ["Sunday", "Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday"]
        order_of_day: list[str] = ["Am dishes", "Day dishes", "Night dishes"]
        for day in week_days:
            dict_jobs_per_day: dict = self.daily_turns[day]
            names_temp: list[str] = []
            for time in order_of_day:
                for name, job in dict_jobs_per_day[time]:
                    if name == "":
                        names_temp.append(("No assigned",time))
                    else:
                        names_temp.append((name, time))

            self.schedule_per_day[day] = names_temp

    def create_schedule_matrix(self) -> None:
        '''
        gather information from self.get_daily_turns and it in a 2d list or matrix to represent a calendar
        :return: None
        '''
        days = ["Sunday", "Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday"]
        for i in days:
            temp = [i]
            current = self.get_daily_turns()[i]
            for index, val in current.items():
                temp += val
            self.calendar_matrix.append(temp)

        # creating the first column
        time_of_the_day: list[str] = ["Time"]
        for i in range(1, len(self.calendar_matrix[0])):
            time_of_the_day.append(self.calendar_matrix[0][i][1])

        self.calendar_matrix = [time_of_the_day] + self.calendar_matrix
        self.calendar_matrix = list(zip(*self.calendar_matrix))  # transpose matrix

    def get_daily_turns(self):
        return self.daily_turns

    def get_schedule_matrix(self):
        return self.calendar_matrix

    def get_schedule_dict_per_day(self):
        return self.schedule_per_day


if __name__ == "__main__":
    cells = GatherCellsFromGoogle(title="JS Job Wheel").get_cells_data()
    a = CreateSchedule(cells)
    # pprint(a.get_daily_turns())
    pprint(a.get_schedule_dict_per_day())
    for i in a.get_schedule_matrix():
        print()
