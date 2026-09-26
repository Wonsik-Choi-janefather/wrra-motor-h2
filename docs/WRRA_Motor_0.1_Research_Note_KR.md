# WRRA-Motor 0.1

## WRRA Core 1.0으로 도출한 최소 세포내 보행 구조

**연구자:** 최원식  
**상태:** 구조 수준 연구노트 — 단백질 서열과 DNA는 아직 OPEN  
**Core:** WRRA Core 1.0 동결본. Core 규칙은 변경하지 않으며 본 연구는 WRRA-Bio의 Domain Profile이다.

## 1. 연구 질문

세포질의 열잡음 속에서 극성을 가진 선로를 따라 유한한 화학에너지를 소비하며 반복적으로 전진하는 물리적 단백질에는 어떤 최소 구조가 필요한가?

이 단계에서는 키네신·다이네인·미오신의 서열과 자연 모터에 맞춘 속도상수를 입력하지 않았다. 먼저 WRRA의 생존 계약과 최소계산 원칙으로 기능 구조를 도출한 뒤 자연 모터와 사후 대조했다.

## 2. WRRA Domain Profile

실행계보는 다음과 같다.

\[
\mathrm{SOURCE}\rightarrow\mathrm{RELATION/LAW}\rightarrow
\mathrm{STATE/RESIDUE}\rightarrow\mathrm{BOUNDARY}\rightarrow
\mathrm{COMMON\ CARRIER}\rightarrow\mathrm{UPDATE}\rightarrow
\mathrm{RENDERER}\rightarrow\mathrm{PHENOTYPE}\rightarrow
\mathrm{OBSERVABLE/RECORD/LEDGER}.
\]

| WRRA 항목 | 보행 문제에서의 소유자 |
|---|---|
| SOURCE | 외부 화학 자유에너지 |
| RELATION/LAW | 국소 상세균형, 결합·해리, 열확산, 극성 선로 |
| STATE/RESIDUE | 현재의 결합상태, 에너지 운반자 점유, 탄성·구조 변형 |
| BOUNDARY | 세포질, 열잡음, 유한 하중, 선로의 격자와 극성 |
| COMMON CARRIER | 단백질 구조변화 |
| UPDATE | 에너지 입력에 결합된 상태전이 |
| RENDERER | 결합면의 기하와 구조적 결합 규칙 |
| PHENOTYPE | 선로 위 순방향 변위 |
| OBSERVABLE | 변위, 이탈률, 연속 이동거리, 에너지 비용 |

과거 이력은 별도 기억장치에 저장하지 않는다. 필요한 기록은 현재의 뉴클레오타이드 점유, 결합상태 또는 탄성변형으로 물리적으로 구현되어야 한다. 이는 WRRA Core 1.0의 fixed-present 조건을 따른다.

## 3. 최소 생존 계약

후보 구조 \(M\)의 엄격한 보행 계약을 다음처럼 정의했다.

\[
V_{\mathrm{strict}}(M)=1
\]

이 되기 위한 조건은 다음 네 가지다.

1. 한 주기의 기대변위가 양수다.
2. 이산 선로의 접촉 위치를 교환하는 동안 적어도 하나의 접촉부는 결합되어 있다.
3. 에너지 입력과 구조 복잡도가 유한하다.
4. 현재상태만으로 다음 결합·해리 순서를 결정할 수 있다.

순간적인 완전 이탈 후 재결합을 허용하는 경우는 별도의 완화 계약 \(V_{\mathrm{relaxed}}\)로 분리한다.

## 4. 방향성이 생기는 최소조건

정방향과 역방향 전이율의 비를 국소 상세균형 형태로 쓰면

\[
\frac{k_+}{k_-}=e^{\mathcal A},\qquad
\mathcal A=\frac{\Delta\mu-W_{\mathrm{load}}}{k_{\mathrm B}T}
\]

이다. 한 주기에 \(+d\) 또는 \(-d\)로 이동하는 최소 두 결과 모델에서는

