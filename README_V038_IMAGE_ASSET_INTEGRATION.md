# SW BATTLECATS V038 IMAGE ASSET INTEGRATION DELTA

기준: V037 upload-ready static + V038 FIXED5 collected assets

## 실제 변경
- 캐릭터 실제 distinct visual: 1973 / 1973
- raw 비독립/중복 form 숨김: 363
- 공유 알 이미지로 연결한 form: 52 (파일 중복 없이 10개 공통 자산)
- 적 실제 이미지: 585 / 585
- 특수 핵심 실제 아이콘: 67개
- 스테이지 실제 이미지가 없는 경우 빈 이미지 박스 제거
- 상단 검색 + 모바일 + 닌텐도 한 줄 배치
- 모든 런타임 이미지는 local-only. 원격 hotlink 사용 안 함.

## 아직 미완료
- Nintendo 공통/전용 판정 데이터
- 한국어 텍스트가 들어간 뽑기/이벤트 배너
- 스테이지/성 대표 이미지
- 일본어/번체 문자가 포함된 속성/특능 아이콘의 한국판 검증

## 적용
V037 GitHub 배포 루트에 이 DELTA의 파일 구조 그대로 덮어쓰세요. 기존 runtime-v037는 삭제하지 마세요. V038 manifest가 변경 없는 데이터는 runtime-v037를 참조합니다.

SQL 변경 없음.

## 검증 결과
- runtime manifest 16개 참조 파일 존재/압축 해제/JSON 파싱/SHA 검증: PASS
- 캐릭터 사용자 표시 1,952개: 로컬 이미지 1,952/1,952, placeholder 0: PASS
- 캐릭터 distinct visual 원본 기준 1,973/1,973 확보: PASS
- 적 585개: 로컬 이미지 585/585, placeholder 0: PASS
- 특수 아이템/재화 253개 중 검증된 공통 아이콘 67개 표시: PASS
- 실제 asset 경로 참조 누락 0: PASS
- 내부 숫자 raw 라벨(예: 730_1, 771-1) 사용자 목록 노출 0: PASS
- M 배지: 현재 검증된 모바일 데이터에 표시: PASS
- N 배지: Nintendo 원본 대조 전이라 생성하지 않음
- 상단 검색/모바일/닌텐도 1줄 3열: Chromium 390px 런타임 검사 PASS
- 스테이지 이미지 미확보 시 빈 placeholder 영역 제거: PASS
- JavaScript node --check 3개: PASS
- Headless Chromium 런타임 콘솔/page error: 0
- GitHub Pages 실제 배포/실기기 확인: 미검증

## 데이터 보존/표시 규칙
- raw cat 2,336행은 호환성을 위해 보존합니다.
- 비독립/중복 raw form 363개는 목록에서 숨기고 내부 참조에는 이전 실제 visual alias를 유지합니다.
- 숫자/구분자 형태의 내부 라벨 22개 중 비독립과 겹치지 않는 21개는 한국어 이름 검증 전 목록에서 추가로 숨깁니다.
- 따라서 현재 사용자 표시 캐릭터 형태는 1,952개이며, 별개 visual 자산 자체는 1,973/1,973 확보 상태입니다.
