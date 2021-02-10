from flask import Flask, request, make_response, send_file
import io
from zipfile import ZipFile, ZIP_DEFLATED

app = Flask(__name__)

@app.route("/")
def hello():
  return "Hello, World!"


@app.route('/zipper', methods=['POST'])
def zip_request():
  if request.method == 'POST':
    memory_file = io.BytesIO()
    # In-memory zip file handling
    with ZipFile(memory_file,'w', compression = ZIP_DEFLATED) as zf: # Compression type
      json_str = request.form['json']
      uploaded_pdf_file = request.files['pdf_file']
      zf.writestr(uploaded_pdf_file.filename, uploaded_pdf_file.read())
      zf.writestr('content.json', json_str)
    # After writing the contents to zip file, the file pointer is reset to the starting position.
    memory_file.seek(0)
    return send_file(memory_file, attachment_filename='compressed_response.zip', as_attachment=True)
