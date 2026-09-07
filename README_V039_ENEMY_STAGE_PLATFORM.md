# SW BATTLECATS V039 ENEMY / STAGE VISUAL / PLATFORM DELTA

기준 원본: V038 FULL (`SW_BATTLECATS_V038_FULL_SOURCE_NEXT_CHAT_20260907`)

## 이번 DELTA 실제 변경
- 적 585개 이미지/기존 능력 데이터 유지.
- 적 557개는 기존 검증 한국어 스테이지 링크 상태를 명시.
- 적 28개는 원본 spawn이 존재하지만 한국어 스테이지명이 미확정인 상태를 `0개`로 오해하지 않도록 별도 표시.
- 잘못된 스테이지명/내부 native ID를 사용자에게 추측 노출하지 않음.
- 스테이지 이미지 스키마를 `배경` / `적 성`으로 분리하고 VERIFIED 자산만 렌더링하도록 준비.
- 현재 검증된 BCKR 스테이지 이미지는 0개이므로 실제 이미지 영역은 계속 숨김.
- 모바일/Nintendo 판본 메타데이터를 범주별 availability 구조로 확장.
- Nintendo 데이터는 canonical 수입 전까지 계속 잠금. 모바일 데이터를 대체 표시하지 않음.

## SQL
- 변경 없음. DB 스키마/데이터는 수정하지 않았습니다.

## 다음 수집 단계
1. BCKR 메인 스토리(세계/미래/우주) 성·배경 자산을 지역 검증 우선으로 수집.
2. Legend/Special 공통 배경·성은 source ID 교차검증 후 공유 자산으로 연결.
3. Nintendo Switch 캐릭터/스테이지 canonical 표를 별도 namespace로 구축 후 범주별 UI 오픈.
