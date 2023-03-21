FROM python:3-slim
WORKDIR /usr/src/app
COPY requirements.txt ./
COPY secret.json ./
COPY invokes.py ./
RUN python -m pip install --no-cache-dir -r requirements.txt
COPY ./auth.py .
CMD [ "python", "./auth.py" ]