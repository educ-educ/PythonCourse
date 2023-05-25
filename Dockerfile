# our base image
FROM python:3.8
RUN pip install --upgrade pip

COPY ./ ./
RUN pip install -r requirements.txt
# specify the port number the container should expose
EXPOSE 3000


# run the application
CMD ["python", "./server.py"]