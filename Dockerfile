FROM python:3
WORKDIR	/app
ADD . /app 
RUN pip3 install forex-python flask 
CMD [ "python3", "./converter-web.py" ]
