import csv
from datetime import date

class SaveDeepWorkSession:

    def __init__(self, time:int):
        self.time=time;
        self.date=date.today()
        self.header= ["hour", "date"]

    def formatting_date(self):
        pass

    
    def checking_if_csv_exists(self):
        """ safeguard to be sure the file exists """
        try:
            with open("deep_work_output.csv", "r") as f:
                reader = csv.reader(f, delimiter=",")
        except FileNotFoundError:
            print("\nNo file found. A csv file was newly created.\n")
            self.adding_header()

  
    def checking_if_header_exists(self):
        """ safeguard to be sure the file has headers and is not empty """
        lines=[]
        with open("deep_work_output.csv", "r") as f:
            reader = csv.reader(f)
            for line in reader:
                lines.append(line);
        if not lines or self.header not in lines:
            print("\nMissing header. Adding it...\n")
            self.adding_header()

    def adding_header(self):
        with open("deep_work_output.csv", "w", newline="", encoding='UTF-8') as w:
            writer= csv.DictWriter(w, fieldnames=self.header)
            writer.writeheader()

    def adding_new_row(self):
        with open("deep_work_output.csv", "a+", newline="", encoding='UTF-8') as a:
            appender = csv.DictWriter(a, fieldnames=self.header)
            appender.writerow({"hour": self.time, "date": self.date})


    def log_deep_work_session(self):
        self.checking_if_csv_exists();
        self.checking_if_header_exists();
        self.adding_new_row();

