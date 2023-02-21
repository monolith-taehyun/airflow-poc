# Airflow PoC

## 목적
배치 스케쥴러로써 `Apache Airflow`의 실제 동작을 확인하고 테스트하고자 함

## 설치
간단한 사용을 위해 Docker를 이용해 로컬에서 구동

https://airflow.apache.org/docs/apache-airflow/stable/howto/docker-compose/index.html


```sh
# DB 초기화 
$ docker compose up airflow-init

# Airflow 시작 
$ docker compose up
```

## 웹 인터페이스로 접근
도커 클러스트가 정상적으로 시작되면 웹 인터페이스에 로그인하여 테스트 할 수 있습니다.
- http://localhost:8080
- 기본 계정 아이디/비밀번호: `airflow` / `airflow`

