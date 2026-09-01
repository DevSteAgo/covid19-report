from flask import Flask, render_template, request

from export import export_to_xlsx

from conn import get_covid_data

from datetime import datetime


app = Flask(__name__)



datetime
@app.route("/")
def dashboard():

    if request.args.get("date"):
        filter_date = request.args.get("date")
    else:
        filter_date = None

    if request.args.get("sort"):
        sort_order = request.args.get("sort")
    else:
        sort_order = None

    covid_data = get_covid_data(True, filter_date, sort_order)
          
    if covid_data:
        selected_date = datetime.fromisoformat(covid_data[0]["date"]).date()
    elif filter_date:
        selected_date = datetime.fromisoformat(filter_date).date()
    else:
        selected_date = None

    selected_date_string = selected_date.strftime("%d/%m/%Y") if selected_date else None


   
        
    print(sort_order)

    if covid_data:
        return render_template("dashboard.html", covid_data=covid_data, selected_date=selected_date_string, selected_date_iso=selected_date, sort_order=sort_order, max_date=datetime.now().date())
    else:
        return render_template("no_result.html", selected_date=selected_date_string , selected_date_iso=selected_date, sort_order=sort_order, max_date=datetime.now().date())






@app.route("/export")
def export():
    selected_date = request.args.get("date")
    covid_data = get_covid_data(True, selected_date)

    if covid_data:
        filename = f"covid_data_{selected_date}.xls"
        return export_to_xlsx(covid_data, filename)
    else:
        return render_template("no_result.html", selected_date=selected_date, selected_date_iso=selected_date)

    

