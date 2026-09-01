import sqlite3

def get_db_connection():
    conn = sqlite3.connect("data/db/covid-19.db")
    conn.row_factory = sqlite3.Row
    return conn



def get_covid_data( filter_date=None, sort_order="cases_desc"):
    try:
        conn = get_db_connection()
        cur = conn.cursor()

        filter_clause = ""

        if filter_date:
            filter_clause = f"WHERE date = '{filter_date}' and date >= '2020-02-24'"
        else: #If no filter_date is provided, get the latest available date
            filter_clause = "WHERE date = (SELECT MAX(date) FROM covid_data)"

        
        query = f"SELECT r.region, SUM(cd.total_cases) as total_cases, date  FROM (covid_data cd INNER JOIN province p ON cd.province_code = p.province_code) INNER JOIN region r ON p.region_code = r.region_code {filter_clause} GROUP BY r.region"
        if sort_order == "cases_asc":
            query += " ORDER BY total_cases ASC, r.region ASC"
        elif sort_order == "cases_desc":
            query += " ORDER BY total_cases DESC, r.region ASC"
        elif sort_order == "reg_asc":
            query += " ORDER BY r.region ASC, total_cases DESC"
        elif sort_order == "reg_desc":
            query += " ORDER BY r.region DESC, total_cases DESC"
       
        cur.execute(query)
        rows = cur.fetchall()
        
    except sqlite3.Error as e:
        print("Error while connecting to sqlite", e)
        return []
    finally:
        if conn:
            conn.close()
    return rows
    

    
