from fastapi import FastAPI, BackgroundTasks, UploadFile, File, Form
from fastapi_mail import FastMail, MessageSchema,ConnectionConfig
from fastapi_mail.email_utils import DefaultChecker
from starlette.responses import JSONResponse
from pydantic import EmailStr, BaseModel
from starlette.requests import Request
from typing import List, Dict, Any
from pydantic import EmailStr
from static.email_templates import email_templates

class EmailSchema(BaseModel):
    email: List[EmailStr]
    body: Dict[str, Any]


conf = ConnectionConfig(
    MAIL_USERNAME = "a9f521690f65a4",
    MAIL_PASSWORD = "11480b2eec8121",
    MAIL_FROM = "elisegb-49cabc@inbox.mailtrap.io",
    MAIL_PORT = 2525,
    MAIL_SERVER = "smtp.mailtrap.io",
    MAIL_TLS = False,
    MAIL_SSL = False
)

app = FastAPI()


html = """
<p>Hi this test mail, thanks for using Fastapi-mail</p> 
"""

template = """
<p>Hi this test mail using BackgroundTasks, thanks for using Fastapi-mail</p> 
"""

# /email
@app.post("/email")
async def simple_send(email: EmailSchema) -> JSONResponse:

    message = MessageSchema(
        subject="Fastapi-Mail module",
        recipients=['elvissegbawu@gmail.com'],  # List of recipients, as many as you can pass 
        body=email_templates.html,
        subtype="html"
        )

    fm = FastMail(conf)
    await fm.send_message(message)
    return JSONResponse(status_code=200, content={"message": "email has been sent"})

# /emailbackground
async def send_in_background(background_tasks: BackgroundTasks ) -> JSONResponse:

    message = MessageSchema(
        subject="Fastapi mail module",
        recipients=['elvissegbawu@gmail.com','clay@mail.com', 'james@james.com'],
        body=email_templates.html,
        subtype="html"
        )

    fm = FastMail(conf)

    background_tasks.add_task(fm.send_message,message)

    return JSONResponse(status_code=200, content={"message": "email has been sent"})

# /file
async def send_file(background_tasks: BackgroundTasks,file: UploadFile = File(...),email:EmailStr = Form(...)) -> JSONResponse:

    message = MessageSchema(
            subject="Fastapi mail module",
            recipients=[email],
            body="Simple background task ",
            attachments=[file]
            )

    fm = FastMail(conf)

    background_tasks.add_task(fm.send_message,message)

    return JSONResponse(status_code=200, content={"message": "email has been sent"})

