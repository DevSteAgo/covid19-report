from flask import Flask, render_template, request
from datetime import datetime

from export import export_to_xlsx
from conn import get_covid_data, get_last_date




app = Flask(__name__)



datetime
@app.route("/")
def dashboard():
   
    filter_date = request.args.get("date")
    sort_order = request.args.get("sort", "cases_desc")

    #Validate the filter_date parameter
    if filter_date:
        try:
            datetime.strptime(filter_date, "%Y-%m-%d")
        except (ValueError, TypeError):
            filter_date = None
            return render_template("no_result.html", covid_data=None, selected_date=None, selected_date_iso=None, sort_order=sort_order, max_date=datetime.now().date(), message="Invalid date format. Please use YYYY-MM-DD.")
    if filter_date and filter_date < "2020-02-24":
        return render_template("no_result.html", covid_data=None, selected_date=None, selected_date_iso=None, sort_order=sort_order, max_date=datetime.now().date(), message="No data available for the selected date. The earliest available date is 2020-02-24.")
    
    #Get covid data from db
    covid_data = get_covid_data(filter_date, sort_order)

    last_date = get_last_date()


    #Get the date of the available covid data
    if covid_data:
        #Get the selected date from the first record in the covid_data list
        selected_date = datetime.fromisoformat(covid_data[0]["date"]).date()
    elif filter_date:
        #Get the selected date from the filter_date parameter
        selected_date = datetime.fromisoformat(filter_date).date()
    else:
        selected_date = None

    #Format the selected date as a string in the format "dd/mm/yyyy"
    selected_date_string = selected_date.strftime("%d/%m/%Y") if selected_date else None


    if covid_data: 
        return render_template("dashboard.html", covid_data=covid_data, selected_date=selected_date_string, selected_date_iso=selected_date, sort_order=sort_order, max_date=datetime.now().date(), )
    else:
        return render_template("no_result.html", selected_date=selected_date_string , selected_date_iso=selected_date, sort_order=sort_order, max_date=last_date, message=f"No data available for the selected date. Last available date is {last_date}.")






@app.route("/export")
def export():
    selected_date = request.args.get("date")
    sort_order = request.args.get("sort", "cases_desc")

    if selected_date:
            try:
                datetime.strptime(selected_date, "%Y-%m-%d")
            except (ValueError, TypeError):
                selected_date = None

    #Get covid data from db
    covid_data = get_covid_data(selected_date, sort_order)

    if covid_data:
        filename = f"covid_data_{selected_date}.xls"
        return export_to_xlsx(covid_data, filename)
    else:
        return None, 404
    
