import secrets
import logging

from fastapi import Body, FastAPI, Request, Form, Query
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from starlette.middleware.sessions import SessionMiddleware
import mysql.connector
from passlib.context import CryptContext

from utils.mysql import get_db_connection, execute_query
from utils.messages import get_messages, add_messages

logging.basicConfig(filename="app.log", level=logging.INFO)
logger = logging.getLogger(__name__)

secret_key = secrets.token_bytes(32)
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

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
    user_id = None

    if not username or not password:
        error_message = "Please enter username and password"
    else:

        try:
            connection = get_db_connection()
            query = "SELECT * FROM member WHERE username = %s"
            user = execute_query(connection, query, (username,))

            if user and pwd_context.verify(password, user[3]):
                user_id = user[0]
                name = user[1]
            else:
                error_message = "帳號或是密碼輸入錯誤"
        except mysql.connector.Error as err:
            logger.error("資料庫連線錯誤: %s", err)
            error_message = "資料庫連線錯誤: 請聯繫工程師"

    if error_message:
        return RedirectResponse(f"/error?message={error_message}", status_code=302)

    request.session["SIGNED_IN"] = True
    request.session["NAME"] = name
    request.session["USER_ID"] = user_id
    request.session["USER_NAME"] = username
    return RedirectResponse("/member", status_code=302)


@app.get("/signout")
def signout(request: Request):
    request.session.clear()
    return RedirectResponse("/", status_code=302)


@app.post("/signup")
def signup(
    signup_name: str = Form(...),
    signup_account: str = Form(...),
    signup_password: str = Form(...),
):
    error_message = None

    try:
        connection = get_db_connection()
        query = "SELECT * FROM member WHERE username = %s"
        existing_user = execute_query(
            connection, query, (signup_account,), fetch_method="fetchone"
        )

        if existing_user:
            error_message = "重複的使用者名稱"
        else:
            connection = get_db_connection()
            hashed_password = pwd_context.hash(signup_password)
            query = "INSERT INTO member (name, username, password) VALUES (%s, %s, %s)"
            values = (signup_name, signup_account, hashed_password)
            existing_user = execute_query(
                connection, query, values, fetch_method="fetchone"
            )

    except mysql.connector.Error as err:
        logger.error("資料庫連線錯誤: %s", err)
        error_message = "資料庫連線錯誤: 請聯繫工程師"

    if error_message:
        return RedirectResponse(f"/error?message={error_message}", status_code=302)
    else:
        return RedirectResponse("/", status_code=302)


@app.get("/member", response_class=HTMLResponse)
def member(request: Request):
    if not request.session.get("SIGNED_IN", False):
        return RedirectResponse("/", status_code=302)

    name = request.session.get("NAME", "")
    user_name = request.session.get("USER_NAME", "")
    messages = get_messages()

    response = templates.TemplateResponse(
        "/member/index.html",
        {
            "request": request,
            "header_text": "歡迎光臨，這是會員頁",
            "name": name,
            "messages": messages,
            "user_name": user_name,
        },
    )
    response.headers["Cache-Control"] = "no-cache, no-store"

    return response


@app.post("/createMessage")
def createMessage(request: Request, message: str = Form(...)):
    user_id = request.session.get("USER_ID", "")

    add_messages(user_id, message)

    return RedirectResponse("/member", status_code=302)


@app.post("/deleteMessage")
def deleteMessage(message_id: int = Form(...)):
    connection = get_db_connection()
    query = "DELETE FROM message WHERE id = %s"
    execute_query(connection, query, (message_id,))


@app.get("/api/member")
def get_member(request: Request, username: str = Query(None)):
    if not request.session.get("SIGNED_IN", False):
        return {"data": None}

    try:
        connection = get_db_connection()
        query = "SELECT * FROM member WHERE username = %s"
        find_member = execute_query(
            connection, query, (username,), fetch_method="fetchone"
        )

        if find_member:
            return {
                "data": {
                    "id": find_member[0],
                    "name": find_member[1],
                    "username": find_member[2],
                }
            }
        else:
            return {"data": None}

    except mysql.connector.Error as err:
        logger.error("資料庫連線錯誤: %s", err)
        return {"data": None}


@app.patch("/api/member")
def update_member_name(request: Request, member_data: dict = Body(...)):
    if not request.session.get("SIGNED_IN", False):
        return {"error": True}

    try:
        user_id = request.session.get("USER_ID")
        new_name = member_data.get("name")

        if new_name:
            connection = get_db_connection()
            query = "UPDATE member SET name = %s WHERE id = %s"
            execute_query(connection, query, (new_name, user_id))
            request.session["NAME"] = new_name

            return {"ok": True}
        else:
            return {"error": True}

    except mysql.connector.Error as err:
        logger.error("資料庫連線錯誤: %s", err)
        return {"error": True}


@app.get("/error", response_class=HTMLResponse)
def error(request: Request, message: str = Query(None)):
    return templates.TemplateResponse(
        "/error/index.html",
        {"request": request, "message": message, "header_text": "失敗頁面"},
    )
