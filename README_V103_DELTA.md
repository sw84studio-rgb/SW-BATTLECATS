# SW BATTLE CATS V103 DELTA

기준: V101 FULL + V102 DELTA
생성일: 2026-09-11
성격: 같은 채팅용 DELTA

## 변경
- Minecraft 실제 운용 구조를 참고해 냥코 한국판 버전 감지/후보/승인/복원 파이프라인 추가.
- V102 runtime manifest가 요구하지만 V102 DELTA에 빠졌던 `specialCombos.jgz`를 V101의 동일 SHA-256 원본으로 복구.
- 매일 GitHub Actions에서 한국 App Store 공식 metadata를 확인.
- 새 Stable 감지 시 실제 runtime/한국어 보정 데이터를 자동 덮어쓰지 않고 GitHub Issue로 검수 후보만 알림.
- rerun-current / rerun-selected / approve / apply-selected / restore 수동 실행 지원.
- 승인 전 현재 runtime inventory와 Unit 673 `치타` 보호 상태를 감사 보고서에 포함.
- 최대 30개 baseline 이력 보존 및 직전/지정 baseline 복원 지원.

## 보호
- V102 데이터 변경 전체 유지.
- V098 공식 KR 속성 아이콘 유지.
- V100 링크 중복 정리 유지.
- 사용자 확정 한국어명/획득처/적 등장처/뽑기 분류는 자동 덮어쓰기 금지.
- UI/CSS/레이아웃 변경 없음.
- SQL/DB 변경 없음.

## 현재 기준
- 프로젝트 데이터 버전: 15.5.0
- 한국 App Store app id: 848091833
- 감지 소스: Apple iTunes Lookup 공식 metadata endpoint
