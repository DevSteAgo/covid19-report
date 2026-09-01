from io import BytesIO
from flask import send_file, request
import xlwt


def export_to_xlsx(data, filename):

    output = BytesIO()
    workbook = xlwt.Workbook()
    sheet = workbook.add_sheet("COVID-19")

    sheet.write(0, 0, "Region")
    sheet.write(0, 1, "Total cases")

    for index, row in enumerate(data, start=1):
        sheet.write(index, 0, row["region"])
        sheet.write(index, 1, row["total_cases"])

    workbook.save(output)
    output.seek(0)

    return send_file(
        output,
        mimetype="application/vnd.ms-excel",
        as_attachment=True,
        download_name=filename,
    )

