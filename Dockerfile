FROM python:3

ARG GRAPNEL_ENV

ENV GRAPNEL_ENV=${GRAPNEL_ENV} \
    PYTHONFAULTHANDLER=1 \
    PYTHONUNBUFFERED=1 \
    PYTHONHASHSEED=random \
    PIP_NO_CACHE_DIR=off \
    PIP_DISABLE_PIP_VERSION_CHECK=on \
    PIP_DEFAULT_TIMEOUT=100 \
    POETRY_VERSION=0.12.15 \
    PATH=${PATH}:/root/.poetry/bin

SHELL ["/bin/bash", "-c"]

RUN curl -sSL https://raw.githubusercontent.com/sdispater/poetry/master/get-poetry.py | python

WORKDIR /usr/grapnel

COPY ./pyproject.toml .
COPY ./poetry.lock .
COPY ./README.rst .

RUN poetry config settings.virtualenvs.create false 
RUN poetry install $(test "GRAPNEL_ENV" == production && echo "--no-dev") --no-interaction --no-ansi

COPY ./src ./src
COPY ./tests ./tests
COPY ./tox.ini .
COPY ./pylama.ini .
COPY ./.coveragerc .

CMD [ "poetry", "run", "tox" ]