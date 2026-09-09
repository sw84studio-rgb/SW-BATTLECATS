# SW_BATTLECATS_V093_DELTA_20260909

- 기준: V092 적용본
- 성격: DELTA
- DB: V033 유지 / SQL 없음

## 변경
1. 캐릭터 상세에서 상세용 이미지가 없는 경우 큰 빈 이미지 박스를 쓰지 않고 compact 카드 fallback 레이아웃 사용
2. V092 `catDetailImages`는 optional 데이터로 변경. 해당 파일이 늦게 배포되거나 누락되어도 캐릭터/적/스테이지 전체 부팅은 계속됨
3. V092 상세 이미지가 있는 형태는 기존 큰 상세 영역 유지
4. 적 상세 pixelated fallback, 검색창+모바일/닌텐도 1줄, 적 성 상태 표시는 유지
5. KR 15.5 InstallPack + libnative에서 서버 다운로드 그룹 35개/파일명/MD5를 추출하여 `SERVER_ASSET_INVENTORY_V093.json`에 기록

## 실제 전투 전신 원본 상태
- `.imgcut/.mamodel/.maanim`은 로컬에 있으나 실제 `*_e.png`, `*_c.png` 등 전투 텍스처 바이트는 InstallPack 로컬 팩에 없음
- 서버 그룹 구조와 필요한 pack/list 정보까지는 확인 완료
- 보호된 서버 접근을 우회하거나 제3자 서명 키를 사용하지 않음
- 따라서 V093은 가짜 전신을 만들지 않고, 현재 fallback UI/로딩 구조를 안전하게 정리하는 버전

## 변경 파일
- web/index.html
- web/css/encyclopedia-v093.css
- web/js/data-loader-v093.js
- web/js/encyclopedia-v093.js
- data/runtime-v093/manifest.json
- SERVER_ASSET_INVENTORY_V093.json

## 적용
V092가 적용된 GitHub 작업본에 ZIP 내부 `web`, `data`를 병합/덮어쓰기. `runtime-v092` 이하 삭제 금지.
