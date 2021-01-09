FROM python:3-slim

RUN pip install flask \
    && pip install numpy

VOLUME /application
WORKDIR /application

COPY ./ ./

EXPOSE 5000

CMD ["python", "ui.py"]

