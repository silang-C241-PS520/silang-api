FROM python:3.10

ARG DB_PASSWORD
ARG JWT_SECRET_KEY

ENV DB_PASSWORD ${DB_PASSWORD}
ENV JWT_SECRET_KEY ${JWT_SECRET_KEY}

WORKDIR /code

COPY ./requirements.txt /code/requirements.txt

RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt

COPY ./src /code/src

EXPOSE 8000

CMD ["fastapi", "run", "src/main.py", "--port", "8000"]