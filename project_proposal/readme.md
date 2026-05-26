# block_chain_practice_20201500
20201500 최진우 블록체인실습 제안서 작성 후 그대로 구현하는 과제입니다.

## Overall Structures : 
```
├── creator_support_DAO_v2.sol
├── Creator_Support_DAO_v2.html
├── Creator_Support_DAO_proposal_ppt.pptx
└── readme.md
```

## Overview : Creator Support DAO
기존 "Buy Me a Coffee" 형태의 단순 후원 DApp을 확장한 참여형 후원 플랫폼입니다.
사용자는 ETH를 이용해 후원할 수 잇으며, 후원 보상으로 ERC-20 기반의 CoffeeToken을 지급받습니다.
또한 DAO의 핵심 개념인 Proposal 및 Voting 구조를 간소화하여 적용하였으며, 후원자가 단순 후원자에 그치지 않고 플랫폼 운영 바향에 참여할 수 있도록 구성하였습니다.

기존 후원 플랫폼은 다음과 같은 한계가 존재합니다.
- DAO Hack - Reentrancy Attack
- Parity Wallet Hack #1 - Unauthorized Initialization
- Parity Wallet Hack #2 - Library Selfdestruct / Frozen Funds
이를 해결하기 위해 일반 후원가 Proposal 전용 후원을 분리하고, Proposal 및 투표 시스템을 도입하여 후원자가 자금 사용 방향에 참여할 수 있도록 설계하였습니다.

### 지난 발표와의 변경점
'일반 후원금과 Proposal 전용 후원금을 별도 balance로 관리한다'고 설명 가능하다. 
- 후원금 사용 목적에 따라 일반 후원과 Proposal 전용 후원 분리하여 Proposal에서만 후원금을 사용하도록 할 수 있다.
- Proposal 전용 후원으로 후원된 경우 Proposal이 실행 완료된 상태일 때 출금 가능하다.
- Proposal 생성 시 구체적으로 10 COFFEE 토큰을 소모하도록 하여 무분별한 제안 생성을 방지했다.
- 이외에도 VIP 조건을 기존의 5ETH는 너무 큰 것 같아 1ETH로 완화하였다.

## 기술스택
- Solidity
- OpenZeppelin
- Remix IDE
- Ethereum Sepolia Testnet
- MetaMask
- ethers.js

## 주요기능
### DAO_Hack
- ETH 기반 후원 기능
- 후원 기록 블록체인 저장
- 일반 후원 / Proposal 전용 후원 분리

### CoffeeToken(ERC-20)
- 후원 보상 토큰
- Governance Token 역할 수행
- 1ETH 후원 시 100 CoffeeToken 지급
  
### VIP 시스템
- 누적 1 ETH 이상 후원 시 VIP 부여
- VIP 사용자만 Proposal 생성 가능

### Proposal 및 Voting
- Proposal 생성 시 10 CoffeeToken 소모
- 후원자 투표 기능 제공
- 중복 투표 방지

### Proposal 기반 자금 관리
- 일반 후원금은 owner가 출금 가능
- Proposal 전용 후원금은 Proposal 실행 이후에만 출금 가능

### Governance 흐름
MetaMask 연결
- ETH 후원
- CoffeeToken 지급
- VIP 판별
- Proposal 생성
- 투표 진행
- Proposal 실행
- Proposal 전용 자금 출금
  
### Proposal 상태 흐름
- Active -> Passed/Rejected -> Executed

## 스마트 컨트랙트 구조
### CoffeeToken - ERC-20 기반 토큰 컨트랙트
- mint(), burnFrom()의 주요 기능

### CreatorSupportDAO : DAO 핵심 로직 컨트랙트
- donate(), donateToProposalFund(), createProposal(), vote(), executeProposal(), withdrawGeneral(), withdrawProposalFund() 등 주요 기능

## 보안 요소
### Reentrancy 공격 방지
- ReentrancyGuard 적용
- CEI(Check-Effects-Interactions) 패턴 적용
### 접근 제어
- onlyOwner Modifier 적용
### 중복 투표 방지
- mapping(uint256 => mapping(address => bool)) voted;
### Proposal 상태 검증
- 실행된 Proposal 재실행 방지
- 반대표가 더 많은 Proposal 실행 방지

## 프론트엔드
HTML / CSS / JavaScript 및 ethers.js 기반으로 구성- 출금 요청 저장
- MetaMask 연결
- 후원 기능
- Proposal 생성 및 투표
- Proposal 상태 표시
- 후원 로그 조회
- Coffee 잔액 표시
---
<img width="916" height="614" alt="html구성1" src="https://github.com/user-attachments/assets/dda6bc9b-91d8-454a-ac0c-cda4d8cf1b49" />
<img width="909" height="709" alt="html구성2" src="https://github.com/user-attachments/assets/c331b53d-4486-44fe-97ea-fbdbfa8bb944" />
<img width="907" height="823" alt="html구성3" src="https://github.com/user-attachments/assets/a5175302-1ad9-4d1c-a75c-0c65c5e8d5df" />


