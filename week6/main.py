import secrets
from fastapi import FastAPI, Request, Form, Query
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from starlette.middleware.sessions import SessionMiddleware
import mysql.connector

from utils.mysql import connection_mysql, close_mysql
from utils.messages import get_messages, add_messages

secret_key = secrets.token_bytes(32)

app = FastAPI()
app.add_middleware(SessionMiddleware, secret_key=secret_key)
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")


@app.get("/", response_class=HTMLResponse)
def index(request: Request):
    return templates.TemplateResponse(
        "index.html", {"request": request, "header_text": "歡迎光臨，請註冊登入系統"}
    )


@app.post("/signin")
def signin(request: Request, username: str = Form(None), password: str = Form(None)):
    error_message = None
    name = None

    if not username or not password:
        error_message = "Please enter username and password"
    else:
        connection, cursor = connection_mysql()

        try:
            query = "SELECT * FROM member WHERE username = %s AND password = %s"
            values = (username, password)
            cursor.execute(query, values)
            user = cursor.fetchone()

            if user:
                name = user[1]
            else:
                error_message = "帳號或是密碼輸入錯誤"
        except mysql.connector.Error as err:
            error_message = f"資料庫連線錯誤: {err}"
        finally:
            close_mysql(cursor, connection)

    if error_message:
        return RedirectResponse(f"/error?message={error_message}", status_code=302)

    request.session["SIGNED_IN"] = True
    request.session["NAME"] = name
    request.session["USERNAME"] = username
    return RedirectResponse("/member", status_code=302)


@app.get("/signout")
def signout(request: Request):
    request.session.clear()
    return RedirectResponse("/", status_code=302)


@app.post("/signup")
def signup(
    signupName: str = Form(...),
    signupAccount: str = Form(...),
    signupPassword: str = Form(...),
):
    error_message = None
    connection, cursor = connection_mysql()

    try:
        query = "SELECT * FROM member WHERE username = %s"
        cursor.execute(query, (signupAccount,))
        existing_user = cursor.fetchone()

        if existing_user:
            error_message = "重複的使用者名稱"
        else:
            query = "INSERT INTO member (name, username, password) VALUES (%s, %s, %s)"
            values = (signupName, signupAccount, signupPassword)
            cursor.execute(query, values)
            connection.commit()

    except mysql.connector.Error as err:
        error_message = f"資料庫連線錯誤: {err}"

    finally:
        close_mysql(cursor, connection)

    if error_message:
        return RedirectResponse(f"/error?message={error_message}", status_code=302)
    else:
        return RedirectResponse("/", status_code=302)


@app.get("/member", response_class=HTMLResponse)
def member(request: Request):
    if not request.session.get("SIGNED_IN", False):
        return RedirectResponse("/", status_code=302)

    name = request.session.get("NAME", "")
    messages = get_messages()

    response = templates.TemplateResponse(
        "/member/index.html",
        {
            "request": request,
            "header_text": "歡迎光臨，這是會員頁",
            "name": name,
            "messages": messages,
        },
    )
    response.headers["Cache-Control"] = "no-cache, no-store"

    return response


@app.post("/createMessage")
def createMessage(request: Request, message: str = Form(...)):
    username = request.session.get("USERNAME", "")

    add_messages(username, message)

    return RedirectResponse("/member", status_code=302)


@app.get("/error", response_class=HTMLResponse)
def error(request: Request, message: str = Query(None)):
    return templates.TemplateResponse(
        "/error/index.html",
        {"request": request, "message": message, "header_text": "失敗頁面"},
    )
