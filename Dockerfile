FROM python:3.9
COPY . .
RUN pip install mysql-connector-python
RUN pip install requests
CMD ["python", "Bitcoin_Py_Sql.py"]
