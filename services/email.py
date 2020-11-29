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
    MAIL_USERNAME = "execarray@fastmail.com",
    MAIL_PASSWORD = "Zack2000black;",
    MAIL_FROM = "execarray@fastmail.com",
    MAIL_PORT = 465,
    MAIL_SERVER = "smtp.fastmail.com",
    MAIL_TLS = True,
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

    print(email.get("email"))

    message = MessageSchema(
        subject="Fastapi-Mail module",
        recipients=email.get("email"),  # List of recipients, as many as you can pass 
        body=html,
        subtype="html"
        )

    fm = FastMail(conf)
    await fm.send_message(message)
    return JSONResponse(status_code=200, content={"message": "email has been sent"})

# from fastapi import FastAPI, BackgroundTasks, UploadFile, File, Form, HTTPException
# from starlette.responses import JSONResponse
# from starlette.requests import Request
# from fastapi_mail import FastMail, MessageSchema,ConnectionConfig
# from pydantic import EmailStr
# from pydantic import EmailStr, BaseModel
# from typing import List

# class EmailSchema(BaseModel):
#     email: List[EmailStr]

# conf = ConnectionConfig(
#     MAIL_USERNAME = "devmail0233@gmail.com",
#     MAIL_PASSWORD = "password0233",
#     MAIL_FROM = "devmail0233@gmail.com",
#     MAIL_PORT = 465,
#     MAIL_SERVER = "smtp.gmail.com",
#     MAIL_TLS = False,
#     MAIL_SSL = False
# )

# # conf = ConnectionConfig(
# #     MAIL_USERNAME = "devmail0233@gmail.com",
# #     MAIL_PASSWORD = "password0233",
# #     MAIL_FROM = "devmail0233@gmail.com",
# #     MAIL_PORT = 587,
# #     MAIL_SERVER = "smtp.googlemail.com",
# #     MAIL_TLS = True,
# #     MAIL_SSL = False
# # )

# html = """
# <p>Hi this test mail, thanks for using Fastapi-mail</p> 
# """

# async def simple_send():

#     message = MessageSchema(
#         subject="Fastapi-Mail module",
#         recipients=['elvissegbawu@gmail.com'],
#         body=html,
#         subtype="html"
#     )

#     try:
#         fm = FastMail(conf)
#     except:
#         raise HTTPException(status_code=409)

#     await fm.send_message(message)
#     return JSONResponse(status_code=200, content={"message": "email has been sent"})


# async def awesome_fastapi_func_1():
#     #as gmail requires TLS connection, therefore you require to set tls to True
#     # mail = FastMail(username="devmail0233@gmail.com",password="password0233",tls=True,port="587")

#     print(dir(FastMail.__init__))
#     print(FastMail)

    # await  mail.send_message(recipient=['elvissegbawu@gmail.com'],subject="Test email from fastapi-mail", body=html, text_format="html")

    # return JSONResponse(status_code=200, content={"message": f"email has been sent"})

# from fastapi_mail import FastMail, MessageSchema,ConnectionConfig
# from fastapi import BackgroundTasks, UploadFile, File, Form
# from pydantic import EmailStr, BaseModel
# from typing import List

# import os

# class EmailSchema(BaseModel):
#     email: List[EmailStr]

# conf = ConnectionConfig(
#     MAIL_USERNAME = "devmail0233@gmail.com",
#     MAIL_PASSWORD = "password0233",
#     MAIL_PORT = 465,
#     MAIL_SERVER = "smtp.fastmail.com",
#     MAIL_TLS = True,
#     MAIL_SSL = False
# )

# fm = FastMail(conf)

# # fm = FastMail(email="devmail0233@gmail.com",password="password0233",tls=True,port="587",services="gmail")

# html = """
# <html> 
# <body>
# <p>Hi This test mail
# <br>{Thanks for using Fastapi-mail}</p> 
# </body> 
# </html>
# """

# template = """
# <html> 
# <body>
# {}
# </body> 
# </html>
# """

# async def send_email():
#     message = MessageSchema(
#         subject="Fastapi-Mail module",
#         recipients=['elvissegbawu@gmail.com'],  # List of recipients, as many as you can pass 
#         body='sdd',
#         subtype="html"
#     )

