from fastapi import FastAPI, BackgroundTasks, UploadFile, File, Form
from starlette.responses import JSONResponse
from starlette.requests import Request
from fastapi_mail import FastMail, MessageSchema,ConnectionConfig
from pydantic import EmailStr
from pydantic import EmailStr, BaseModel
from typing import List



class EmailSchema(BaseModel):
    email: List[EmailStr]


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


@app.post("/email")
async def simple_send(email: EmailSchema) -> JSONResponse:

    message = MessageSchema(
        subject="Fastapi-Mail module",
        recipients=['elvissegbawu@gmail.com'],  # List of recipients, as many as you can pass 
        body=html,
        subtype="html"
        )

    fm = FastMail(conf)
    await fm.send_message(message)
    return JSONResponse(status_code=200, content={"message": "email has been sent"})