\[
p_+=\frac{1}{1+e^{-\mathcal A}},\qquad
\langle\Delta x\rangle=d\tanh\left(\frac{\mathcal A}{2}\right).
\]

따라서 선언한 모델 안에서는 다음이 성립한다.

- 에너지 구동이 없거나 공간·구조 비대칭과 결합되지 않으면 \(\mathcal A=0\)이고 순이동은 0이다.
- 화학 입력보다 하중 일이 커지면 순이동은 멈추거나 역전된다.
- 에너지 입력만 있고 극성 결합이 없으면 스칼라 에너지가 방향을 선택하지 못한다.

## 5. 접촉부 수에 대한 조건부 최소성

이산 선로에서 단 하나의 점 접촉부만 허용하고 접촉 위치가 \(i\)에서 \(i+1\)로 바뀌어야 한다면, 이동 과정 중 접촉이 0개인 구간이 반드시 생긴다. 따라서 1접촉부 구조는 엄격한 항상-결합 계약을 만족할 수 없다.

2접촉부 구조에서는 한 접촉부가 선로에 남아 있는 동안 다른 접촉부가 다음 위치를 탐색할 수 있다. 그러므로 엄격한 계약 아래에서 2는 가능한 최소 접촉부 수다.

그러나 이는 보편적 자연법칙이 아니다. 선로 표면을 따라 미끄러지는 약결합 상태 또는 완전 이탈 뒤 편향 재결합을 허용하면 1접촉부 Brownian ratchet도 평균적인 방향성을 가질 수 있다. 이 때문에 “두 접촉부가 최소”라는 주장은 `CONDITIONAL`이다.

## 6. 최소 상태주기

2접촉부 후보의 한 가지 최소 표현은 다음과 같다.

\[
S_0(i,i+1)\rightarrow S_1(\varnothing,i+1)
\rightarrow S_2(i+1,i+2)\rightarrow S_0(i+1,i+2).
\]

- \(S_0\): 두 접촉부가 결합되어 있고 후방 접촉부가 방출 준비 상태다.
- \(S_1\): 전방 접촉부가 닻으로 남고 다른 접촉부가 이동 가능한 상태다.
- \(S_2\): 이동 접촉부가 다음 위치에 결합해 두 접촉부가 다시 연결된다.
- 마지막 전이는 접촉부의 전·후방 역할을 교환한다.

필요한 기억은 별도 과거기록이 아니라 현재의 결합·에너지·변형 상태다. 이 상태가 어느 접촉부가 다음에 해리될지를 제한한다.

## 7. 전수조사 결과

접촉부 1–4개와 다음 네 개의 이진 조건을 조합해 64개 구조를 전수조사했다.

- 비평형 에너지 구동 여부
- 선로 극성과의 결합 여부
- 현재상태 기록 여부
- 접촉부 간 조정 여부

엄격한 계약을 만족한 구조는 접촉부가 2·3·4개인 세 구조였고, 비용벡터

\[
C(M)=(N_{\mathrm{contact}},N_{\mathrm{control}},N_{\mathrm{drive}})
\]

에서 유일한 파레토 최소 구조는 다음이었다.

\[
M^*=(2\ \text{contacts},\ \text{drive},\ \text{polarity},\
\text{present record},\ \text{coordination}).
\]

이는 단백질의 실제 접힘이나 서열이 아니라 기능 아키텍처의 최소성이다.

## 8. 강건성 민감도

한 교환창에서 단일 접촉부가 상실될 확률을 \(q\)라 하고, 조정된 \(n\)접촉부의 완전 이탈이 독립적인 동시 상실을 요구한다고 단순화하면

\[
P_{\mathrm{survive}}(N;n,q)=(1-q^n)^N.
\]

100주기 생존확률은 다음과 같다.

