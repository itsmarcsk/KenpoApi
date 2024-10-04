FROM python:3.12.6


WORKDIR /code


COPY requirements.txt /code/requirements.txt


RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt



COPY BBDD/mongodb /code/BBDD/mongodb
COPY BBDD/mysql /code/BBDD/mysql
COPY tools /code/tools
COPY ./app /code/app


CMD ["fastapi", "run", "app/main.py", "--port", "80"]