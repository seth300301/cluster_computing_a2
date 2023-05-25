FROM python:3.10.6

WORKDIR /dashboard

COPY . /dashboard

RUN pip install -r requirements.txt
RUN pip install --upgrade pip
RUN pip install --upgrade Pillow

CMD ["python3", "-m", "streamlit", "run", "Home.py"]