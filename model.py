import pymysql
from pymysql.cursors import DictCursor
from config import Config


def get_connection(autocommit=True):
    """
    Fungsi koneksi ke TiDB Cloud.
    Semua konfigurasi database diambil dari file .env lewat config.py.
    """

    db_config = {
        "host": Config.TIDB_HOST,
        "port": Config.TIDB_PORT,
        "user": Config.TIDB_USER,
        "password": Config.TIDB_PASSWORD,
        "database": Config.TIDB_DATABASE,
        "autocommit": autocommit,
        "cursorclass": DictCursor,
        "connect_timeout": 15,
    }

    if Config.CA_PATH:
        db_config["ssl"] = {
            "ca": Config.CA_PATH,
            "check_hostname": True,
        }
    else:
        db_config["ssl"] = {
            "check_hostname": False,
        }

    return pymysql.connect(**db_config)
