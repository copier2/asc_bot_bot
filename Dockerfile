FROM python:3.10.12-slim

RUN pip install --upgrade pip

RUN python -m venv tutorial-env

RUN source tutorial-env/bin/activate

COPY requirements.txt .

RUN pip3 install -r /requirements.txt --no-cache-dir

COPY ../ .

WORKDIR .

CMD ["python3", "main.py"]