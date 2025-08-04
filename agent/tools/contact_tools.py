from langchain_core.tools import tool
import os 
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import gspread
from google.oauth2.service_account import Credentials
from datetime import datetime



@tool
def send_client_email(user_subject, user_body, user_email):
    """    Send an email using the Gmail SMTP server to the user acknowledging that user received the message.
    Args:
        subject (str): The subject of the email.
        body (str): The body of the email.
        to (str): The recipient's email address.
        """
    
    from_email = "veenathinrisedigital@gmail.com"
    from_password = "dycb azhi uphg lwhj"

    # Create a proper email message with UTF-8 encoding
    message = MIMEMultipart()
    message["From"] = from_email
    message["To"] = user_email
    message["Subject"] = user_subject

    # Attach the body with UTF-8 encoding
    message.attach(MIMEText(user_body, "plain", "utf-8"))

    try:
        # Connect to the SMTP server
        with smtplib.SMTP("smtp.gmail.com", 587) as server:
            server.starttls()  # Upgrade the connection to a secure encrypted SSL/TLS connection
            server.login(from_email, from_password)  # Log in to the email account
            server.sendmail(from_email, user_email, message.as_string())  # Send the email
            print("Email sent successfully!")
    except Exception as e:
        print(f"Error sending email: {e}")


@tool
def send_dept_email(department_subject, department_body, department_email):
    """    Send an email using the Gmail SMTP server.
    Args:
        subject (str): The subject of the email.
        body (str): The body of the email.
        to (str): The recipient's email address.
        """
    
    from_email = "veenathinrisedigital@gmail.com"
    from_password = "dycb azhi uphg lwhj"

    # Create a proper email message with UTF-8 encoding
    message = MIMEMultipart()
    message["From"] = from_email
    message["To"] = department_email
    message["Subject"] = department_subject

    # Attach the body with UTF-8 encoding
    message.attach(MIMEText(department_body, "plain", "utf-8"))

    try:
        # Connect to the SMTP server
        with smtplib.SMTP("smtp.gmail.com", 587) as server:
            server.starttls()  # Upgrade the connection to a secure encrypted SSL/TLS connection
            server.login(from_email, from_password)  # Log in to the email account
            server.sendmail(from_email, department_email, message.as_string())  # Send the email
            print("Email sent successfully!")
    except Exception as e:
        print(f"Error sending email: {e}")


    

@tool
def email_routing_tool(department_subject, department_body, department_email, user_email, user_subject, user_body):
    """
    Sends two emails using the Gmail SMTP server:
    1. An internal routing email to the appropriate department or team.
    2. A user acknowledgment email.

    Args:
        department_subject (str): Subject line for the internal email.
        department_body (str): Body content for the internal email.
        department_email (str): Recipient email address for the internal routing (e.g., a department inbox).
        user_email (str): The original user's email address to send the acknowledgment to.
        user_subject (str): Subject line for the acknowledgment email sent to the user.
        user_body (str): Body content for the acknowledgment email sent to the user.

    Returns:
        None
    """

    # Send acknowledgment email to the user
    agent_mail = send_dept_email(department_subject, department_body, department_email)
    user_email = send_client_email(user_subject, user_body, user_email)
    return f"Email sent to {department_email} and acknowledgment sent to {user_email}"


@tool
def log_request_to_sheet(user_name: str, user_email: str, message_content: str, department: str, department_email: str):
    """
    Logs contact form submission data to Google Sheet.
    
    Args:
        user_name (str): Name of the user submitting the form.
        user_email (str): Email address of the user.
        message_content (str): The message from the contact form.
        department (str): Department the request was routed to (SALES, SUPPORT, PARTNERSHIP).
        department_email (str): Email address of the department.
    
    Returns:
        str: Success or error message.
    """
    try:
        # Define the scope
        scope = [
            "https://www.googleapis.com/auth/spreadsheets",
            "https://www.googleapis.com/auth/drive"
        ]
        
        # Load credentials from the JSON file
        creds = Credentials.from_service_account_file("neon-poetry-467907-k3-c6c2f44fb294.json", scopes=scope)
        
        # Authorize and open the sheet
        client = gspread.authorize(creds)
        spreadsheet_id = "1ST3IWDLgNNJESD5Kb4d6FquveuaOJt3_kkKXP3JgDUg"
        sheet = client.open_by_key(spreadsheet_id).sheet1
        
        # Generate timestamp and request ID
        current_time = datetime.now()
        timestamp = current_time.strftime("%Y-%m-%d %H:%M:%S")
        request_id = f"REQ_{current_time.strftime('%Y%m%d_%H%M%S')}"
        
        # Prepare the row data
        row_data = [
            timestamp,           # Time
            request_id,          # Request_ID
            user_name,           # User's Name
            user_email,          # User's Email
            message_content,     # Request
            department,          # Department
            department_email,    # Department Email
            timestamp            # email_sent_at (using same timestamp)
        ]
        
        # Add the row to the sheet
        sheet.append_row(row_data)
        
        return f"Successfully logged request {request_id} to Google Sheet"
        
    except Exception as e:
        return f"Error logging to Google Sheet: {str(e)}"