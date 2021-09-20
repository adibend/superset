# Superset specific config
# ROW_LIMIT = 5000

# SUPERSET_WEBSERVER_PORT = 80

# The SQLAlchemy connection string to your database backend
# This connection defines the path to the database that stores your
# superset metadata (slices, connections, tables, dashboards, ...).
# Note that the connection information to connect to the datasources
# you want to explore are managed directly in the web UI
# SQLALCHEMY_DATABASE_URI = 'sqlite:////path/to/superset.db'
SQLALCHEMY_DATABASE_URI = 'postgresql://postadmin:NgRCTbd2WdtwPlr7eyZG@db-qa-01.cv7xzvrv270p.us-east-1.rds.amazonaws.com:5432/superset'

import os
from cachelib.redis import RedisCache
import logging
from datetime import timedelta
from typing import Optional
from cachelib.file import FileSystemCache
from celery.schedules import crontab
from superset.user_package.services import (OnlineOfflinePointGetter,
                                            HotColdWaterMetricGetter)

logger = logging.getLogger()


def get_status_trend_graph(from_=None, to=None, countries=None):
    points = OnlineOfflinePointGetter(from_, to, countries).get_points()
    output = ''
    for index, point in enumerate(points):
        output += f"SELECT TIMESTAMP '{point['day']}' as __time, " \
                  f"{point['online']} as online, " \
                  f"{point['offline']} as offline "
        if not index == (len(points) - 1):
            output += ' UNION ALL '
    return output


def get_hot_cold_water_metric(from_=None, to=None, countries=None):
    return HotColdWaterMetricGetter(from_, to, countries).get_metric()


JINJA_CONTEXT_ADDONS = {
    'get_status_trend_graph': get_status_trend_graph,
    'get_hot_cold_water_metric': get_hot_cold_water_metric,
}



def env(key, default=None):
    return os.getenv(key, default)

SQLALCHEMY_TRACK_MODIFICATIONS = True
SECRET_KEY = env('SECRET_KEY', 'thisISaSECRET_1234')

FEATURE_FLAGS = {
	"ENABLE_TEMPLATE_PROCESSING": True,
}
