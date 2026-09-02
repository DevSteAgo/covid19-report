import sqlite3
import json 




def __main__():
    con = None

    try:
        con = sqlite3.connect("data/db/covid-19.db")
        
        print("Connected to database successfully")

        cur = con.cursor()
        cur.execute("""DROP TABLE IF EXISTS covid_data;""")
        cur.execute("""DROP TABLE IF EXISTS region;""")
        cur.execute("""DROP TABLE IF EXISTS province;""")


        
        cur.execute("""CREATE TABLE region (
                        region_code INTEGER PRIMARY KEY,
                        region TEXT)""")
        
        cur.execute("""
                    CREATE TABLE province (
                        province_code INTEGER PRIMARY KEY,
                        province TEXT,
                        region_code INTEGER REFERENCES region(region_code))
                    """)

        cur.execute("""
                    CREATE TABLE covid_data (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        province_code INTEGER REFERENCES province(province_code),
                        date DATE,
                        total_cases INTEGER)
                    """)

        print("Tables created successfully")

        with open("data/json/dpc-covid19-ita-province.json", "r") as f:
            json_file = f.read()

        json_data = json.loads(json_file)

        cur.execute("BEGIN TRANSACTION")

        
        for item in json_data:

            province = item["denominazione_provincia"]
            date = item["data"]
            date = date.split("T")[0]
            total_cases = item["totale_casi"]
            region_code = item["codice_regione"]
            province_code = item["codice_provincia"]
            region = item["denominazione_regione"]
            

            if region_code and region:
                cur.execute("INSERT OR IGNORE INTO 'region' VALUES (?, ?)", (region_code, region))

            if province_code and province and region_code:
                cur.execute("INSERT OR IGNORE INTO 'province' VALUES (?, ?, ?)", (province_code, province, region_code))

            cur.execute("INSERT INTO 'covid_data' (province_code, date, total_cases) VALUES (?, ?, ?)", (province_code, date, total_cases))

        cur.execute("COMMIT")

        print("Data inserted successfully")
                        

    except sqlite3.Error as e:
        print("Error while connecting to sqlite", e)
        return False
    finally:
        if con:
            con.close()
            print("Connection to database closed")

    return True



if __name__ == "__main__":
    __main__()
