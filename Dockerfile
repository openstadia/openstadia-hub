FROM python:3.10-slim as requirements-stage

WORKDIR /tmp

RUN pip install poetry==1.6.1

COPY ./pyproject.toml ./poetry.lock /tmp/

RUN poetry export -f requirements.txt -o requirements.txt --without-hashes

FROM python:3.10-slim

WORKDIR /code

COPY --from=requirements-stage /tmp/requirements.txt /code/requirements.txt

RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt

COPY ./alembic.ini ./run.sh /code/

COPY ./openstadia_hub /code/openstadia_hub

COPY ./alembic /code/alembic

CMD ["/bin/sh", "./run.sh"]