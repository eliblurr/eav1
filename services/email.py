from fastapi_mail import FastMail, MessageSchema,ConnectionConfig
from fastapi import BackgroundTasks, UploadFile, File, Form
from pydantic import EmailStr, BaseModel
from typing import List

class EmailSchema(BaseModel):
    email: List[EmailStr]

fm = FastMail(conf)

conf = ConnectionConfig(
    MAIL_USERNAME = "your@email.com",
    MAIL_PASSWORD = "strong_password",
    MAIL_PORT = 587,
    MAIL_SERVER = "your mail server",
    MAIL_TLS = True,
    MAIL_SSL = False
)

html = """
<html> 
<body>
<p>Hi This test mail
<br>{Thanks for using Fastapi-mail}</p> 
</body> 
</html>
"""

template = """
<html> 
<body>
{}
</body> 
</html>
"""

async def simple_send(email: EmailSchema,subject: str, body: List[str]):

    template.format(create_paragraphs(body))

    message = MessageSchema(
        subject="Fastapi-Mail module",
        recipients=email.dict().get("email"),  # List of recipients, as many as you can pass 
        body=template,
        subtype="html"
    )

    await fm.send_message(message)

async def send_in_background(background_tasks: BackgroundTasks,email: EmailSchema,subject: str, body: List[str]):

    template.format(create_paragraphs(body))

    message = MessageSchema(
        subject=subject,
        recipients=email.dict().get("email"),
        body=template,
        subtype="html"
    )

    background_tasks.add_task(fm.send_message,message)
    return 'sent'

async def send_file(background_tasks: BackgroundTasks,file: UploadFile = File(...),email:EmailStr = Form(...)):

    message = MessageSchema(
            subject="Fastapi mail module",
            recipients=[email],
            body="Simple background task ",
            attachments=[file]
            )

    background_tasks.add_task(fm.send_message,message)

def create_paragraphs( body: List[str]):
    for paragraph in body:
        paragraphs += "<p>{paragraph}</p>"
    
    return paragraphs
