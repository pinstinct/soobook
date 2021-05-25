# SooBook Project

자기가 읽었거나 읽고 싶은 책을 보관하고 관리할 수 있는 '개인 도서 관리 서비스'입니다.

원하는 책을 검색하여 내 책장에 추가할 수 있습니다.
추가한 책에 한줄 평가, 별점 평가, 책속 글귀를 입력할 수 있습니다.


## [구현 기능](https://pinstinct.github.io/web/2017/04/26/soobook-detail/)

### 1. 회원관리 기능
- 가입
- 로그인 : rest_framework.authtoken
- 로그아웃 : rest_framework.authtoken

### 2. 책 검색 기능
- 전체 책 검색 : Google Book API, Daum Book Search API, requests, django_celery_results, django_celery_beat, django_filters
- 내 책 검색 : django_filters

### 3. 책 평가 기능
#### 내 책
- 추가
- 삭제
- 리스트
- 디테일

#### 한줄 평가
- 추가 및 업데이트
- 삭제

#### 별점 평가
- 추가 및 업데이트
- 리스트

#### 책속 글귀
- 추가
- 업데이트
- 삭제

## [테스트 코드](https://pinstinct.github.io/web/2017/04/26/soobook-testcode/)




# Github Flow

기능별로 브랜치를 만들어 작업합니다.

아래의 설명은 `user-api` 브랜치 기준으로 작성했습니다.
작업 시, 브랜치 이름을 꼭 확인해주세요.

```shell
$ git checkout develop
$ git pull
$ git checkout -b user-api develop

# 작업 후
$ git add -A
$ git commit -m "message"

$ git push origin user-api

# 팀원과 확인 후 브랜치를 병합
$ git checkout develop
$ git merge user-api
# (충돌이 일어날 경우, 해결)
$ git push origin develop
```