| 접촉부 | \(q=0.01\) | \(q=0.05\) | \(q=0.10\) |
|---:|---:|---:|---:|
| 1 | 0.3660 | 0.0059 | 0.0000266 |
| 2 | 0.9900 | 0.7786 | 0.3660 |
| 3 | 0.9999 | 0.9876 | 0.9048 |
| 4 | 0.999999 | 0.9994 | 0.9900 |

이 표는 실험적으로 피팅된 운동학이 아니라 구조적 민감도 분석이다. 환경 위험이 증가하면 3·4접촉부의 여분이 생존을 높이지만, 낮거나 중간인 위험에서는 2접촉부가 비용 대비 최소 구조로 남는다. WRRA 관점에서 여분은 낭비가 아니라 경계조건이 악화될 때 생존범위를 확장하는 비용이다.

목표 생존률을 \(P_*\)로 두면 필요한 최소 접촉부 수는 선언한 모델 안에서

\[
n_{\min}=\left\lceil
\frac{\ln\left(1-P_*^{1/N}\right)}{\ln q}
\right\rceil
\]

이다. 100주기 동안 90% 이상 생존을 요구하면 \(q=0.01\)에서는 2개, \(q=0.05\)와 \(0.10\)에서는 3개, \(q=0.20\)에서는 5개가 필요하다. 따라서 WRRA가 선택하는 최소 구조는 고정된 숫자가 아니라 선언된 환경 경계와 생존 계약의 함수다.

### 에너지로부터 얻는 이상적 하중 상계

한 에너지 입력이 한 번의 길이 \(d\) 전진과 결합한다면 양의 순방향 작동의 이상적 열역학 경계는

\[
F d < \Delta\mu,
\qquad
F_{\max}^{\mathrm{ideal}}=\frac{\Delta\mu}{d}
\]

이다. 생리조건에서 ATP 자유에너지를 약 \(20k_{\mathrm B}T\), \(T=310\,\mathrm K\), \(d=8\,\mathrm{nm}\)로 놓으면 이상적 상계는 약 \(10.7\,\mathrm{pN}\)이다. 이는 손실이 없는 가역 상계이지 실제 키네신의 stall force 예측값이 아니다. 실제 단일 키네신은 대략 5–7 pN 범위가 보고되어 있어 상계 아래에 놓인다.

## 9. 자연 모터와의 사후 대조

블라인드 도출을 고정한 뒤 자연 모터와 대조했다.

| WRRA가 요구한 기능 | 키네신-1에서의 구현 |
|---|---|
| 두 접촉부 | 두 개의 motor head |
| 비평형 에너지 입력 | ATP 결합·가수분해 |
| 극성 결합 | 미세소관 plus-end 방향성 |
| 현재상태 기록 | nucleotide occupancy와 head 간 strain |
| 구조적 조정 | neck linker와 gating |
| 공통운반자 | ATP 상태를 기계운동으로 바꾸는 구조변화 |
| 출력 인터페이스 | stalk·tail·cargo adaptor |

키네신-1은 실제로 두 머리를 이용해 약 8 nm의 hand-over-hand 보행을 하고, neck linker의 방향과 결합상태가 두 머리의 순서를 조절한다. 또한 한 ATP 가수분해가 대략 한 번의 8 nm 전진과 결합한다. 반면 단량체 KIF1A는 편향 Brownian motion으로 plus-end 방향 평균 이동이 가능하다고 보고되어 있다. 이는 WRRA 모델이 분리한 엄격한 2접촉부 보행과 완화된 1접촉부 ratchet의 두 영역에 각각 대응한다.

이 일치는 WRRA가 키네신의 세부구조를 새로 발견했다는 뜻은 아니다. 현재 성과는 자연 모터의 핵심 기능구조를 WRRA의 최소계산·fixed-present·boundary·carrier 원리로 독립 재구성했다는 수준이다.

## 10. 단백질 설계로 내려가기 위한 모듈

현재 결과에서 필요한 단백질 기능 모듈은 여섯 개다.

