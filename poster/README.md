# 차량 안전사고 예방 포스터 — 한 대의 차량, 네 명의 안전관

| 파일 | 내용 |
|---|---|
| `safety-poster-A2-orange.pdf` | 오렌지 바탕 + 검정 (추천) |
| `safety-poster-A2.pdf` | 회색 바탕 + 오렌지 |
| `safety-poster-preview*.png` | 미리보기 |

두 PDF 모두 A2(420×594mm) 한 장, 전부 벡터(이미지 없음), 폰트 임베드. A3 등으로 줄여 출력해도 선명하다.

## 구성
- 제목·역할명·표어: Black Han Sans / 본문: Gothic A1
- 가운데 그림: 중형버스(현대 카운티 계열) 오른쪽 옆면. 실제 버스 사진 위에 벡터를 겹쳐 보며 비율을 맞췄다(`bus.py`).
  운전병(운전석), 선탑자(앞좌석), 안전벨트를 맨 탑승자, 버스 좌후방의 유도병, 버스 바로 뒤의 후방 사각지대.
- 군 버스 도색(흰색 상단 + 짙은 회색 하단)을 따랐다.

## 다시 만들기
```sh
./fetch_fonts.sh      # 문구를 바꿀 때만 필요 (저장소 폰트는 현재 문구에 맞춘 서브셋)
python3 build.py      # poster.html, poster-orange.html 생성
NODE_PATH=$(npm root -g) SRC=poster-orange.html PDF=safety-poster-A2-orange.pdf node render.js
NODE_PATH=$(npm root -g) PDF=safety-poster-A2.pdf node render.js
```
색은 `build.py`의 `PALETTES`, 버스 색은 `bus.py`의 `C`에서 바꾼다.

## 출처·라이선스
- 통계: 군 안전사고 사망자 원인별 현황(2010~2019), 차량사고 34%
- 버스 형태 참고 사진: "Juulchin Tourism Corp 10.JPG", Wikimedia Commons, 퍼블릭 도메인. 사진 자체는 포스터에 들어가지 않는다.
- 폰트: Black Han Sans, Gothic A1. 모두 SIL OFL (`fonts/OFL-*.txt`)
