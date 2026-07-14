# ECTOS Frontend

Edge–Cloud Task Offloading Simulator의 핵심 계산 모델을 브라우저에서 체험할 수 있는 최소 기능 프론트엔드입니다.

## 실행

`index.html`을 브라우저에서 열면 바로 실행됩니다. 로컬 서버를 사용할 경우 프로젝트 폴더에서 아래 명령을 실행하세요.

```powershell
python -m http.server 4173
```

그 후 `http://localhost:4173`으로 접속합니다.

## 포함 기능

- 작업 데이터 크기, CPU 연산량, 결과 크기, 마감 시간 설정
- Local / Edge / Cloud 지연 시간·비용·에너지 계산
- Local only, Edge only, Cloud only, 최소 지연, 마감 내 최소 비용 전략
- 추천 노드 및 마감 충족 여부 표시
- 반응형 화면

계산식과 기본 노드 설정은 원본 Python 프로젝트를 기준으로 구현했습니다.
