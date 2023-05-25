FROM python:3.10.6

COPY main.py .
COPY process_mastodon_data.py .
COPY views.py .
COPY requirements.txt .

RUN pip install -r requirements.txt

CMD ["python3", "main.py"]

