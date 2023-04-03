FROM python:3-slim
WORKDIR /usr/src/app
COPY ./amqp_setup.py ./mail.py ./requirements.txt ./
RUN python -m pip install --no-cache-dir -r ./requirements.txt
CMD [ "python", "./mail.py" ]