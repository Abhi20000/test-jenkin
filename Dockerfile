FROM python
WORKDIR /app
COPY . /app
RUN pip install mysql.connector.python
RUN pip install flask
CMD ["python","Abhi.py"]
