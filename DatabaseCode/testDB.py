import pymysql

# The SQLAlchemy engine will help manage interactions, including automatically
# managing a pool of connections to your database
import datetime
import logging
import os

from flask import Flask, render_template, request, Response
import sqlalchemy

db_user = os.environ.get("DB_USER")
db_pass = os.environ.get("DB_PASS")
db_name = os.environ.get("DB_NAME")
cloud_sql_connection_name = os.environ.get("CLOUD_SQL_CONNECTION_NAME")

app = Flask(__name__)
logger = logging.getLogger()

db = sqlalchemy.create_engine(
    # Equivalent URL:
    # mysql+pymysql://<db_user>:<db_pass>@/<db_name>?unix_socket=/cloudsql/<cloud_sql_instance_name>
    sqlalchemy.engine.url.URL(
        drivername='mysql+pymysql',
        username="samyibrahim",
        password="samizosan",
        database="IOT_SMART_BABY_MONITORING",
        query={
            'unix_socket': '/cloudsql/{}'.format("iotsmartbabymonitoringcloud:us-east1:iot-smartbaby-monitoring")
        }
    ),
    # Pool size is the maximum number of permanent connections to keep.
    pool_size=5,
    # Temporarily exceeds the set pool_size if no connections are available.
    max_overflow=2,
    # 'pool_timeout' is the maximum number of seconds to wait when retrieving a
    # new connection from the pool. After the specified amount of time, an
    # exception will be thrown.
    pool_timeout=30,  # 30 seconds
    # 'pool_recycle' is the maximum number of seconds a connection can persist.
    # Connections that live longer than the specified amount of time will be
    # reestablished
    pool_recycle=1800,  # 30 minutes
)

@app.before_first_request
def create_tables():
    # Create tables (if they don't already exist)
    with db.connect() as conn:
        conn.execute(
            "CREATE TABLE IF NOT EXISTS test "
            "( id SERIAL NOT NULL, hold CHAR(6) NOT NULL, "
            "PRIMARY KEY (id) );"
        )

@app.route('/', methods=['POST'])
def save_test(hold):
    stmt = sqlalchemy.text(
        "INSERT INTO test (hold)"
        " VALUES (':hold')"
    )
    try:
        # Using a with statement ensures that the connection is always released
        # back into the pool at the end of statement (even if an error occurs)
        with db.connect() as conn:
            conn.execute(stmt, hold=hold)
    except Exception as e:
        # If something goes wrong, handle the error in this section. This might
        # involve retrying or adjusting parameters depending on the situation.
        # [START_EXCLUDE]
        logger.exception(e)
        return Response(
            status=500,
            response="Unable to successfully cast vote! Please check the "
                     "application logs for more details."
        )

if __name__ == '__main__':
    create_tables()
    save_test("samy")
