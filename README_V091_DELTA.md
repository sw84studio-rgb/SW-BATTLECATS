# SW BATTLECATS V091 DELTA

기준: V090 적용 소스
날짜: 2026-09-09
DB: V033 유지 / SQL 변경 없음

## 이번 수정만
- V090 회귀였던 검색창 + `모바일` + `닌텐도` 1줄 배치를 V089 확정 UI 구조로 복구.
- V090의 적 상세 64x64 썸네일 강제 확대(최대 약 4배)를 제거. 상세에서도 원본보다 확대하지 않음.
- 캐릭터 상세 이미지 규칙은 변경하지 않음.
- V090의 모바일/Nintendo 데이터 분리 로직과 현재 판본 제목 표시는 유지.
- V090의 적 성 ID / 이미지 미확보 상태 표시는 유지.

## 적 상세 원본 조사 결과
- KR 15.5 `ImageDataLocal`에는 적 전투 모델용 `.imgcut`, `.mamodel`, `.maanim` 데이터가 존재.
- `.imgcut`은 `717_e.png` 같은 실제 텍스처를 참조하지만 현재 확보한 InstallPack 로컬 팩에는 해당 적 텍스처 PNG가 없음.
- 따라서 현재 64x64 도감 썸네일을 확대해 고해상도처럼 보이게 하지 않음.
- 실제 서버 텍스처가 확보되기 전까지 적 상세는 원본 썸네일 크기 보호가 정확한 동작.

## 성 이미지
- 새 성 이미지를 만들거나 추측 매핑하지 않음.
- V090에서 확인한 실제 로컬 성 이미지 3종(rc171/179/181)과 미확보 상태 표시를 그대로 유지.

## 변경 파일
- `data/runtime-v091/manifest.json`
- `web/index.html`
- `web/css/encyclopedia-v091.css`
- `web/js/data-loader-v091.js`
- `web/js/encyclopedia-v091.js`

## 적용
현재 V090이 적용된 GitHub 소스 루트에 이 DELTA의 `data`, `web` 폴더를 병합/덮어쓰기.
기존 runtime-v090 및 이전 runtime 폴더 삭제 금지.
