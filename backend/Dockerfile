FROM python:3.10.6

ADD main.py .
ADD process_mastodon_data.py .
ADD views.py .

RUN pip install -r requirements.txt

CMD ["python3", "main.py"]

