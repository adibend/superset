FROM apache/superset
WORKDIR /app
ENV SUPERSET_CONFIG_PATH /app/superset_config.py
COPY ./superset_config.py /app
COPY ./superset/user_package/ /app/superset/user_package/
