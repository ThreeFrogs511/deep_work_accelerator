import matplotlib.pyplot as plt
from datetime import datetime, timedelta
from datetime import date

class Plotter:

    def __init__(self, range="day"):
        self.x=[]
        self.y=[]
        self.range=range
    

    def remove_redundant_dates(self, data:list[tuple[int, date, str]]):
        last_seven_days_cleaned = []
        current_session: None | tuple[int, datetime] = None
        length_of_data = len(data)
        i=0

        for minutes, date, theme in data:
            i = i + 1

            # first item
            if current_session is None:                  
                current_session = (minutes, date)
                

            # date redundancy, we add the minutes
            elif date == current_session[1]:
                new_tuple = (minutes+current_session[0], date)
                current_session = new_tuple

            # new date, we store last sessions then create a new one
            elif current_session is not None and date != current_session[1]:
                last_seven_days_cleaned.append(current_session)
                current_session = (minutes, date)

            # end of the list
            if i == length_of_data:
                last_seven_days_cleaned.append(current_session)


        return last_seven_days_cleaned


    def prep_data_for_graph(self, data:list[tuple[str, str, str]]):
        date_today = datetime.now()
        date_from_seven_days_ago = date_today - timedelta(days=7)
        last_seven_days=[]

        for minutes, date, theme in data:
            new_date = datetime.strptime(date, "%Y-%m-%d %H:%M:%S")
            if new_date >= date_from_seven_days_ago:
                from_str_to_datetime = datetime.strptime(date, "%Y-%m-%d %H:%M:%S")
                only_date_not_hours = from_str_to_datetime.date()
                new_tuple = (int(minutes), only_date_not_hours, theme)
                last_seven_days.append(new_tuple)
            else:
                continue
        cleaned_last_seven_days =  self.remove_redundant_dates(last_seven_days)

        
        if len(cleaned_last_seven_days) < 7:
            print("\nNot enough data to plot a chart. Here's the raw data instead:\n")
            for day in last_seven_days:
                print(f"{str(day[1])} - {day[0]} minute(s) of work - '${day[2]}' ")
            return False
        else:            
            last_seven_days = self.remove_redundant_dates(last_seven_days)
            for day in last_seven_days:
                self.x.append(day[1])
                self.y.append(day[0])

            return True

    

    def plotting_deep_work_session(self, data:list[tuple[str, str, str]]):
        try:
            is_plotting_possible = self.prep_data_for_graph(data)
            if is_plotting_possible:
                plt.style.use('_mpl-gallery')
                plt.bar(self.x, self.y,  width=1, edgecolor="white", linewidth=0.7)
                plt.title("Deep Work Minutes Per Day - Last 7 Days")
                plt.tight_layout()
                plt.show()
            else:
                return
        except KeyboardInterrupt:
            plt.close()
        