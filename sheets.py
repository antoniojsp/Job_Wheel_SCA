import gspread

gc = gspread.service_account(filename='C:/Users/Antonio/PycharmProjects/Job_Wheel/credentials.json')

sh = gc.open("Copy of JS Job Wheel")

print(sh.sheet1.get('A1'))

url = "https://docs.google.com/spreadsheets/d/1XTb5lM1OOd4PNZ0O4FawsYIH1We6f-WH9lEkUV6yp0w/edit#gid=1847066599"
spreadsheet = gc.open_by_url(url)
sheet_names = [s.title for s in spreadsheet.worksheets()]
print(sheet_names)