from fastapi import FastAPI, Form, Request, Depends
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from starlette.middleware.sessions import SessionMiddleware

from random import randint

from models import Person, User
from serializer import serializer, deserializer


app = FastAPI()
app.add_middleware(SessionMiddleware, secret_key='Sergey Nikolaev')
templates = Jinja2Templates(directory="templates")

NUMBER_OF_EXTRASENSE = 5


async def get_session(request: Request):
    return request.session


@app.post('/', response_class=HTMLResponse)
async def main_loop(
        request: Request,
        answer: int = Form(default=None),
        enter_answer: int = Form(),
        session_data: dict = Depends(get_session)
):

    error_message = ''

    #получение объектов
    if session_data:
        user = deserializer(request, 'class_user')
        extrasenses = deserializer(request, 'class_extrasenses')
        status = request.session.get('status')
    else:
        extrasenses = [Person() for i in range(NUMBER_OF_EXTRASENSE)]
        user = User()
        status = False

    # обработка данных из формы
    if enter_answer == 0:
        for extrasens in extrasenses:
            extrasens.add_answer(randint(10, 99))
        status = True

    if enter_answer == 1:
        try:
            user.validate_answer(answer)
        except TypeError:
            error_message = 'Введенные данные должны быть целым числом'
        except ValueError:
            error_message = 'Число должно быть двухзначным'
        else:
            user.add_answer(answer)
            for extrasens in extrasenses:
                extrasens.match(extrasens.answer[-1], answer)
            status = False

    data = get_data_for_templates(user, extrasenses, status)

    #запись данных в сессию
    session_data['status'] = status
    session_data['class_extrasenses'] = serializer(extrasenses)
    session_data['class_user'] = serializer(user)

    return templates.TemplateResponse('index.html',
        {'request': request, 'data': data, 'error_message': error_message}
    )


@app.get('/', response_class=HTMLResponse)
async def formation_start_page(request: Request, session_data: dict = Depends(get_session)):
    session_data = session_data or {}
    data = {}

    if session_data:
        user = deserializer(request, 'class_user')
        extrasenses = deserializer(request, 'class_extrasenses')
        status = session_data['status']
        data = get_data_for_templates(user, extrasenses, status)
    else:
        data['status'] = False

    return templates.TemplateResponse("index.html", {'request': request, "data": data})


def get_data_for_templates(user, extrasenses, status):
    data = {'user': user.answer,
            'extrasenses': [vars(extrasens) for extrasens in extrasenses],
            'status': status}
    return data


@app.get('/clear-session')  # сброс сессии
async def clear_session(session_data: dict = Depends(get_session)):
    session_data.clear()
    return {'Result': 'Session data is clearing!'}
