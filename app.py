from flask import Flask,render_template, request, jsonify
import google.generativeai as genai


import os
app = Flask(__name__)

generation_config = {
    "temperature": 0.9,
    "top_p": 0.95,
    "top_k": 64,
    "max_output_tokens": 8192,
    "response_mime_type": "text/plain",
    }

try:
        genai.configure(api_key="AIzaSyD211F-lq7CsQren1P-wr3FYLsv8GY2k7A")
        model = genai.GenerativeModel(
                    model_name="gemini-1.5-flash",
                    generation_config=generation_config,
                    system_instruction= "You are an SAP expert",
                    )
        chat = model.start_chat()
        print("Model created successfully")
except Exception as e:
        print(f"Error creating model: {e}")

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/get")
def get_bot_response():    
    userText = request.args.get('msg')
    response = chat.send_message(userText) # for the gemini AI model
    return response.text

if __name__ == "__main__":
    app.run()
