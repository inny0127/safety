# 차량 안전사고 예방 포스터 — 한 대의 차량, 네 명의 안전관

| 파일 | 내용 |
|---|---|
| `safety-poster-A2.pdf` | 회색 바탕 + 시그널 오렌지 |
| `safety-poster-A2-orange.pdf` | 오렌지 바탕 + 검정 |
| `safety-poster-preview*.png` | 미리보기 |

두 PDF 모두 A2(420×594mm) 한 장, 전부 벡터(이미지 없음), 폰트 임베드. A3 등으로 줄여 출력해도 선명하다.

## 구성
- 제목·역할명·표어: Black Han Sans / 본문: Gothic A1
- 가운데 그림은 2½톤 카고트럭이 후진할 때의 평면도. 실제 치수(m)로 그렸다.
  운전석(좌), 선탑석(우), 적재함 벤치, 좌측 사이드미러로 이어지는 시야선, 후방 사각지대, 좌후방 유도 위치.

## 다시 만들기
```sh
./fetch_fonts.sh      # 문구를 바꿀 때만 필요 (저장소 폰트는 현재 문구에 맞춘 서브셋)
python3 build.py      # poster.html, poster-orange.html 생성
NODE_PATH=$(npm root -g) PDF=safety-poster-A2.pdf node render.js
NODE_PATH=$(npm root -g) SRC=poster-orange.html PDF=safety-poster-A2-orange.pdf node render.js
```
색은 `build.py`의 `PALETTES`에서 바꾼다.

## 출처·라이선스
- 통계: 군 안전사고 사망자 원인별 현황(2010~2019), 차량사고 34%
- 폰트: Black Han Sans, Gothic A1. 모두 SIL OFL (`fonts/OFL-*.txt`)
