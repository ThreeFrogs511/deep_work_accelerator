import matplotlib.pyplot as plt
import csv

class CsvToGraph:

    def __init__(self, range="day"):
        self.reader={}
        self.x=[]
        self.y=[]
        self.data_per_day=[]
        self.data_per_day_CLEANED=[]
        self.data_per_month=[]
        self.months = [
            {"01":"Jan"}, 
            {"02":"Feb"}, 
            {"03":"Mar"}, 
            {"04":"Apr"}, 
            {"05":"May"}, 
            {"06":"June"}, 
            {"07":"July"}, 
            {"08":"Aug"}, 
            {"09":"Sept"}, 
            {"10":"Oct"}, 
            {"11":"Nov"}, 
            {"12":"Dec"}
        ]
        self.range=range
        self.csv_len = self.calculating_length_of_csv()

    def read_csv_for_graph(self):
        """prevents errors"""
        try:
            with open("deep_work_output.csv", "r") as f:
                self.reader= csv.reader(f, delimiter=",")
        except FileNotFoundError:
            print("\nNo csv file found.\nPlease launch a deep work session to create one.\n")

    

    def calculating_length_of_csv(self):
        """required to prevent skipping the last line of the csv file"""
        with open("deep_work_output.csv", "r") as f:
            reader = csv.reader(f, delimiter=",")
            count=0
            for row in reader:
                count+=1
            return count
    
    def cleaning_csv_data_per_day(self, reader):
        """cleans day duplicates
        returns a list of deep work hours(y) per day(x)
        then hydrates the graph"""
        counter=0
        for row in reader:
            counter+=1

            if row[0] == "hour" and row[1] == "date":
                continue
            if not self.data_per_day:
                self.data_per_day = [row[0], row[1]]

            elif row[1] == self.data_per_day[1]:
                hours= int(row[0]) + int(self.data_per_day[0]);
                self.data_per_day = [str(hours), self.data_per_day[1]]

                # end of file 
                # adding the last line in the graph 
                # if it's similar to the previous one
                if counter==self.csv_len:
                    self.data_per_day_CLEANED.append(self.data_per_day)
                    self.y.append(int(self.data_per_day[0]))
                    self.x.append(self.data_per_day[1])
                    return
            else:
                self.data_per_day_CLEANED.append(self.data_per_day)
                self.y.append(int(self.data_per_day[0]))
                self.x.append(self.data_per_day[1])
                self.data_per_day = [row[0], row[1]]

                # end of file
                #adding the last line in the graph if it's not similar 
                # to the previous one
                if counter==self.csv_len:
                    self.data_per_day_CLEANED.append(self.data_per_day)
                    print(row)
                    self.y.append(int(row[0]))
                    self.x.append(row[1])



    def convert_int_to_string_months(self, date:list[str]):
        """required to display months in letter (e.g: "04" to "Apr")"""
        split = date.split("-")
        months_index = int(split[1])-1
        month_dict = self.months[months_index]
        return month_dict.get(split[1])

    def cleaning_csv_data_per_month(self, reader):
        """generates a list of deep work hours total (y) per month (x)
        based on the list 'data_per_day_CLEANED' 
        created by 'cleaning_csv_data_per_day'
        then hydrates the graph """
        self.cleaning_csv_data_per_day(reader)
        self.y, self.x = [], []
        for day in self.data_per_day_CLEANED:
            hour=int(day[0])
            is_month_already_in = False
            month_in_letters = self.convert_int_to_string_months(day[1])
            if not self.data_per_month:
                self.data_per_month.append([hour, month_in_letters]);
                continue
            for m in self.data_per_month:
                if month_in_letters in m:
                    m[0] = hour + int(m[0])
                    is_month_already_in = True
                    break
            if not is_month_already_in:
                self.data_per_month.append([day[0], month_in_letters])

        for month in self.data_per_month:
            self.x.append(month[1])
            self.y.append(int(month[0]))
            
            



    def plotting_deep_work_session(self):
        """add the x and y data used by the graph then launches it"""
        # self.read_csv_for_graph()
        try:
            with open("deep_work_output.csv", "r") as f:
                reader = csv.reader(f, delimiter=",")
                if self.range=="day":
                    self.cleaning_csv_data_per_day(reader)
                elif self.range=="month":
                    self.cleaning_csv_data_per_month(reader)
                    print(self.data_per_month)
                plt.plot(self.x, self.y, marker="o")
                plt.title("Deep work session per " + self.range)
                plt.show()
        except KeyboardInterrupt:
            plt.close()