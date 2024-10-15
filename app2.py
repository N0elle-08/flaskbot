from flask import Flask, request, jsonify, session, render_template
import os
import google.generativeai as genai
from werkzeug.utils import secure_filename
from model.utils import create_model, setup_logger, generate_content
from build.intents import funct_call
import logging

# Flask setup
app = Flask(__name__)
app.secret_key = "your_secret_key"  # Required for session management
app.config["UPLOAD_FOLDER"] = "uploads/"
os.makedirs(app.config["UPLOAD_FOLDER"], exist_ok=True)

# Set up the logger using the utility function
logger = setup_logger()

# Initialize the AI model using create_model function
GOOGLE_API_KEY = "AIzaSyD211F-lq7CsQren1P-wr3FYLsv8GY2k7A"

chat_model = create_model(GOOGLE_API_KEY)

# Initialize chat history in session
@app.before_request
def init_chat_history():
    if "history" not in session:
        session["history"] = []

# Define conversation chat function adapted to Flask
def conversation_chat(file_path, text_prompt):
    """
    Handles the chat session logic using the provided file path and text prompt.
    """
    try:
        user_input = text_prompt if text_prompt else ""
        user_entry = {"role": "user", "parts": [user_input]}

        # Handle file upload if a file is provided
        if file_path:
            filename = secure_filename(file_path.filename)
            temp_file_path = os.path.join(app.config["UPLOAD_FOLDER"], filename)
            file_path.save(temp_file_path)  # Save file

            logger.info(f"Successfully saved uploaded file: {filename}")

            # Upload the file to Google Generative AI
            genai_file = genai.upload_file(path=temp_file_path, display_name=filename)
            user_entry = {"role": "user", "parts": [genai_file, user_input]}

        # Append user entry to chat history
        session["history"].append(user_entry)

        # Generate AI response using the chat model and conversation history
        response = generate_content(chat_model, user_entry)

        # Process function calls if present in the response
        if response.text:
            bot_response = response.text
        elif response.function_call:
            fc = response.function_call
            bot_response = funct_call(fc.name, dict(fc.args))

        # Append bot response to the chat history
        bot_entry = {"role": "model", "parts": bot_response}
        session["history"].append(bot_entry)

        logger.info("Conversation processed successfully")
        return bot_response

    except Exception as e:
        logger.error(f"Error processing input: {e}")
        return "Error in processing the input"

# Flask route to handle chat interaction
@app.route("/chat", methods=["POST"])
def chat():
    """
    Chat route to handle text and file inputs from the user and generate AI responses.
    """
    text_prompt = request.form.get("text_prompt")
    file = request.files.get("file")

    bot_response = conversation_chat(file, text_prompt)
    return jsonify({"response": bot_response})

# Flask home route (you can serve a basic frontend here)
@app.route("/")
def home():
    return render_template("index1.html")

# Run the Flask app
if __name__ == "__main__":
    app.run(debug=True)
