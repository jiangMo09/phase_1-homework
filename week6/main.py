import secrets
from fastapi import FastAPI, Request, Form, Query
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from starlette.middleware.sessions import SessionMiddleware

secret_key = secrets.token_bytes(32)

app = FastAPI()
app.add_middleware(SessionMiddleware, secret_key=secret_key)
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")


@app.get("/", response_class=HTMLResponse)
def index(request: Request):
    return templates.TemplateResponse(
        "index.html", {"request": request, "header_text": "歡迎光臨，請輸入帳號密碼"}
    )


@app.post("/signin")
def signin(request: Request, username: str = Form(None), password: str = Form(None)):
    error_message = None

    if not username or not password:
        error_message = "Please enter username and password"
    elif username != "test" or password != "test":
        error_message = "Username or password is not correct"

    if error_message:
        return RedirectResponse(f"/error?message={error_message}", status_code=302)

    request.session["SIGNED_IN"] = True
    return RedirectResponse("/member", status_code=302)


@app.get("/signout")
def signout(request: Request):
    request.session.clear()
    return RedirectResponse("/", status_code=302)


@app.get("/member", response_class=HTMLResponse)
def member(request: Request):
    if not request.session.get("SIGNED_IN", False):
        return RedirectResponse("/", status_code=302)

    response = templates.TemplateResponse(
        "/member/index.html",
        {"request": request, "header_text": "歡迎光臨，這是會員頁"},
    )
    response.headers["Cache-Control"] = "no-cache, no-store"

    return response


@app.get("/error", response_class=HTMLResponse)
def error(request: Request, message: str = Query(None)):
    return templates.TemplateResponse(
        "/error/index.html",
        {"request": request, "message": message, "header_text": "失敗頁面"},
    )


@app.get("/square/{number}")
def square(request: Request, number: int):
    return templates.TemplateResponse(
        "/squared_number/index.html",
        {
            "request": request,
            "squared_number": number**2,
            "header_text": "正整數平方計算結果",
        },
    )
