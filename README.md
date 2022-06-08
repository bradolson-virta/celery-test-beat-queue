This document is a small proof-of-concept/sanity check that celery beat/workers are operating with celery 5.0.5, redis as a broker, and rabbit as a message queue.

#### Setup

Requires `redis` and `rabbitmq`

```
brew install rabbitmq
brew install redis
```

Install the required python packages:
```
pip install requirements.txt
```

Start the required broker/mq:
```
rabbitmq-server
redis-server
```

Start the celery beat and worker:
```
celery --app celery_test.celery beat -s /tmp/celerybeat2-schedule --loglevel=INFO
celery --app celery_test.celery worker --loglevel=INFO -E
```

Expected output in worker terminal:
```
[2022-06-08 15:07:09,991: INFO/ForkPoolWorker-8] Task initial_task[938848cc-6c99-4e4e-b5f4-e159b1a571b8] succeeded in 0.003216833999999835s: None
[2022-06-08 15:07:09,992: INFO/ForkPoolWorker-1] subsequent_task[6949e4f2-3cd5-49c5-a06d-c4c2e9949bad]: executing subsequent task
[2022-06-08 15:07:09,994: INFO/ForkPoolWorker-1] Task subsequent_task[6949e4f2-3cd5-49c5-a06d-c4c2e9949bad] succeeded in 0.0016594699999998852s: None
[2022-06-08 15:07:19,987: INFO/MainProcess] Received task: initial_task[040435db-022a-4b5f-8c29-ba94cf882c31]
[2022-06-08 15:07:19,988: INFO/ForkPoolWorker-8] initial_task[040435db-022a-4b5f-8c29-ba94cf882c31]: creating group
[2022-06-08 15:07:19,989: INFO/ForkPoolWorker-8] initial_task[040435db-022a-4b5f-8c29-ba94cf882c31]: group created, applying async
[2022-06-08 15:07:19,991: INFO/MainProcess] Received task: subsequent_task[f3e469b5-a8b2-4400-92b9-bc822492f73b]
[2022-06-08 15:07:19,991: INFO/ForkPoolWorker-8] Task initial_task[040435db-022a-4b5f-8c29-ba94cf882c31] succeeded in 0.0028956899999954544s: None
[2022-06-08 15:07:19,992: INFO/ForkPoolWorker-1] subsequent_task[f3e469b5-a8b2-4400-92b9-bc822492f73b]: executing subsequent task
[2022-06-08 15:07:19,993: INFO/ForkPoolWorker-1] Task subsequent_task[f3e469b5-a8b2-4400-92b9-bc822492f73b] succeeded in 0.0013096069999960491s: None
```
