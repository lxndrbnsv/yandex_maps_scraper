import os
import shutil
from openpyxl import load_workbook


class ClearWB:
    def __init__(self):
        os.remove("./results.xlsx")
        shutil.copy("./template.xlsx", "./results.xlsx")


class CheckWB:
    def __init__(self):
        wb = load_workbook(filename="results.xlsx")
        ws = wb['Worksheet']

        print(ws.max_row)