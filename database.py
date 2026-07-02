import sqlite3

class Database:
    def __init__(self):
        self.conn = self.connect_to_database()
        pass


    def connect_to_database(self):
        conn = sqlite3.connect('database.db')
        cursor = conn.cursor()
        cursor.execute(
        "CREATE TABLE IF NOT EXISTS deep_work_sessions(session_id INTEGER PRIMARY KEY AUTOINCREMENT, minutes INTEGER NOT NULL, theme TEXT DEFAULT null, date TIMESTAMP DEFAULT CURRENT_TIMESTAMP)"
        )
        cursor.close()
        return conn;


    def insert_entry(
            self, 
            data:list[tuple[int, str | None]]
    ):
        cursor = self.conn.cursor()
        cursor.executemany("INSERT INTO deep_work_sessions(minutes, theme) VALUES(?, ?)", data)
        self.conn.commit()
        cursor.close()

    def clean_data_to_insert(data:list[tuple[int, str | None]]):
        pass


    def read_all_entries(self):
        cursor = self.conn.cursor()
        cursor.execute("SELECT minutes, date, theme FROM deep_work_sessions")
        data = cursor.fetchall()
        cursor.close()
        return data



    def search_entry(self, filter:str, search_input:str):
            try:
                allowed_columns=("date", "minutes", "theme")
                if filter not in allowed_columns:
                    raise ValueError
                cursor = self.conn.cursor()
                cursor.execute(f"SELECT minutes, date, theme FROM deep_work_sessions WHERE {filter} LIKE ?", (f"{search_input}%",))
                data = cursor.fetchall()
                cursor.close()
                return data
            except ValueError:
                pass


    def calculate_nb_of_minutes_per_time_window(self, time_window:str):
        pass

