# our base image
FROM python:3.7
RUN pip install --upgrade pip 
# specify the port number the container should expose
EXPOSE 3000

# run the application
CMD ["python", "./server.py"]