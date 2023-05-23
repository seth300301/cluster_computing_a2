FROM python:3.10.6

ADD shortage.py .
ADD requirements.txt .
ADD config.yaml .

RUN pip install -r requirements.txt

CMD ["python3", "./shortage.py"]

