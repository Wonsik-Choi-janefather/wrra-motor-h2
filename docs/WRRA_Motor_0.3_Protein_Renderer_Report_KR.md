# WRRA-Motor 0.3 Protein Renderer

## 기능 제약에서 단백질·DNA 후보까지의 실행 가능한 사상

**연구자:** 최원식  
**Core:** WRRA Core 1.0 동결본  
**결과 등급:** H2 `PREDICTED_SEQUENCE_ONLY`; 완전 신생 N1 `FAIL_CLOSED`

## 1. 결과

WRRA-Motor 0.3 Renderer를 실제 코드로 구현하고 실행했다. Renderer는 WRRA-Motor 0.1이 도출한 다섯 기능조건을 입력으로 받는다.

\[
F=\{
\text{energy transduction},\text{polar track binding},
\text{two contacts},\text{present-state gate},\text{coordination}
\}.
\]

현재 버전은 검증된 모터·선로결합 코어를 보존한 채, 두 접촉부의 이량체화와 상태결합을 담당할 coiled-coil gate 후보를 생성한다. 완전 신생 ATPase·선로결합 코어는 생성하지 않는다.

실행 결과는 다음과 같다.

| 항목 | 결과 |
|---|---:|
| 생성·필터 통과 gate | 512개 |
| 보존한 상위 후보 | 5개 |
| 최상위 후보 | H2-b2f820d18e |
| 전체 단백질 | 385 aa |
| 상속된 KIF5B 구간 | 353 aa, 91.69% |
| 새로 설계한 gate | 32 aa, 8.31% |
| DNA CDS | 종결코돈 포함 1,158 nt |
| DNA GC | 57.69% |
| 최장 단일염기 반복 | 4 nt |

## 2. Renderer 구조

\[
R_{0.3}:
F\rightarrow T_{\mathrm{hybrid}}ightarrow
\{g_i\}_{i=1}^{512}\rightarrow
\mathrm{filter}\rightarrow
H2^*\rightarrow\mathrm{DNA}(H2^*).
\]

- \(F\): WRRA 기능계약
- \(T_{\mathrm{hybrid}}\): KIF5B 모터 코어와 설계 gate의 topology
- \(g_i\): heptad 규칙으로 만든 gate 후보
- \(H2^*\): 현재 휴리스틱 점수가 가장 높은 혼성 후보
- \(\mathrm{DNA}(H2^*)\): 사람 세포용 일반 역번역 CDS 후보

## 3. H2 최상위 후보

단백질 topology는 다음과 같다.

\[
\underbrace{\mathrm{KIF5B}_{1-353}}_{\text{INHERITED}}
\Vert
\underbrace{\mathrm{VQNIEQKIANLKEEGAAALQQVEQKIQNLKAE}}_{\text{DESIGNED gate}}.
\]

새 gate는 네 개의 7잔기 반복 사이에 `GAAA` hinge/stutter를 배치한다. heptad의 \(a,d\) 위치에는 소수성 잔기를, \(e,g\) 위치에는 반대 전하쌍을 배치했다.

구조 파일은 동일한 385 aa 사슬 두 개가 평행 이량체를 이루는 topology를 기록한다. 각 사슬은 motor·선로결합 코어 1–328, neck/coupling junction 329–353, 설계 gate 354–385로 나뉜다. 원자 좌표는 구조예측 결과가 없으므로 `OPEN_NOT_PREDICTED`로 남겼다.

최상위 gate의 휴리스틱 지표는 다음과 같다.

| 지표 | 값 |
|---|---:|
| hydrophobic \(a,d\) 충족률 | 1.000 |
| 반대전하 \(e,g\) 충족률 | 1.000 |
| gate 전하밀도 | 0.2813 |
| 9잔기 최대 소수성 비율 | 0.5556 |
| 정규화 조성 엔트로피 | 0.7014 |
| switch proxy | 1.000 |
| 종합 휴리스틱 점수 | 5.0806 |

`switch proxy`는 양쪽 heptad가 성립하고 중앙 hinge가 존재하는지를 나타내는 문법적 대리값이다. 실제 두 구조상태의 자유에너지 차이나 전환속도를 계산한 값이 아니다.

## 4. DNA Renderer

H2 단백질을 일반적인 사람 핵 발현에 맞춘 제한조건으로 역번역했다.

- 목표 GC: 0.58
- 실제 GC: 0.5769
- 종결코돈: `TAA`
- 선택적으로 배제한 부위: EcoRI, HindIII, BamHI, BsaI, BsmBI 인식서열
- 최장 단일염기 반복: 4 nt
- 번역 왕복검사: 정확히 385 aa + stop으로 복원

이 DNA에는 promoter, Kozak sequence, UTR, polyadenylation signal, vector backbone이 없다. 따라서 독립적인 발현 plasmid가 아니라 CDS 후보다. 세포주·벡터·발현량·태그가 정해지기 전에는 `PREDICTED_NOT_SYNTHESIS_READY`다.

