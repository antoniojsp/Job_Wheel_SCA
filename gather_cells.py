import gspread
import credentials


class GatherCellsFromGoogle:
    def __init__(self, title):
        self.gc = gspread.service_account_from_dict(credentials.credentials)
        self.sheet = self.gc.open(title)  # title: title of the spreadsheet to use
        #  get all the sheet names but we use the first one that it's the current term.
        self.current_sheet_name = self.get_sheet_names()[0]
        self.get_cells_data()

    def get_sheet_names(self) -> list:
        return [s.title for s in self.sheet.worksheets()]  # sheet names (to select the current or past sheet)

    def get_cells_data(self):
        entire_sheet = self.sheet.worksheet(self.current_sheet_name)  # currently, only selects the most recent job
        result = [self.current_sheet_name]  # first index will store the name of the current term to be used for the
        # other methods. after the first index, all the regular information is included
        for row in entire_sheet.get()[1:]:
            if row[0] == "":
                continue
            if len(row) < 6:
                row.append("")
            job = row[0].capitalize().strip()
            day = row[1].capitalize().strip()
            points = row[4].capitalize().strip()
            name = row[5].capitalize().strip()
            result.append([job, day, points, name])
        return result

# a = GatherCellsFromGoogle(title="JS Job Wheel").get_cells_data()
# for i in a:
#     print(i, sep="/n")
