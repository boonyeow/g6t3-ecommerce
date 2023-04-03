FROM python:3-slin
WORKDIR /usr/src/app
COPY ./requirements.txt ./invokes.py ./amqp_setup.py ./place_an_order.py ./
RUN python -m pip install --no-cache-dir -r requirements.txt
CMD [ "python", "./make_a_review.py" ]