# SW BATTLECATS V121 DELTA

- 기준: 사용자가 업로드한 GitHub 최신 `SW-BATTLECATS-main (1).zip` (V120 실제 로딩 소스)
- 목적: 모바일/Nintendo 스테이지 출현 적 원본 이미지 표시 유지 + Nintendo 상세/권장 캐릭터 표시 보강

## 변경
- Nintendo 스테이지 출현 적을 런타임 이름 재검색 대신 검증된 `enemy ID` 직접 참조로 연결
- Nintendo 권장 캐릭터를 텍스트 버튼에서 기존 원본 이미지 + 한국어 이름 카드로 표시
- Nintendo 상세에서 기존 검증된 통솔력/성 체력/보상/해금/보스/대응/공략 정보는 그대로 표시
- 확인되지 않은 Nintendo 값은 빈칸 유지
- 모바일 스테이지 출현 적의 기존 enemy ID → 원본 이미지 표시 로직 유지
- 기존 UI 색상/글자 크기/메뉴/레이아웃/CSS 변경 없음
- 모바일 캐릭터/적/스테이지 원본 데이터 변경 없음

## 정적 검증
- JS 문법 검사: PASS
- Nintendo 스테이지 목록: 315행, 파생 EX 포함 표시 총계 316 유지
- Nintendo 직접 enemy ref: 333건 / 100개 스테이지 / 57종 / 이미지 누락 0
- Nintendo 권장 캐릭터: 26건 / 18종 / Nintendo scope 누락 0 / 이미지 누락 0
- 모바일 스테이지 enemy ref 고유 ID: 557종 / 이미지 누락 0
- visualAssets가 가리키는 로컬 이미지 파일 누락: 0
- runtime manifest의 Nintendo guide gzip/hash/size 검증: PASS
- 기존 Nintendo guide 값은 enemy_refs 추가 외 변경 없음

## 미검증
- 실행 환경의 Chromium이 localhost 및 file URL을 조직 정책으로 차단하여 실제 PC/모바일/태블릿 브라우저 렌더링은 미검증
- 실제 배포 화면은 사용자 확인 필요
