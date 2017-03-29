## Github Flow

기능별로 브랜치를 만들어 작업합니다.

아래의 설명은 `user-api` 브랜치 기준으로 작성했습니다.
작업 시, 브랜치 이름을 꼭 확인해주세요.

```shell
$ git checkout -b user-api origin/develop


# 커밋의 생활
$ git add -A
$ git commit -m "message"

$ git pull --rebase
$ git push origin user-api
```

pull reqeust를 보낸다.
이 때, **develop** > user-api 로 설정.

풀리퀘를 받는 사람은 반드시 **Rebase and Merge**로 받는다.


하나의 기능 개발이 완료되면 브랜치를 삭제합니다.
