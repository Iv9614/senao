# Senao

<!-- GETTING STARTED -->
## Getting Started

### Prerequisites

專案環境變數已經給了範例環境變數檔(template.env)，修改環境變數，並且將檔名重新命(.env)即可使用環境變數檔。以下是修改範例

```sh
PROJECT__NAME="SENAO API"


DATABASE__SERVER=127.0.0.1
DATABASE__PORT=5432
DATABASE__USER=senao_admin
DATABASE__PASSWORD="seano_123"
DATABASE__DATABASE="senao"

```

### Installation

該專案因為會啟動PostgreSQL和API server，因此需仰賴docker compose 啟動DB以及ＡＰＩ server。

API server 可以直接專案內dockerfile build image，可參考Option 1，或是直接拉取dockerhub image(https://hub.docker.com/repository/docker/jesus28713/senao_example/general)，參考Option 2。


### Option 1

1. 啟動docker compose並重新build images
```sh
docker compose up --build
```

### Option 2

可以從dockerhub拉取images， 

1. 修改docker compose 文件
``` sh
  web:
    # build: .
    image: jesus28713/senao_example:1.0.0
    container_name: senao_web
    command: ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]

    ...
```

2. 啟動docker compose 
```sh
docker compose up -d
```


最後前往 [127.0.0.1:8000/docs](127.0.0.1:8000/docs) 應可看到API swagger文件。

## Dockerhub and Github
dockerhub: [https://hub.docker.com/repository/docker/jesus28713/senao_example/general](https://hub.docker.com/repository/docker/jesus28713/senao_example/general)

Github: [https://github.com/Iv9614/senao.git](https://github.com/Iv9614/senao.git)
