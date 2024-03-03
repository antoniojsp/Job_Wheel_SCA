import gspread

import credentials


class ScheduleCreator:
    def __init__(self, title):
        self.week = {"Sunday": {"Morning": [], "Day": [], "Night": []},
                     "Monday": {"Morning": [], "Day": [], "Night": []},
                     "Tuesday": {"Morning": [], "Day": [], "Night": []},
                     "Wednesday": {"Morning": [], "Day": [], "Night": []},
                     "Thursday": {"Morning": [], "Day": [], "Night": []},
                     "Friday": {"Morning": [], "Day": [], "Night": []},
                     "Saturday": {"Morning": [], "Day": [], "Night": []}
                     }

        self.week = [[[]] * 3] * 7

        self.gc = gspread.service_account_from_dict(credentials.credentials)

        self.sheet = self.gc.open(title)  # title: title of the spreadsheet to use
        #  get all the sheet names but we use the first one that it's the current term.
        self.current_sheet_name = self.get_sheet_names()[0]
        self.create_schedule()
    def create_schedule(self):
        entire_sheet = self.sheet.worksheet(self.current_sheet_name)  # currently, only selects the most recent job

        for row in entire_sheet.get()[1:]:
            if len(row) < 6:
                row.append("")

            if row[1].capitalize() in ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]:
                print(row[0], row[1], row[5])

    def get_sheet_names(self) -> list:
        return [s.title for s in self.sheet.worksheets()]  # sheet names (to select the current or past sheet)

ScheduleCreator(title="JS Job Wheel").create_schedule()
