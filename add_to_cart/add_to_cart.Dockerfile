FROM python:3-slim
WORKDIR /usr/src/app
COPY ./add_to_cart.py ./invokes.py ./requirements.txt ./
RUN python -m pip install --no-cache-dir -r requirements.txt
CMD [ "python", "./add_to_cart.py" ]