1. **Track-binding interface:** 선로의 반복단위와 극성을 구별한다.
2. **Energy-transducing pocket:** 화학 자유에너지 입력을 받는다.
3. **Directional converter:** 에너지상태를 비대칭 구조변화로 바꾼다.
4. **Paired-contact scaffold:** 두 접촉부를 한 개체로 유지한다.
5. **Present-state gate:** 한 접촉부의 상태가 다른 접촉부의 전이를 제한한다.
6. **Output interface:** 화물 또는 형광표지를 연결한다. 보행 자체에는 선택적이다.

최초 실물 설계는 세 층으로 분리한다.

- **양성대조군:** 이미 검증된 KIF5 계열 보행체. 실험계가 작동하는지 확인한다.
- **WRRA 최소 혼성체:** 검증된 에너지·선로 결합 코어와 재설계한 조정·이량체·출력 모듈을 결합한다.
- **완전 신생체:** 모든 모듈을 새 서열로 만든다. 현재 단백질 설계의 최전선이므로 앞의 두 층을 통과한 뒤 진행한다.

## 11. 주장 원장

### EXACT — 선언한 수학모델 내부

- \(\mathcal A=0\)이면 두 결과 전이모델의 평균 순이동은 0이다.
- 이산 위치를 바꾸는 단일 점 접촉부는 엄격한 항상-결합 조건을 만족하지 못한다.
- 열거한 64개 구조 중 2접촉부 조정형이 유일한 파레토 최소다.

### CONDITIONAL

- 두 접촉부의 최소성은 이산 선로·항상-결합·자율 보행 계약에 의존한다.
- \(q^n\) 보호는 접촉부 상실의 독립성을 가정한 민감도 모델이다.
- 현재상태 기록이 실제 단백질에서 nucleotide occupancy나 strain으로 구현될 수 있다는 판단은 구조 후보 가설이다.

### OPEN

- 최소 접힘 구조
- 아미노산 서열
- 발현 가능한 DNA 서열
- 세포 내 올바른 접힘과 안정성
- 실제 속도·연속 이동거리·하중·ATP 효율
- 세포독성과 내인성 수송계 교란

## 12. 다음 단계

다음 단계에서는 양성대조군과 WRRA 최소 혼성체를 분리해 아미노산 수준의 후보를 만든다. 먼저 각 잔기와 모듈에 `INPUT`, `INHERITED`, `DESIGNED`, `CALIBRATED`, `PREDICTED`, `OPEN` 소유권을 부여한다. 그 뒤 구조예측·응집·이량체 형성·선로 결합·에너지 포켓 보존을 검사하고, 통과한 단백질에 대해서만 발현 숙주에 맞춘 DNA 염기서열을 작성한다.

## 참고문헌

1. Dogan MY et al. *Kinesin's front head is gated by the backward orientation of its neck linker.* Cell Reports (2015).
2. Mizuhara Y, Takano M. *Biased Brownian motion of KIF1A and the role of tubulin's C-terminal tail studied by molecular dynamics simulation.* Proteins (2021).
3. Hua W et al. *Kinesin hydrolyses one ATP per 8-nm step.* Nature (1997). PMID: 9237757.
4. Coy DL et al. *Kinesin takes one 8-nm step for each ATP that it hydrolyzes.* Journal of Biological Chemistry (1999).
5. Budaitis BG et al. *Neck linker docking is critical for kinesin-1 force generation in cells but at a cost to motor speed and processivity.* eLife (2019), Article 44146.
6. Cross JA et al. *A de novo designed coiled coil-based switch regulates the microtubule motor kinesin-1.* Nature Chemical Biology (2024), DOI: 10.1038/s41589-024-01640-2.
7. Svoboda K, Block SM. *Force and velocity measured for single kinesin molecules.* Cell (1994), DOI: 10.1016/0092-8674(94)90060-4.
8. Nishiyama M et al. *Kinetics of force generation by single kinesin molecules activated by laser photolysis of caged ATP.* PNAS (1999).
