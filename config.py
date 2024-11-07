from flask import Flask, request, jsonify, render_template
from flask_socketio import SocketIO, emit
from pymongo import MongoClient
import pdfplumber
import io
import google.generativeai as genai


genai.configure(api_key=" .....here you add your api key.............")
model = genai.GenerativeModel("gemini-1.5-flash")

# Flask and SocketIO
app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app, cors_allowed_origins="*")


client = MongoClient("mongodb://localhost:27017/")   # here i used mongoDB database to stored the metadata..
db = client["pdf_db"]
collection = db["pdf_metadata"]


@app.route('/upload_pdf', methods=['POST']) ##uploading  PDF and save content i here i used...Flask framewrk..for FASTAPI
def upload_pdf():
    if 'file' not in request.files:
        return jsonify({"error": "No file part"}), 400
    file = request.files['file']
    
    if file.filename == '':
        return jsonify({"error": "No selected file"}), 400
    
    if file and file.filename.endswith('.pdf'):
        
        with pdfplumber.open(io.BytesIO(file.read())) as pdf:
            content = ""
            for page_num, page in enumerate(pdf.pages):
                content += page.extract_text() or ""
        
       
        pdf_data = {
            "file_name": file.filename,
            "content": content
        }
        collection.insert_one(pdf_data)
        return jsonify({"message": "PDF uploaded and content saved."}), 200

    return jsonify({"error": "Invalid file type"}), 400


@socketio.on('question')            ## WebSocket for real-time Q&A.......chatting..
def handle_question(data):
    file_name = data.get("file_name")
    question = data.get("question")
    
  
    pdf_data = collection.find_one({"file_name": file_name})
    if not pdf_data:
        emit('answer', {"error": "File not found"})
        return
   
    context = pdf_data["content"]
    try:
        
        response = model.generate_content(f"{context}\n\nQuestion: {question}")
        answer = response.text if response else "No answer found."

        
        emit('answer', {"answer": answer})
    except Exception as e:
        emit('answer', {"error": str(e)})

# Home route to render index.html
@app.route('/')
def index():
    return render_template('index.html')


if __name__ == '__main__':
    socketio.run(app, debug=True)
