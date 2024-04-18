FROM python:3.10.12-slim

RUN pip install --upgrade pip

RUN python3 -m venv venv

RUN source venv/bin/activate

COPY requirements.txt .

RUN pip3 install -r /requirements.txt --no-cache-dir

COPY ../ .

WORKDIR .

CMD ["python3", "main.py"]