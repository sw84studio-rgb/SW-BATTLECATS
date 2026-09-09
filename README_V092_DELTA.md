# SW_BATTLECATS_V092_DELTA_20260909

- 기준: V091 적용본
- 버전: V092
- 성격: DELTA (변경 파일 + 신규 상세 이미지 자산만 포함)

## 이번 수정 핵심
1. 캐릭터 상세에서 KR 15.5 `UnitLocal/udi*.png` 가 존재하는 형태는 **더 큰 상세용 이미지**로 교체
2. 적 상세는 고해상도 원본 미확보 상태이므로 **64×64 원본을 선명(pixelated) 확대 fallback**으로 표시
3. 성(적 성) 관련 V090/V091 상태 표시는 유지
4. 검색창 + 모바일/닌텐도 한 줄 UI는 유지

## 상세 이미지 적용 범위
- 캐릭터 상세 대체 연결: 162개 형태
- 출처: KR 15.5 `UnitLocal/udi###_[c|f|s|u].png`
- 처리: 투명 여백 자동 crop 후 상세 전용 자산으로 저장
- 제한: true full-body 전투 텍스처가 아니라 **클라이언트 로컬 UnitLocal 계열 상세 카드/텍스처**입니다.
- 나머지 캐릭터 형태는 기존 카드 이미지 fallback 유지

## 변경 파일
- `web/index.html`
- `web/js/data-loader-v092.js`
- `web/js/encyclopedia-v092.js`
- `web/css/encyclopedia-v092.css`
- `data/runtime-v092/manifest.json`
- `data/runtime-v092/catDetailImages.jgz`
- `assets/mobile/kr/cats/detail/**` (신규 162개 PNG)

## 적용 방법
현재 GitHub 작업본이 **V091 적용본**이라면, 이 ZIP의 `web`, `data`, `assets` 폴더를 병합/덮어쓰기 후 커밋/푸시하면 됩니다.

## SQL
- 없음 (DB V033 그대로)
