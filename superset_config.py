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
