# 차량 안전사고 예방 포스터 — 한 대의 차량, 네 명의 안전관

- `safety-poster-A2.pdf` — 출력용 (A2 420×594mm, 전부 벡터, A3 등으로 축소 출력해도 선명)
- `safety-poster-preview.png` — 미리보기

## 다시 만들기

문구·색·수칙은 `build.py` 상단(`ROLES`, `CAUSES`, 팔레트)과 `page()`에서 고친다.

```sh
python3 build.py                                   # poster.html 생성
NODE_PATH=$(npm root -g) PDF=safety-poster-A2.pdf node render.js
NODE_PATH=$(npm root -g) PNG=preview.png SCALE=0.5 node render.js
```

Playwright(Chromium)가 필요하다.

## 출처·라이선스

- 통계: 2010~2019년 군 안전사고 사망자 원인별 현황 (차량 34%, 추락·충격 15%, 항공·함정 11%, 익사 11%, 총기 3%)
- 폰트: Pretendard, Big Shoulders Stencil Display, Barlow Condensed — SIL OFL (`fonts/OFL-*.txt`)
- 아이콘: Tabler Icons — MIT (`icons/LICENSE-tabler.txt`)
