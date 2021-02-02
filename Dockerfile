FROM mcr.microsoft.com/azure-functions/python:3.0-python3.8

ENV host:logger:consoleLoggingMode=always

COPY . /home/stromabrechnung

RUN cd /home/stromabrechnung && pip install -r requirements.txt