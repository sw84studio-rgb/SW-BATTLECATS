# SW BATTLECATS V134 DELTA

- 기준: V132 FULL + V133 DELTA 적용 상태
- 날짜: 2026-09-15
- 목적: Nintendo 한국어판 특수 스테이지의 출현 적 종류, 확인 가능한 출현 수·조건, 적도감 역연결을 추가 보강

## 주요 변경
- Nintendo 특수 스테이지 59개를 근거 수준에 따라 재검증
  - FULL 24개: Switch 전용 자료에서 출현 적 종류 전체 확인
  - PARTIAL 25개: 확인된 적/보스/출현 조건만 표시
  - UNVERIFIED 10개: 근거 없는 모바일 데이터 대입 없이 미확인 유지
- 월요일·화요일·금요일 요일 스테이지, 메탈 티켓 스테이지, 개다래 다수 스테이지의 출현 적 구성 연결
- 광란/대광란 스테이지의 확인된 보스 및 일부 출현 적 연결
- 출현 수·조건이 확인된 24개 스테이지에 `출현 수·조건` 표시 추가
  - 예: 대갈이군 1마리, 광란의 도마뱀 3마리, 광란의 거신 1마리, 샤이 보어 2마리, 블랙 맴매 2마리 등
- 각성의 고양이 무트 스테이지의 보스 및 에이리언 계열 정보 역연결
- Nintendo 적도감 허용 범위 95종 → 115종
  - 특수 스테이지에서 실제 Nintendo 출현 근거가 확인된 적만 추가
- Nintendo 적도감 `등장 스테이지`는 계속 Nintendo stage guide 역연결만 사용하며 모바일 등장 스테이지는 섞지 않음
- V133의 Nintendo 능력/특성 필터 및 V129/V130 캐릭터 상세 이동 수정 유지

## 현재 검증 상태
- 세계편: 48/48 FULL
- 미래편: 48/48 FULL
- 우주편: 43/48 FULL, 5/48 PARTIAL
- 레전드: 24/112 FULL, 73/112 PARTIAL, 15/112 UNVERIFIED
- 특수: 24/59 FULL, 25/59 PARTIAL, 10/59 UNVERIFIED

## 특수 스테이지 미확인 10개
- 척척박사 초급 / 중급 / 상급
- 저격의 명수 초급 / 중급 / 상급
- 경험은 꿀맛 초급 / 중급 / 상급 / 초상급

위 10개는 Switch 전용 전체 적 근거를 확보하지 못해 모바일판 구성으로 임의 보완하지 않았습니다.

## 주요 교차검증 자료
- Switch 스페셜/요일/광란 출현 적: https://nekoyakata.net/hutaridenyanko-special/
- Switch 개다래 출현 적: https://nekoyakata.net/hutaridenyanko-special-stage/
- Switch 개다래 추가 교차검증: https://w.atwiki.jp/raitoni2009/pages/45.html
- Switch 일일·게릴라: https://ds-can.com/nyanko/sub/sp_all.html
- Switch 레어티켓 게릴라: https://ds-can.com/nyanko/other/tike.html
- Switch 광란/대광란: https://ds-can.com/nyanko/sub/kyoran.html
- Switch 각성의 고양이 무트: https://ds-can.com/nyanko/sub/legend_nekomu.html

## 검증
- `encyclopedia-v134.js` Node 문법 검사 PASS
- Nintendo stage guide 315개 유지
- 각 스테이지 `enemy_type_count`와 고유 enemy ref 수 일치 PASS
- Nintendo stage guide enemy ref 중 Nintendo 적도감 scope 외 참조 0건
- Nintendo 적도감 범위 115종 확인
- 모바일 `cats.jgz`, `stages.jgz`, `hierarchy.jgz` 변경 없음
- V133 기준 변경 파일 6개 확인
- 기존 `openEntry` 상세 이동 함수 유지
- 로컬 HTTP에서 index / V134 JS / manifest / Nintendo stage guide 로드 PASS

## 미검증 / 남은 항목
- 우주편 PARTIAL 5개 전체 적 구성
- 레전드 PARTIAL 73개 / UNVERIFIED 15개 전체 적 구성
- 특수 UNVERIFIED 10개 전체 적 구성
- 특수 PARTIAL 스테이지의 전체 출현 순서·총 마릿수·반복 간격
- Nintendo 전 캐릭터/적의 세부 전투 수치를 한국어판 원본으로 1:1 전수검증한 상태는 아님
- 실제 배포 PC/모바일/태블릿 및 사용자 실기 확인은 미실시
