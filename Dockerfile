FROM python:3.10.12-slim

RUN pip install --upgrade pip

COPY requirements.txt .

RUN pip3 install -r /requirements.txt --no-cache-dir

COPY ../ .

WORKDIR .

CMD ["python3", "main.py"]