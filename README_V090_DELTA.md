# SW BATTLECATS V090 DELTA

기준: V089 FULL SOURCE (GitHub 배포본)
날짜: 2026-09-09
DB: V033 유지 / SQL 변경 없음

## 변경
- 적 도감 목록 썸네일 크기는 기존 유지. 상세 화면에서 64x64 썸네일도 최대 약 240x240까지 별도 확대 표시.
- 모바일판 / Nintendo판 상단 탭을 명확히 분리하고, 화면 제목에 현재 판본을 표시. 현재 판본과 동일한 M/N 배지는 반복 표시하지 않음.
- Nintendo canonical 데이터 미수입 정책 유지. 모바일 데이터를 Nintendo에 fallback하지 않음.
- KR 15.5 stage CSV 4,957개에서 enemy_base_id를 전수 연결. 실제 성 그림이 없는 경우 상세에서 적 성 영역을 숨기지 않고 `적 성 #ID / 이미지 바이트 미확보`로 표시.
- InstallPack ImageLocal 재검사 결과 rc*.png 39개 중 실제 비-placeholder 그림은 rc171/rc179/rc181 3개뿐. 나머지 36개는 1x1 placeholder이므로 사용하지 않음.

## 적 성 자산 상태
- 전체 스테이지 enemy_base_id 연결: 4,957
- distinct enemy_base_id: 149
- 실제 검증 성 이미지 ID: 3 (171, 179, 181)
- 실제 성 이미지가 표시되는 스테이지: 15
- 이미지 미확보 상태로 표시되는 스테이지: 4,942

## 변경 파일
- `data/runtime-v090/manifest.json`
- `data/runtime-v090/stageVisualAssets.jgz`
- `web/index.html`
- `web/css/encyclopedia-v090.css`
- `web/js/data-loader-v090.js`
- `web/js/encyclopedia-v090.js`

## 적용
V089 소스 루트에 이 DELTA의 `data`, `web`을 병합/덮어쓰기. 기존 runtime-v089 이하 파일 삭제 금지.
