FROM python:3.10

WORKDIR /code

RUN apt-get update && apt-get install libgl1 -y

COPY ./requirements.txt /code/requirements.txt

RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt

COPY ./src /code/src

EXPOSE 8000

CMD ["fastapi", "run", "src/main.py", "--port", "8000"]