FROM kong:2.0.4
USER root
RUN apk add --no-cache curl 
USER kong