## How to Run
### Remix IDE로 컨트랙트 생성
1. sol 파일을 이용해서 compile -> deploy한다. 이때 MetaMask 지갑을 WalletConnect -> MetaMask로 연결해준다.
2. Deploy 순서는 CoffeeToken, CreatorSupportDAO 순서로 진행한다. 일단 CoffeeToken을 deploy하고 컨트랙트 주소를 복사해두자.
3. CreatorSupportDAO를 Deploy한다. 이때 복사해둔 CoffeeToken 컨트랙트 주소를 tokenAddress에 붙여넣기 후 진행해야 한다.
4. Deployed Contracts에 CoffeeToken으로 들어가서 TransferOwnership에 CreatorSupportDAO 컨트랙트 주소를 넣는다.
<img width="279" height="730" alt="remix1_token_and_DAO" src="https://github.com/user-attachments/assets/878341a0-8928-4bc9-a42e-00a9d52bf658" />
<img width="637" height="618" alt="coffeetoken_transferownership" src="https://github.com/user-attachments/assets/bcbc47f0-3781-4fd5-a685-731e7eb79ff5" />

### MetaMask 연결
1. MetaMask 연결 버튼 클릭 시 연결이 된다.
<img width="909" height="344" alt="metamask연결" src="https://github.com/user-attachments/assets/18fe423b-4dd1-42b8-bcdb-4b9db9132b91" />

### Donate
1. 일반 후원과 Proposal 전용 후원으로 나누어져 있으며 Small, Large, Whale, 이외에도 더 많은 양을 직접 입력을 통해 후원할 수 있다.
2. 1ETH 후원 시 100 CoffeeToken의 비율로 후원한 만큼 같은 비율로 받게 된다.
<img width="893" height="562" alt="후원완료" src="https://github.com/user-attachments/assets/faae1663-2eb1-4833-8c3d-6b086838a58c" />

3. 1ETH 이상 후원 시 VIP 상태가 되고, Proposal 생성이 가능해진다.
<img width="914" height="288" alt="became_vip" src="https://github.com/user-attachments/assets/043d00ff-09f3-4979-a221-8f5ca19b182f" />

### Proposal
1. VIP가 되면 Proposal을 생성할 수 있다.
2. 매번 Proposal을 만들 때마다 10 CoffeeToken을 사용하여 Proposal 생성을 눌러서 생성이 가능하다.
<img width="906" height="399" alt="proposal생성" src="https://github.com/user-attachments/assets/508fbce1-1dc2-47e8-94c0-f9c4a2c9f56b" />

3. Proposal의 경우 진행중, 통과/거절, 실행 완료의 상태가 있고 투표를 통해 찬성/반대로 표를 던질 수 있다. 한번 투표하면 다른 의견으로 투표가 불가능하다.
4. 찬성 상태일 때 Proposal 실행 시 실행 완료 상태가 된다.
<img width="1024" height="934" alt="proposal상태와목록" src="https://github.com/user-attachments/assets/aa5d9293-10f2-4272-a358-f7754a75ec9d" />

5. Proposal에 대해서도 Proposal 전용으로 일반적인 후원 방식처럼 후원이 가능하다. 그리고 후원 목록도 proposal 후원으로 확인 가능하다.
<img width="1421" height="574" alt="proposal전용후원" src="https://github.com/user-attachments/assets/f22a6c04-0a62-4e8e-a8c9-99ebebf43a55" />
<img width="1052" height="543" alt="proposal후원목록" src="https://github.com/user-attachments/assets/a7f90580-a197-4d64-9c85-4385ef64b9e8" />

### Withdraw
1. 현재 후원을 받아서 아래의 사진과 같은 상태이다.
<img width="1053" height="279" alt="withdraw이전" src="https://github.com/user-attachments/assets/ca133d18-677d-4405-903b-89653cdac957" />

2. 일반출금의 경우 일반 후원금 출금으로 바로 출금이 가능하고, Proposal 전용 출금의 경우 실행완료된 Proposal ID를 입력하고 출금이 가능하다.
<img width="1418" height="288" alt="일반출금" src="https://github.com/user-attachments/assets/57e93241-15cf-4516-bac4-6b3364a75ca5" />

3. 일반출금과 Proposal 전용 출금을 하면 아래와 같이 컨트랙트에 쌓여있던 ETH가 프론트엔드 상으로 다 빠진 것을 확인할 수 있다.
<img width="1051" height="273" alt="withdraw후" src="https://github.com/user-attachments/assets/c6e29b66-6473-4047-9ae7-8194b669309f" />

## Self Feedback
- Proposal 전용 withdraw나 후원을 후원하고자 Proposal ID를 정해서 하도록 하면 어떤 Proposal에 얼마나 돈이 쌓였고, 쌓여있는 Proposal 전용 후원금에서 그만큼의 돈을 출금할 수 있을 것이다. 
