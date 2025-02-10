import sqlite3

def setup_database():
    con = sqlite3.connect("jobsNumbers.db")
    cur = con.cursor()

    cur.execute("""
        CREATE TABLE IF NOT EXISTS AtJobsHist (
            ID INTEGER PRIMARY KEY AUTOINCREMENT, 
            jobType TEXT, 
            JobNumber INTEGER,
            TimeStamp DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    """)

    con.commit()
    con.close()

if __name__ == "__main__":
    setup_database()
