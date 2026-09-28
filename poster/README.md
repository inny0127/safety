# 차량 안전사고 예방 포스터 — 한 대의 차량, 네 명의 안전관

- `safety-poster-A2.pdf`: 출력용 파일 (A2 420×594mm, 전부 벡터, 폰트 임베드. A3 등으로 줄여 출력해도 선명함)
- `safety-poster-preview.png`: 미리보기

## 구성
- 종이·먹·별색(빨강) 세 가지 색만 씀
- 헤드라인·본문: Noto Serif KR / 수칙·도해 라벨: IBM Plex Sans KR / 번호: IBM Plex Mono
- 그림 1은 2½톤 카고트럭 후진 상황의 평면 도해. 실제 치수(m)로 그린 뒤 축척 112px/m로 옮김.
  운전석(좌), 선탑석(우), 적재함 벤치, 좌측 사이드미러 시야선, 후방 사각지대, 좌후방 유도 위치를 표시함

## 다시 만들기
```sh
./fetch_fonts.sh      # 문구를 바꿀 때만 필요 (저장소의 폰트는 현재 문구에 맞춘 서브셋)
python3 build.py      # poster.html 생성
NODE_PATH=$(npm root -g) PDF=safety-poster-A2.pdf PNG=safety-poster-preview.png SCALE=1 node render.js
```

## 출처·라이선스
- 통계: 군 안전사고 사망자 원인별 현황(2010~2019). 차량 34%, 추락·충격 15%, 항공·함정 11%, 익사 11%, 총기 3%
- 1-3의 휴식 기준(2시간마다 15분)은 민간 권고이므로 부대 운행 규정을 확인할 것
- 폰트: Noto Serif KR, IBM Plex Sans KR, IBM Plex Mono. 모두 SIL OFL (`fonts/OFL-*.txt`)
