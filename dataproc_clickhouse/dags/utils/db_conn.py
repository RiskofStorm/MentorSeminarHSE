import clickhouse_connect
from pyhive import hive
import paramiko
from pyhive import hive
from sshtunnel import SSHTunnelForwarder

def get_clickhouse_connection():
    return clickhouse_connect.get_client(host='clickhouse-server', username='default') # password='password'

def get_hive_connection():
    ssh_host = '51.250.35.56'
    ssh_port = 22
    ssh_user = 'ubuntu'
    private_key_path = '/tmp/hse_dataproc'

    local_bind_address = ('localhost', 10000)
    remote_bind_address = ('hive_server_host', 10000)

    with SSHTunnelForwarder(
            (ssh_host, ssh_port),
            ssh_pkey=private_key_path,
            ssh_username=ssh_user,
            remote_bind_address=remote_bind_address,
            local_bind_address=local_bind_address
    ) as tunnel:

        conn = hive.connect(
            host='localhost',
            port=tunnel.local_bind_port,
            username='your_hive_username'
        )
        try:
            cursor = conn.cursor()
            yield cursor
        finally:
            conn.close()