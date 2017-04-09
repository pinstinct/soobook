## Github Flow

기능별로 브랜치를 만들어 작업합니다.

아래의 설명은 `user-api` 브랜치 기준으로 작성했습니다.
작업 시, 브랜치 이름을 꼭 확인해주세요.

```shell
$ git checkout develop
$ git pull
$ git checkout -b user-api develop

# 작업 후,
# 커밋의 생활
$ git add -A
$ git commit -m "message"

$ git push origin user-api
```

