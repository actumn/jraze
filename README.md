# Jraze
- ***Installable push sending service*** that can control push targets with their properties by notification's conditions

## Pre-requisites
- docker >= 19.03.8
- docker-compose >= 1.25.5
- python >= 3.7

## Quick start (on local)
```
------- Select FCM API version
| $ export PUSH_WORKER__FCM__LEGACY__SERVER_KEY={..fcm server key..}
| $ export PUSH_WORKER__FCM__CLIENT=legacy
-------
| $ export PUSH_WORKER__FCM__V1__KEY_FILE_NAME={..fcm service account key path..}
| $ export PUSH_WORKER__FCM__V1__PROJECT_ID={..fcm project id..}
| $ export PUSH_WORKER__FCM__CLIENT=v1
-------
$ docker-compose -f local-docker-compose.yml up -d
```

## Worker

### Push worker
#### Run worker
```
$ export ENV=dev
------- Select FCM API version
| $ export PUSH_WORKER__FCM__LEGACY__SERVER_KEY={..fcm server key..}
| $ export PUSH_WORKER__FCM__CLIENT=legacy
-------
| $ export PUSH_WORKER__FCM__V1__KEY_FILE_NAME={..fcm service account key path..}
| $ export PUSH_WORKER__FCM__V1__PROJECT_ID={..fcm project id..}
| $ export PUSH_WORKER__FCM__CLIENT=v1
-------
$ export PUSH_WORKER__REDIS__HOST={...}
$ export PUSH_WORKER__REDIS__PASSWORD={...}
$ python3 -m worker.push.fcm
```

#### Run worker with docker-compose in local
```
$ export PUSH_WORKER__FIREBASE__SERVER_KEY={..fcm server key..}
$ docker-compose -f local-docker-compose.yml up -d push-worker
```

### Result worker
#### Run worker
```
$ export ENV=dev
$ export RESULT_WORKER__REDIS__HOST={...}
$ export RESULT_WORKER__REDIS__PASSWORD={...}
$ export RESULT_WORKER__MYSQL__HOST={...}
$ export RESULT_WORKER__MYSQL__USER={...}
$ export RESULT_WORKER__MYSQL__PASSWORD={...}
$ python3 -m worker.result
```

#### Run worker with docker-compose in local
```
$ docker-compose -f local-docker-compose.yml up -d result-worker
```

### Notification worker
#### Run worker
```
$ export ENV=dev
$ export NOTIFICATION_WORKER__REDIS__HOST={...}
$ export NOTIFICATION_WORKER__REDIS__PASSWORD={...}
$ export NOTIFICATION_WORKER__MYSQL__HOST={...}
$ export NOTIFICATION_WORKER__MYSQL__USER={...}
$ export NOTIFICATION_WORKER__MYSQL__PASSWORD={...}
$ python3 -m worker.notification
```

#### Run worker with docker-compose in local
```
$ docker-compose -f local-docker-compose.yml up -d notification-worker
```

## API server

### Run server
```
$ export ENV=dev
$ export API_SERVER__MYSQL__HOST={...}
$ export API_SERVER__MYSQL__USER={...}
$ export API_SERVER__MYSQL__PASSWORD={...}
$ export API_SERVER__REDIS__HOST={...}
$ export API_SERVER__REDIS__PASSWORD={...}
$ python3 -m apiserver
```

### Run worker with docker-compose in local
```
$ docker-compose -f local-docker-compose.yml up -d api-server
```


## Project structure
```
/
  /apiserver
  /worker
    /push
      /fcm
    /result
    /notification
```

- API server
  ---
  - Endpoint for client can attach through REST API
  - Take roles about register device/notification
  - Also it shows device's event for notification
  - Publish job for 'Notification worker'

- Notification worker
  ---
  - Find devices comfort notification's condition and publish job for 'Push worker'

- Push worker
  ---
  - Client for send push message to each send platform like: FCM, APNs(in planning)
  - Publish job for 'Result worker' to update notification sent result (success / failed)

- Result worker
  ---
  - Client for update notifications' sent result

### Sequence
```
[API server] -> [Notification worker] -> [Push worker] -> [Result worker]
```
