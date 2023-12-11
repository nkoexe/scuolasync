from pathlib import Path
import pandas as pd


class Docenti:
    def from_csv():
        pass

    def from_xlsx(filepath: Path):
        print(pd.read_excel(filepath))


if __name__ == "__main__":
    Docenti.from_xlsx(r"C:\Users\nicco\Downloads\Members_03o7alnk2seo67k_11122023_163539.csv.xlsx")
