from fastapi import APIRouter, Form
from fastapi.responses import JSONResponse
from agent import handle_contact_form_submission  # Your logic

router = APIRouter()

@router.post("/submit-contact-form")
async def submit_contact_form(
    user_name: str = Form(...),
    user_email: str = Form(...),
    message_content: str = Form(...)
):
    try:
        result = handle_contact_form_submission(user_name, user_email, message_content)
        return JSONResponse(content=result)
    except Exception as e:
        return JSONResponse(status_code=500, content={"error": str(e)})
