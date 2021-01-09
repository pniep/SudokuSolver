FROM python:3-slim

RUN pip install flask \
    && pip install numpy

EXPOSE 80

VOLUME /application
WORKDIR /application

CMD ["python", "ui.py"]

