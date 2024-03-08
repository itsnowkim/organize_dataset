# 네이밍 컨벤션 변경하기
1. `endoscope_naming_convention.py` 에서 해당 스크립트를 실행할 경로 설정하기
2. `endoscope_naming_convention.py` 실행하기

# 데이터 다운로드하기
1. AWS Athena 에서 다운로드할 데이터 쿼리하기
2. 쿼리 결과 csv 파일 key 값 알아오기
3. AWS credential 세팅하기
```bash
export AWS_ACCESS_KEY_ID=your_access_key_id_here
export AWS_SECRET_ACCESS_KEY=your_secret_access_key_here
export AWS_DEFAULT_REGION=your_default_region_here
```
환경 변수로 세팅해도 되고, aws cli 로 config 한 후 실행해도 무관.
4. `download.py` 의 arg 로 key 값 넘겨주고, 실행하기
