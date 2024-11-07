import io

from flask import Flask, request, send_file

import constants
import html_to_pdf_generator

app = Flask(__name__)

@app.route(rule='/generate-pdf', methods=["POST"])
def handle_post_request():
    try:
        request_data = request.get_json()
        page_content = request_data['page_content']
        save_as_html_file(page_content)
        (pdf_file, pdf_file_name) = html_to_pdf_generator.generate_pdf_from_html()

        return send_file(
            io.BytesIO(pdf_file),
            as_attachment=True,
            download_name=pdf_file_name,
            mimetype='application/pdf'
        )
    except Exception as e:
        return {
            "error": str(e)
        }, 500

def run_flask_app():
    # app.run(host="localhost", port=8080)
    app.run(host="0.0.0.0", port=8000)

# TODO to other file
def save_as_html_file(data):
    with open(constants.INPUT_FILE_NAME, "w") as file:
        file.write(data)