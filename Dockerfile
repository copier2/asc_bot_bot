FROM python:3.10.12-slim

RUN pip3 install --upgrade pip

RUN pip3 install --root-user-action=ignore requests

COPY requirements.txt .

RUN pip3 install -r /requirements.txt --no-cache-dir

COPY ../ .

WORKDIR .

CMD ["python3", "main.py"]