#     await fm.send_message(message)
#     return


# async def awesome_fastapi_func_1():
#     print(dir(FastMail))
#     print(FastMail.__init__)
#     #as gmail requires TLS connection, therefore you require to set tls to True
#     mail = FastMail(email="devmail0233@gmail.com",password="password0233",tls=True,port="587",service="gmail")

#     await  mail.send_message(recipient='elvissegbawu@gmail.com',subject="Test email from fastapi-mail", body=html, text_format="html")

#     # return HTTPException(status_code=200)

# async def simple_send(email: List['EmailSchema'],subject: str, body: List[str]):
#     fm.send_message()

#     # template.format(create_paragraphs(body))

#     # message = MessageSchema(
#     #     subject="Fastapi-Mail module",
#     #     recipients=email,  # List of recipients, as many as you can pass 
#     #     body=template,
#     #     subtype="html"
#     # )

#     # await fm.send_message(message)

# async def send_in_background(background_tasks: BackgroundTasks,email: EmailSchema,subject: str, body: List[str]):

#     template.format(create_paragraphs(body))

#     message = MessageSchema(
#         subject=subject,
#         recipients=email.dict().get("email"),
#         body=template,
#         subtype="html"
#     )

#     background_tasks.add_task(fm.send_message,message)
#     return 'sent'

# async def send_file(background_tasks: BackgroundTasks,file: UploadFile = File(...),email:EmailStr = Form(...)):

#     message = MessageSchema(
#             subject="Fastapi mail module",
#             recipients=[email],
#             body="Simple background task ",
#             attachments=[file]
#             )

#     background_tasks.add_task(fm.send_message,message)

# def create_paragraphs( body: List[str]):

#     paragraphs = ''

#     for paragraph in body:
#         paragraphs += """<p>{paragraph}</p>""".format(paragraph=paragraph)
    
#     return paragraphs



# # conf = ConnectionConfig(
# #     MAIL_USERNAME = "devmail0233@gmail.com",
# #     MAIL_PASSWORD = "password0233",
# #     MAIL_FROM = "your@email.com",
# #     MAIL_PORT = 587,
# #     MAIL_SERVER = "your mail server",
# #     MAIL_TLS = True,
# #     MAIL_SSL = False
# # )

# # conf = ConnectionConfig(
# #     MAIL_USERNAME = os.environ['MAIL_USERNAME'],
# #     MAIL_PASSWORD = os.environ['MAIL_PASSWORD'],
# #     MAIL_PORT = os.environ['MAIL_PORT'],
# #     MAIL_SERVER = os.environ['MAIL_SERVER'],
# #     MAIL_TLS = os.environ['MAIL_TLS'],
# #     MAIL_SSL = os.environ['MAIL_SSL']
# # )

# # conf = ConnectionConfig(
# #     MAIL_USERNAME = "devmail0233@gmail.com",
# #     MAIL_PASSWORD = "password0233",
# #     MAIL_PORT = 587,
# #     MAIL_TLS = True,
# # )


# # conf = ConnectionConfig(
# #     MAIL_USERNAME = "",
# #     MAIL_PASSWORD = "",
# #     MAIL_PORT = 465,
# #     MAIL_SERVER = "smtp.fastmail.com",
# #     MAIL_TLS = True,
# #     MAIL_SSL = False,
# # )

# # fm = FastMail(conf)

# # fm = FastMail(email="devmail0233@gmail.com",password="password0233",tls=True,port="587",services="gmail")
# # raise HTTPException(status_code=500, 
#             # detail="Error while processing invoice {}".format(traceback.format_exc()))
# # mail = FastMail(email="devmail0233@gmail.com",password="password0233",tls=True,port="587",services="gmail")
# # background_tasks.add_task(mail.send_message,recipient=principal.email,subject="Payment Notice",body=mail_template.payment_notice_template.format(contact_name=principal.name,amount=payment.amount,paid_in_by=payment.paid_in_by,transaction_date=payment.transaction_date,ref_code=payment.transaction_reference,transaction_reference=payment.transaction_reference),text_format="html")

