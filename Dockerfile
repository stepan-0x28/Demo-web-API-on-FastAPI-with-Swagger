FROM python:3.11-alpine3.18

WORKDIR /usr/src/app

COPY requirements.txt ./

RUN pip install --no-cache-dir -r requirements.txt

COPY main.py ./
COPY routers ./routers
COPY schemas.py ./
COPY utilities.py ./
COPY dependencies.py ./
COPY security.py ./
COPY services ./services
COPY models.py ./
COPY exceptions.py ./
COPY enumerations.py ./
COPY database.py ./

CMD [ "python", "./main.py" ]