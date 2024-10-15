import os
import google.generativeai as genai
from model.prompts import sys_instructions
from settings.base import setup_logger
from build.actions import Actions
from build.func_tools import tools_func


logger = setup_logger()
actions = Actions()

def create_model(api_key):
    """
    Create a GenerativeModel instance using the provided API key.
    """
    generation_config = {
    "temperature": 0.9,
    "top_p": 0.95,
    "top_k": 64,
    "max_output_tokens": 8192,
    "response_mime_type": "text/plain",
    }

    try:
        genai.configure(api_key=api_key)
        model = genai.GenerativeModel(
                    model_name="gemini-1.5-flash",
                    generation_config=generation_config,
                    system_instruction= sys_instructions(),
                    tools=tools_func
                    )
        chat = model.start_chat()
        logger.info("Model created successfully")
        return chat
    except Exception as e:
        logger.error(f"Error creating model: {e}")
        return None


def generate_content(chat, message):
    """
    Send a message to the chat session and get the response.
    """
    try:
        # msg = f"Query:{message}/n/n Every time you provide something please confirm from the user if the identified details are correct. If they are correct, suggest the next healthy meal with the detailed recipe. If any details are incorrect, please ask for additional information."
        response = chat.send_message(message)
        logger.info(f"Generated content for message")
        logger.info(response)
        return response.candidates[0].content.parts[0]
    except Exception as e:
        logger.error(f"Error generating content for message: {e}")
        return f"Error generating content: {e}"
