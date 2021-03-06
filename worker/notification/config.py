from pathlib import Path

import deserialize

from common.configutil import get_config


class Config:
    class NotificationWorker:
        @deserialize.default('port', '3306')
        class MySQL:
            host: str
            port: str
            user: str
            password: str
            database: str

        @deserialize.default('port', '6379')
        class Redis:
            class Database:
                database: str

            host: str
            port: str
            password: str

            notification_queue: Database

        mysql: MySQL
        pool_size: str
        redis: Redis

    notification_worker: NotificationWorker


config_path = f'{Path(__file__).resolve().parent}/config'

config: Config = deserialize.deserialize(
    Config, get_config(config_path)
)
