import asyncio
import json
import multiprocessing

import aioredis
import deserialize

from common.logger.logger import get_logger
from common.structure.job import Job
from worker.config import config
from worker.fcm.messaging import FCM

logger = get_logger(__name__)


class Replica:
    REDIS_MQ_TOPIC = 'FCM_PUSH_QUEUE'
    REDIS_TIMEOUT = 0  # Infinite

    def __init__(self):
        self.fcm = FCM(config.push_worker.firebase.server_key)
        self.redis_host = config.push_worker.redis.host
        self.redis_port = config.push_worker.redis.port
        self.redis_password = config.push_worker.redis.password

    def run(self, pid):  # multiprocess child
        logger.debug(f'Worker {pid} up')
        loop = asyncio.get_event_loop()
        loop.run_until_complete(self.job())

    async def process_job(self, job_json):  # real worker if job published
        try:
            logger.debug(job_json)
            job: Job = deserialize.deserialize(
                Job, json.loads(job_json)
            )

            sent, failed = await self.fcm.send_notification(
                targets=job.registration_tokens,
                title=job.title,
                body=job.body,
                image=job.image,
            )
            logger.info(f'sent: {sent}, failed: {failed}')
        except Exception:
            logger.exception(f'Fatal Error! {job_json}')

    async def job(self):  # real working job
        redis_conn = await aioredis.create_connection(
            f'redis://{self.redis_host}:{self.redis_port}',
            password=self.redis_password,
            db=int(config.push_worker.redis.notification_queue.database),
        )
        while True:
            _, job_json = await redis_conn.execute(
                'blpop',
                self.REDIS_MQ_TOPIC,
                self.REDIS_TIMEOUT,
            )
            logger.debug(multiprocessing.current_process())

            if not job_json:
                continue

            logger.info('new task')
            asyncio.create_task(self.process_job(job_json))
