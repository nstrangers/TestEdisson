from fastapi import FastAPI, Form, Request, Depends
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from starlette.middleware.sessions import SessionMiddleware

from models import Person, User
from exceptions import InvalidAnswer
from serializers import serialize, deserialize


app = FastAPI()
app.add_middleware(SessionMiddleware, secret_key='Sergey Nikolaev')
templates = Jinja2Templates(directory="templates")

NUMBER_OF_EXTRASENSE = 5


async def get_session(request: Request):
    return request.session


@app.post('/', response_class=HTMLResponse)
async def get_user_answer(
        request: Request,
        answer: int = Form(default=None),
        session_data: dict = Depends(get_session)
):

    #получение объектов
    if session_data:
        user = deserialize(session_data['class_user'])
        extrasenses = deserialize(session_data['class_extrasenses'])
        status = session_data['status']
    else:
        extrasenses = [Person() for i in range(NUMBER_OF_EXTRASENSE)]
        user = User()
        status = False

    # обработка данных из формы
    error_message = ''
    if not status:
        for extrasens in extrasenses:
            extrasens.add_guess()
        status = True
    else:
        try:
            if not isinstance(answer, int):
                raise InvalidAnswer('Загаданное число должно быть целым числом')
            if answer < 10 or answer > 99:
                raise InvalidAnswer('Загаданное число должно быть двузначным')

        except InvalidAnswer as error_msg:
            error_message = error_msg

        else:
            user.add_answer(answer)
            for extrasens in extrasenses:
                extrasens.change_rating(answer)
            status = False

    data = get_data_for_templates(user, extrasenses, status)
    #запись данных в сессию
    session_data['status'] = status
    session_data['class_extrasenses'] = serialize(extrasenses)
    session_data['class_user'] = serialize(user)

    return templates.TemplateResponse('index.html',
        {'request': request, 'data': data, 'error_message': error_message}
    )


@app.get('/', response_class=HTMLResponse)
async def start_page(request: Request, session_data: dict = Depends(get_session)):
    session_data = session_data or {}
    data = {}

    if session_data:
        user = deserialize(session_data['class_user'])
        extrasenses = deserialize(session_data['class_extrasenses'])
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
