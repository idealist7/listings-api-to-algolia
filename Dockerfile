FROM python:3.13.3
WORKDIR /app
ADD requirements.txt /app/requirements.txt
RUN pip install -r requirements.txt
ADD . /app/.
RUN pip install -e .
