#from CommonServerPython import *
import base64
import json
from io import BytesIO
from openpyxl import Workbook
from openpyxl.drawing.image import Image
import os

# Input Arguments
args = demisto.args()
data = args.get('data')  # JSON array containing the data to be written to Excel
image_entry_id = args.get('image_entry_id')  # Entry ID of the uploaded image

try:
    if not data:
        return_error("The 'data' argument is required.")
    if not image_entry_id:
        return_error("The 'image_entry_id' argument is required.")

    # Retrieve the file path of the uploaded image using Entry ID
    res = demisto.getFilePath(image_entry_id)
    if not res or "path" not in res:
        return_error("Failed to retrieve file path for Entry ID: {}".format(image_entry_id))

    image_path = res["path"]

    # Parse input data
    data = data.replace("'", '"')  # Ensure JSON format is correct
    data_list = json.loads(data)  # Expecting a list of dictionaries
    if not isinstance(data_list, list) or not data_list:
        return_error("Invalid data format. Expecting a JSON array of objects.")

    # Create a new Excel workbook
    wb = Workbook()
    ws = wb.active
    ws.title = "Sheet1"

    # Write header row
    headers = list(data_list[0].keys()) + ["Image"]
    ws.append(headers)

    # Write data rows
    for row in data_list:
        row_values = [row.get(header, '') for header in headers[:-1]]  # Exclude 'Image' column
        ws.append(row_values)

        # Insert image in the last column (Python 2.7 compatible format)
        column_letter = chr(65 + len(headers) - 2)  # Get column letter dynamically
        cell_position = "{}{}".format(column_letter, ws.max_row)  # Construct cell position
        if os.path.exists(image_path):
            img = Image(image_path)
            ws.add_image(img, cell_position)  # Insert in the last column

    # Save to a BytesIO stream
    output_stream = BytesIO()
    wb.save(output_stream)
    output_stream.seek(0)

    # Save the file
    file_name = "generated_data_with_image.xlsx"
    file_path = demisto.uniqueFile()
    with open(file_path, "wb") as f:
        f.write(output_stream.read())

    # Upload the file to Cortex XSOAR
    file_entry = fileResult(file_name, open(file_path, "rb").read())
    demisto.results(file_entry)

except Exception as e:
    return_error("An error occurred: {}".format(str(e)))