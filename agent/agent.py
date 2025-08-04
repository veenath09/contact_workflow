from .tools import send_dept_email,send_client_email, log_request_to_sheet 
from langchain_google_genai import ChatGoogleGenerativeAI
from dotenv import load_dotenv
from langchain.prompts import PromptTemplate
from datetime import datetime
from utils.prompts import contact_form_prompt

import logging
load_dotenv()

# Initialize Gemini model
llm = ChatGoogleGenerativeAI(
    model="gemini-2.5-flash",
    temperature=0.7,
)

# Bind tools
tools = [ log_request_to_sheet, send_client_email, send_dept_email]
llm_with_tools = llm.bind_tools(tools)

current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")





def handle_contact_form_submission(user_name: str, user_email: str, message_content: str) -> dict:
    """
    Handles the processing of contact form submission using LLM for intent analysis
    and invokes appropriate tool actions like sending email and logging to Google Sheets.

    Args:
        user_name (str): Name of the user submitting the form.
        user_email (str): Email address of the user.
        message_content (str): The message from the contact form.

    Returns:
        dict: A response containing status and details of tool invocations.
    """

    # Classify the request to determine department


    # Format dynamic input
    form_data = {
        "user_name": user_name,
        "user_email": user_email,
        "message_content": message_content,
    }

    message = contact_form_prompt.format(current_time=current_time, **form_data)

    # Invoke the LLM
    result = llm_with_tools.invoke(message)
    response = {"llm_response": str(result), "tool_calls": [], "status": "success"}

    # Log the request to Google Sheet first


    # Handle tool calls
    if hasattr(result, "tool_calls") and result.tool_calls:
        for tool_call in result.tool_calls:
            name = tool_call["name"]
            args = tool_call["args"]
            response["tool_calls"].append({"name": name, "args": args})
            if name == "send_client_email":
                try:
                    send_client_email.invoke(args)
            
                except Exception as e:
                    logging.exception("Email sending failed.")
                    response["status"] = "error"
                    response["error"] = str(e)
            if name == "send_dept_email":
                try:
                    send_dept_email.invoke(args)

                except Exception as e:
                    logging.exception("Email sending failed.")
                    response["status"] = "error"
                    response["error"] = str(e)

            if name == "log_request_to_sheet":
                try:
                    log_request_to_sheet.invoke(args)
                except Exception as e:
                    logging.exception("Logging to Google Sheet failed.")
                    response["status"] = "error"
                    response["error"] = str(e)

    return response
