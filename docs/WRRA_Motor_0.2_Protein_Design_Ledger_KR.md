# WRRA-Motor 0.2 단백질 설계 원장

**연구자:** 최원식  
**목적:** WRRA-Motor 0.1의 기능 아키텍처를 단백질과 DNA로 내리기 전에 소유권과 주장 경계를 고정한다.

## 1. 먼저 확인된 경계

WRRA-Motor 0.1은 다음 기능 묶음을 최소 후보로 도출했다.

\[
\{
\text{two contacts},\text{energy drive},\text{polar coupling},
\text{present-state gate},\text{coordination}
\}.
\]

그러나 이 기능 묶음에서 유일한 아미노산 서열이 나오지는 않는다. 기능에서 접힘과 서열로 가는 사상

\[
R_{\mathrm{protein}}:
\text{functional constraints}\longrightarrow
\text{fold ensemble}\longrightarrow
\text{amino-acid sequences}
\]

은 WRRA Core가 아니라 생명 분야 Renderer다. 현재 WRRA에는 이 Renderer가 닫혀 있지 않다. 따라서 현 단계에서 임의의 새 서열을 “WRRA가 도출했다”고 부르는 것은 금지한다.

## 2. 세 후보군

| 후보 | 구조 | 소유권 | 용도 | 현재 판정 |
|---|---|---|---|---|
| P0 | KIF5B(1–560)-형 보행체 | 기존 연구 INPUT | 실험계 양성대조 | 검증된 계열 |
| H1 | KIF5B(1–353)+GCN4 | 전부 기존 모듈 INHERITED | WRRA 최소 아키텍처의 교정 chassis | 서열 확정, 신규성 없음 |
| N1 | 두 접촉부 완전 신생 단백질 | 추후 DESIGNED | WRRA의 진짜 신생 후보 | OPEN |

## 3. H1 교정 chassis

H1은 다음 구조다.

\[
\mathrm{KIF5B}_{1-353}\;\Vert\;\mathrm{GCN4\ zipper}.
\]

- KIF5B 1–353: ATP 결합, 미세소관 결합, neck-linker를 포함하는 기존 인간 키네신-1 구간
- GCN4 zipper: 두 사슬을 이량체로 유지하는 기존 29잔기 leucine-zipper 계열 서열
- 화물·형광 태그: 아직 붙이지 않음

H1의 목적은 새 단백질 발명이 아니다. WRRA가 도출한 기능 모듈이 실제 작동계와 호환되는지 확인하는 교정 기준이다. 유사한 KIF5B(1–353)-GCN4-GFP 구조는 이미 포유류 세포용으로 사용되었고 Addgene #193714로 공개되어 있다.

### H1 잔기 소유권

| 구간 | 길이 | 출처 | 분류 |
|---|---:|---|---|
| KIF5B 1–353 | 353 aa | UniProt P33176 | INHERITED |
| GCN4 dimerization zipper | 29 aa | 공개된 K353-GCN4 구성 | INHERITED |
| 전체 H1 | 382 aa | 기존 두 모듈의 연결 | CALIBRATION |

따라서 H1 DNA를 역번역하더라도 그것은 “WRRA가 만든 신생 유전자”가 아니라 기존 모터의 재구성 발현서열이다.

## 4. N1에 필요한 Protein Renderer 계약

완전 신생 후보 N1의 Renderer는 최소한 다음을 동시에 만족해야 한다.

1. 두 개의 track-binding interface가 같은 극성 선로의 인접 위치에 도달한다.
2. 에너지 운반자 결합 전후의 구조상태가 구별된다.
3. 상태전이가 자유 접촉부의 전방 탐색확률을 높인다.
4. 두 접촉부가 동시에 강결합 또는 동시에 해리되는 경로를 억제한다.
5. 한 접촉부의 점유·변형이 다른 접촉부의 전이율을 바꾼다.
6. 반복 전이 중 접힘이 유지되고 응집하지 않는다.
7. 세포 단백질과 원치 않는 결합을 최소화한다.

이를 목적함수로 쓰면

\[
\min_s\;C(s)=
w_1E_{\mathrm{fold}}+w_2P_{\mathrm{aggregate}}+
w_3P_{\mathrm{off-target}}+w_4N_{\mathrm{residue}}+
w_5P_{\mathrm{dual-detach}}
\]

이고 다음 제약을 둔다.

\[
\Delta x(s)>0,\quad
P_{\mathrm{survive}}(N;s)\ge P_*,\quad
\Delta G_{\mathrm{state\ switch}}\ \text{is finite and reversible}.
\]

이 목적함수의 각 항에는 구조예측·분자동역학·결합에너지 또는 실험값을 공급하는 외부 계산재료가 필요하다.

## 5. N1 서열 생성의 단계적 폐쇄

1. **Topology:** 접촉부·에너지 포켓·coupler의 공간배치를 고정한다.
2. **Backbone ensemble:** 최소 두 작동상태의 backbone을 만든다.
3. **Sequence design:** 두 상태를 모두 허용하되 비작동·응집상태를 불리하게 하는 서열을 찾는다.
4. **Negative design:** 단일 안정구조만 잘 접히는 후보를 제거한다.
5. **Dimer and track test:** 두 사슬과 선로를 포함한 복합체에서 검사한다.
6. **Mechanochemical cycle:** 에너지상태별 전이와 하중반응을 검사한다.
7. **DNA rendering:** 통과한 아미노산 서열만 숙주별 코돈으로 변환한다.

## 6. DNA를 아직 확정하지 않는 이유

DNA는 아미노산 후보와 발현 숙주가 고정된 뒤 만들어야 한다. 같은 단백질도 코돈 선택에 따라 여러 DNA가 가능하며, 프로모터·Kozak·태그·linker·종결신호는 단백질 보행 코어와 별도의 발현 instance다.

H1은 포유류 발현용 DNA로 즉시 역번역할 수 있지만 신규성이 없다. N1은 Protein Renderer를 통과한 아미노산 서열이 아직 없으므로 DNA를 만들면 안 된다. 이 경계는 계산 부족을 숨기지 않는 WRRA fail-closed 판정이다.

## 7. 현 단계 결론

- WRRA-Motor 0.1은 최소 기능 아키텍처를 도출했다.
- 자연의 키네신-1과의 대응은 강하지만, 그 자체로 새 단백질을 만든 것은 아니다.
- H1은 실행 가능한 교정 chassis이며 전체 아미노산 서열을 별도 FASTA로 고정했다.
- 완전 신생 N1과 그 DNA는 아직 OPEN이다.
- 다음 연구의 핵심은 WRRA Core를 고치는 것이 아니라 Protein Renderer를 추가하는 것이다.

## 참고 출처

- UniProt P33176, human KIF5B canonical sequence.
- RCSB PDB 1MKJ, human kinesin motor domain with docked neck linker.
- Burute M et al., Science Advances 8, eabo2343 (2022), DOI: 10.1126/sciadv.abo2343.
- Addgene plasmid #193714, pB80-hsKIF5B(1-353)GCN4-L-GFP.
