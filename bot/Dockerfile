FROM python:latest
RUN mkdir -p /usr/src/app
WORKDIR /usr/src/app
COPY requirements.txt ./
COPY bot.py ./
RUN pip3 install -r requirements.txt
EXPOSE 8888
CMD ["python3", "bot.py"]