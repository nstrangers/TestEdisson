from fastapi import FastAPI, Form, Request, Depends
from fastapi.responses import HTMLResponse
from starlette.middleware.sessions import SessionMiddleware
from fastapi.templating import Jinja2Templates

from random import randint
import json

from models import Person, User

app = FastAPI()
app.add_middleware(SessionMiddleware, secret_key='Sergey Nikolaev')
templates = Jinja2Templates(directory="templates")

NUMBER_OF_EXTRASENSE = 5


async def get_session(request: Request):
    return request.session


@app.post('/', response_class=HTMLResponse)
async def my_post(
        request: Request,
        answer: int = Form(default=None),
        control: int = Form(),
        session_data: dict = Depends(get_session)
):
    global user
    global extrasenses

    if not session_data:
        extrasenses = [Person() for i in range(NUMBER_OF_EXTRASENSE)]
        user = User()

    if answer is None and control == 0:
        for extrasens in extrasenses:
            extrasens.add_answer(randint(10, 99))
        status = True
        session_data['extrasenses'] = [vars(extrasens) for extrasens in extrasenses]
        session_data['status'] = status

    if answer is not None and validator(answer) and control == 1:
        user.add_answer(answer)
        for extrasens in extrasenses:
            extrasens.match(extrasens.answer[-1], answer)
        session_data['user'] = user.answer
        session_data['extrasenses'] = [vars(extrasens) for extrasens in extrasenses]
        status = False
        session_data['status'] = status
    return templates.TemplateResponse("index.html", {'request': request, 'data': session_data})


@app.get('/', response_class=HTMLResponse)
async def my_get(request: Request, session_data: dict = Depends(get_session)):
    session_data = session_data or {}
    if not session_data:
        session_data['status'] = False
    return templates.TemplateResponse("index.html", {'request': request, "data": session_data})


def validator(answer):
    return 10 <= answer <= 99


@app.get('/clear-session')  # сброс сессии
async def clear_session(session_data: dict = Depends(get_session)):
    session_data.clear()
    return {'Result': 'Session data is clearing!'}
