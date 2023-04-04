FROM python:3-slim
WORKDIR /usr/src/app
COPY ./product_notification.py ./requirements.txt ./
RUN python -m pip install --no-cache-dir -r requirements.txt
CMD ["python", "./product_notification.py"]