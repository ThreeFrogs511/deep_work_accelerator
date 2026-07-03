import matplotlib.pyplot as plt
from datetime import datetime, timedelta

class Plotter:

    def __init__(self, range="day"):
        self.x=[]
        self.y=[]
        self.range=range
    

    def prep_data_for_graph(self, data:list[tuple[str, str, str]]):
        date_today = datetime.now()
        date_from_seven_days_ago = date_today - timedelta(days=7)
        last_seven_days=[]
        for session in data:
            if session[1] != date_from_seven_days_ago.strftime("%Y-%m-%d %H:%M:%S"):
                from_str_to_datetime = datetime.strptime(session[1], "%Y-%m-%d %H:%M:%S")
                only_date = from_str_to_datetime.date()
                new_tuple = (session[0], only_date, session[2])
                last_seven_days.append(new_tuple)
            else:
                break
        
        if len(last_seven_days) < 7:
            print("\nNot enough data to plot a chart. Here's the raw data instead:\n")
            for day in last_seven_days:
                print(f"{str(day[1])} - {day[0]} minute(s) of work - '${day[2]}' ")
            return False
        else:
            for day in last_seven_days:
                self.x.append(day[1])
                self.y.append(day[0])
            return True
    

    def plotting_deep_work_session(self, data:list[tuple[str, str, str]]):
        try:
            is_plotting_possible = self.prep_data_for_graph(data)
            if is_plotting_possible:
                plt.plot(self.x, self.y, marker="o")
                plt.title("Deep work minutes per day - last 7 days")
                plt.tight_layout()
                plt.show()
            else:
                return
        except KeyboardInterrupt:
            plt.close()
        