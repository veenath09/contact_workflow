import os 
import langchain
from langchain_core.prompts import PromptTemplate
from langchain_openai import ChatOpenAI
from langchain_google_genai import ChatGoogleGenerativeAI
from dotenv import load_dotenv
load_dotenv()

# llm  = ChatOpenAI(
#     model = "gpt-o4-mini",
#     temperature = 0.7,
# )



llm = ChatGoogleGenerativeAI(
    model = "gemini-2.5-flash",
    temperature = 0.7,
)


Prompt = ""

result = llm.invoke("What is the capital of France?")

print(result)







# import smtplib
# from email.mime.text import MIMEText
# from email.mime.multipart import MIMEMultipart

# def send_email(subject, body, to):
#     from_email = "veenathinrisedigital@gmail.com"
#     from_password = "dycb azhi uphg lwhj"

#     # Create a proper email message with UTF-8 encoding
#     message = MIMEMultipart()
#     message["From"] = from_email
#     message["To"] = to
#     message["Subject"] = subject
    
#     # Attach the body with UTF-8 encoding
#     message.attach(MIMEText(body, "plain", "utf-8"))

#     try:
#         # Connect to the SMTP server
#         with smtplib.SMTP("smtp.gmail.com", 587) as server:
#             server.starttls()  # Upgrade the connection to a secure encrypted SSL/TLS connection
#             server.login(from_email, from_password)  # Log in to the email account
#             server.sendmail(from_email, to, message.as_string())  # Send the email
#             print("Email sent successfully!")
#     except Exception as e:
#         print(f"Error sending email: {e}")

# send_email("Test Subject", "This is a test email body.", "veenathwickramaarchchi@gmail.com")