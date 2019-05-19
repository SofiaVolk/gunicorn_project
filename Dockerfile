FROM mysql:5.7

COPY requirements.txt .

RUN pip install -r requirements.txt

WORKDIR ./app

COPY . .

COPY gunicorn .

RUN cd gunicorn && python setup.py install

ENTRYPOINT ["python"]
