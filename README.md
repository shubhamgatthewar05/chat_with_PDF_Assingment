# PDF Upload and Q&A Real-time Application

This project is a Flask-based web application that allows users to upload PDF files, extract and save their text content to MongoDB, and ask questions in real-time based on the PDF content. Flask-SocketIO is used for WebSocket connections to enable real-time Q&A responses.


DEMO LINK :    https://youtu.be/9wVtZnIMF2o?si=cgovAO5O5wjvyJNn


## Table of Contents

- [Features](#features)
- [Installation](#installation)
  - [Prerequisites](#prerequisites)
  - [Environment Setup](#environment-setup)
  - [Installing Dependencies](#installing-dependencies)
- [Running the Application](#running-the-application)
- [Project Structure](#project-structure)
- [API Endpoints](#api-endpoints)
- [WebSocket Events](#websocket-events)
- [License](#license)

---

## Features

- **Upload PDF Files**: Users can upload PDF files, and the application extracts and stores the text content in MongoDB.
- **Real-time Q&A**: Users can ask questions related to the PDF content in real time using WebSockets, which returns answers based on the PDF content.
- **Google Generative AI Integration**: Integrated with Google Generative AI for content generation in response to questions.

---

## Installation

### Prerequisites

1. **Python 3.7+**
2. **MongoDB**: Make sure MongoDB is installed and running on `localhost:27017`.
3. **Google Generative AI Key**: Obtain an API key for Google Generative AI.

### Environment Setup

1. Clone the repository:
    ```bash
    git clone <repository-url>
    cd <repository-directory>
    ```

2. **Create a virtual environment** (recommended):
    ```bash
    python3 -m venv venv
    ```

3. Activate the virtual environment:
   - **For Windows**:
     ```bash
     venv\Scripts\activate
     ```
   - **For macOS/Linux**:
     ```bash
     source venv/bin/activate
     ```

### Installing Dependencies

With the virtual environment activated, install all required packages:

```bash
pip install -r requirements.txt
```

> **Note**: Make sure `requirements.txt` includes `Flask`, `Flask-SocketIO`, `pymongo`, `pdfplumber`, and `google.generativeai`.

---

## Running the Application

1. Start the MongoDB server (if it isn't already running).

2. Export your Google Generative AI API key by setting the `GOOGLE_API_KEY` environment variable in your shell or terminal:
   ```bash
   export GOOGLE_API_KEY="Your-Google-API-Key-Here"
   ```

3. Run the application:
   ```bash
   flask run
   ```

4. Open your browser and go to `http://127.0.0.1:5000`.

5. **Using WebSocket**: Connect to the WebSocket on the client side to interact with the Q&A feature in real time.

---

## Project Structure

```
.
├── app.py               # Main application file
├── requirements.txt     # Dependencies for the project
├── templates/
│   └── index.html       # Frontend file for PDF upload and Q&A interface
└── README.md            # Documentation file
```

---

## API Endpoints

### 1. `POST /upload_pdf`
- **Description**: Endpoint to upload a PDF, extract its text content, and save it to MongoDB.
- **Request**: Form-data with a `file` field containing the PDF file.
- **Response**:
  - `200 OK`: If the PDF is successfully uploaded and saved.
  - `400 Bad Request`: If the file is missing or invalid.

Example request:
```bash
curl -X POST -F 'file=@example.pdf' http://127.0.0.1:5000/upload_pdf
```

### 2. `GET /`
- **Description**: Renders the `index.html` template for the homepage.

---

## WebSocket Events

### `question`
- **Description**: Allows users to ask questions in real-time based on the uploaded PDF content.
- **Payload**:
  - `file_name`: The name of the PDF file.
  - `question`: The question to ask based on the PDF content.
- **Response**:
  - `answer`: The generated answer from the AI model.
  - `error`: Error message if any.

Example WebSocket interaction:
```javascript
socket.emit('question', { file_name: 'example.pdf', question: 'What is this document about?' });


