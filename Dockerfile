#############
## Base image
FROM python:3.8-alpine AS Base

ARG BRAINTREE_MERCHANT_ID
ARG BRAINTREE_PUBLIC_KEY
ARG BRAINTREE_PRIVATE_KEY

ENV BRAINTREE_MERCHANT_ID=$BRAINTREE_MERCHANT_ID
ENV BRAINTREE_PUBLIC_KEY=$BRAINTREE_PUBLIC_KEY
ENV BRAINTREE_PRIVATE_KEY=$BRAINTREE_PRIVATE_KEY

COPY requirements.txt /tmp/requirements.txt
RUN pip install -r /tmp/requirements.txt

COPY src/ /beautiful-payment-api/src
COPY lib/ /beautiful-payment-api/lib
COPY swagger.yaml /beautiful-payment-api/
WORKDIR /beautiful-payment-api

CMD gunicorn --bind 0.0.0.0:$PORT src.wsgi

###################
## Local deployment
FROM Base AS Local
ENV PORT 5000

####################
## Heroku deployment
FROM Base AS Production
