# SW BATTLECATS V095 DELTA

기준 원본: 현재 GitHub FULL V093 (`SW-BATTLECATS-main (1).zip`)
생성일: 2026-09-10
성격: 같은 채팅용 DELTA

## 변경 요약
- V094의 빨강 적 일본어 아이콘 제거 및 상세 이미지 경로 표시 수정 병합
- 기존 특수 냥콤보 386행을 KR 15.5 검증 현행 냥콤보 255개로 교체
- 기존 특수 냥콤보의 placeholder 표시 162행 제거
- 냥콤보 식별에 series+combo_id 기반 combo_key 추가
- runtime V095 manifest 생성 및 버전 메타 정합성 수정
- 기존 cats/enemies/stages 및 과거 evidence 원본은 변경하지 않음

## SQL
변경 없음.

## 적용
현재 GitHub FULL 루트에 이 DELTA의 파일을 경로 그대로 덮어쓰기. 과거 runtime 폴더는 삭제하지 말 것.
