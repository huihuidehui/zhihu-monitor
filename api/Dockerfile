FROM python:3.7
RUN mkdir /code
WORKDIR /code
COPY requirments.txt .
RUN pip install -r requirements.txt -i https://pypi.douban.com/simple
EXPOSE 5000

CMD ["flask","run","-h","0.0.0.0"]
CMD ["gunicorn", "start:app", "-c", "./gunicorn.conf.py"]
