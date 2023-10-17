from flask import Flask, render_template, request, send_file
from gtts import gTTS
import tempfile
import PyPDF2

app = Flask(__name__)

def pdf_to_text(file_path):
    with open(file_path, 'rb') as file:
        reader = PyPDF2.PdfReader(file)
        text = ""
        for page in range(len(reader.pages)):
            text += reader.pages[page].extract_text()
        return text

@app.route("/", methods=["GET", "POST"])
def home():
    if request.method == "POST":
        if 'file' in request.files:
            file = request.files['file']
            if file.filename != '':
                # Save the uploaded pdf to a temporary location
                temp_pdf = tempfile.NamedTemporaryFile(delete=False, suffix=".pdf")
                file.save(temp_pdf.name)
                
                # Convert PDF to text
                text = pdf_to_text(temp_pdf.name)
                
                # Convert text to speech
                audio = gTTS(text=text)

                # Create a temporary file for the audio
                with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as temp_file:
                    audio.save(temp_file.name)

                    # Provide the audio file for download
                    return send_file(temp_file.name, as_attachment=True, download_name='output.mp3')

    return render_template("index.html")

if __name__ == "__main__":
    app.run(debug=True)