## 5. WRRA 소유권 원장

| 정보 | 구간 | 소유권 | 판정 |
|---|---|---|---|
| ATP·미세소관 결합과 motor fold | aa 1–353 | KIF5B P33176 | INHERITED |
| coiled-coil gate 문법 | aa 354–385 | Renderer 0.3 | DESIGNED |
| topology 선택 | 전체 | WRRA-Motor 0.1 조건 + 기존 코어 | DERIVED/HYBRID |
| DNA 코돈 | 1,158 nt | Renderer 0.3 | PREDICTED |
| 실제 접힘 | — | 정보 없음 | OPEN |
| 실제 보행 | — | 정보 없음 | OPEN |

따라서 H2는 “WRRA가 처음부터 만든 모터 단백질”이 아니다. 정확한 표현은 **WRRA가 도출한 기능계약에 따라 기존 운동 코어와 새 gate를 결합한 혼성 단백질 후보**다.

## 6. H2의 위험과 탈락 가능성

H2는 서열문법을 통과했지만 다음 이유로 실험에서 실패할 수 있다.

1. gate가 예상한 평행 이량체 대신 다른 oligomer를 형성할 수 있다.
2. `GAAA` hinge가 스위치가 아니라 단순한 불안정점으로 작동할 수 있다.
3. KIF5B 353번 잔기와 gate의 접합이 neck-linker 장력을 바꿀 수 있다.
4. 이량체는 형성되더라도 두 머리의 ATP 주기가 적절히 어긋나지 않을 수 있다.
5. 과도한 활성으로 세포 내 미세소관 수송을 교란할 수 있다.

따라서 현 단계의 점수는 “잘 걸을 확률”이 아니라 선언한 서열문법과 조성 제약의 충족도다.

## 7. 완전 신생 N1 판정

Renderer는 완전 신생 N1 서열을 출력하지 않았다. 이유는 다음 검증기가 없기 때문이다.

- 신생 ATPase와 선로결합 backbone 생성기
- 두 작동상태와 복합체의 구조예측
- ATP·ADP 상태별 자유에너지 계산
- 미세소관 결합 상태의 mechanochemical cycle simulation
- 발현·단분자 운동 실험

이 상태에서 300–500 aa의 임의 서열을 출력하는 것은 생성은 가능하지만 과학적 설계가 아니다. 따라서 `FAIL_CLOSED_NO_SEQUENCE_EMITTED`로 처리했다.

이 경계는 현재 분야의 실제 난도와도 부합한다. ProteinMPNN과 같은 방법은 주어진 backbone에 맞는 서열 설계에서 강력하지만, 자율적으로 에너지를 변환하며 두 접촉부를 조정하는 새로운 motor cycle까지 자동으로 제공하지는 않는다. 최근 인공 단백질 walker도 DNA 선로와 외부 clocking을 이용했으며, 에너지 변환과 유연한 부품을 결합한 자율 모터는 여전히 핵심 난제로 명시되어 있다.

## 8. 검증 상태

자동검사에서는 다음을 확인했다.

- H1 경계: 353 aa KIF5B + 29 aa GCN4
- H2 길이와 상속구간의 완전일치
- 필수 P-loop motif 보존
- H2 gate가 H1 GCN4와 다른 서열임
- DNA 길이와 번역 왕복 일치
- 목표 GC 범위와 단일염기 반복 제한
- 지정 금지서열 부재
- 완전 신생 N1에 대한 fail-closed 출력
- 고정 seed에서 결과 재현

## 9. 현재 결론

Protein Renderer 0.3은 기능조건에서 후보 단백질과 DNA까지 내려가는 실행 경로를 만들었다. H2는 실제로 합성 가능한 형식의 서열이지만, 구조예측과 동역학 검증을 통과하지 않았으므로 합성 권고 단계는 아니다.

이번 연구의 실질적 성과는 다음 두 가지다.

1. WRRA의 추상 기능계약을 서열 생성과 DNA 역번역까지 연결했다.
2. 생성 가능한 것과 과학적으로 검증된 것을 분리하여, 완전 신생 모터에 대해서는 실패를 숨기지 않고 닫았다.

## 참고문헌

1. Dauparas J et al. *Robust deep learning-based protein sequence design using ProteinMPNN.* Science (2022). PMID: 36108050.
2. Cross JA et al. *A de novo designed coiled coil-based switch regulates the microtubule motor kinesin-1.* Nature Chemical Biology (2024). DOI: 10.1038/s41589-024-01640-2.
3. Nilsson P et al. *Clocked stepping of an artificial protein walker along a DNA track.* Nature Nanotechnology (2026). DOI: 10.1038/s41565-026-02211-3.
4. UniProt P33176, human KIF5B canonical sequence.
