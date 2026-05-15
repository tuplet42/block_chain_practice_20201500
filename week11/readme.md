# block_chain_practice_20201500
20201500 최진우 블록체인실습 11주차 실습입니다.

# Overall Structures : 
```
├── README.md
├── DAO_Hack
    └── contracts
        ├── AttackDAO.sol
        ├── SimpleDAO.sol
        ├── SimpleDAO_CEI.sol
        ├── SimpleDAO_Guard.sol
        └── SimpleDAO_Pull.sol
    └── scripts
        ├── attack.js
        ├── deploy.js
        ├── testCEI.js
        ├── testGuard.js
        └── testPull.js
├── Parity_Hack_1
    └── contracts
        ├── FixedWallet.sol
        ├── FixedWalletLibrary.sol
        ├── Wallet.sol
        └── WalletLibrary.sol
    └── scripts
        ├── parityHack1.js
        └── testParityFix1.js
└── Parity_Hack_2
    └── contracts
        ├── FixedWalletKill.sol
        ├── WalletKill.sol
        └── WalletLibraryKill.sol
    └── scripts
        └── parityHack2.js
```

## Overview
Ethereum에서 발생했던 대표적인 스마트 컨트랙트 보안 사고를 로컬 Hardhat 환경에서 재현하고, 취약점 원인과 수정 방법을 분석하기 위한 실습이다.
실습 대상은 아래와 같다.
1. DAO Hack - Reentrancy Attack
2. Parity Wallet Hack #1 - Unauthorized Initialization
3. Parity Wallet Hack #2 - Library Selfdestruct / Frozen Funds
모든 실습은 Hardhat local network에서만 수행하였다.

## Environment
node

npm

hardhat@2.22.5

solidity 0.8.24

## 역할
### DAO_Hack
#### SimpleDAO.sol : 취약한 DAO 스마트컨트랙트 역할
- 사용자 ETH deposit 가능
- balances mapping으로 사용자 잔액 관리
- withdraw() 함수 제공
- 외부 호출 후 잔액 차감하는 구조
- Reentrancy 취약점 존재

#### AttackDAO.sol : Reentrancy 공격 컨트랙트 역할
- SimpleDAO와 연결
- attack()으로 공격 시작
- receive()에서 재귀적으로 withdraw() 재호출
- DAO ETH drain 수행
- collect()로 공격자가 ETH 회수 가능

#### SimpleDAO_CEI.sol : Checks-Effects-Interactions 방어 버전
- 상태 변경을 외부 호출 전에 수행
- Reentrancy 공격 방어

#### SimpleDAO_Guard.sol : Reentrancy Guard 방어 버전
- locked 변수와 modifier 사용
- 함수 실행 중 재진입 차단

#### SimpleDAO_Pull.sol : Pull-over-push 구조 적용 버전
- requestWithdraw()로 출금 요청 저장
- claim()으로 사용자 직접 출금
- 외부 호출과 상태 변경 분리

#### deploy.js : DAO 실습 배포 스크립트
- SimpleDAO 배포
- DAO에 10 ETH 입금
- AttackDAO 배포

#### attack.js : Reentrancy 공격 실행 스크립트
- 공격 전 DAO 잔액 조회
- attack() 실행
- 공격 후 DAO 잔액 및 공격 컨트랙트 잔액 조회

#### testCEI.js : CEI 방어 테스트 스크립트
- CEI DAO 배포
- Reentrancy 공격 시도
- 공격 실패 여부 확인

#### testGuard.js : Reentrancy Guard 방어 테스트 스크립트
- Guard DAO 배포
- Reentrancy 공격 시도
- 공격 실패 여부 확인

#### testPull.js : Pull-over-push 구조 테스트 스크립트
- 출금 요청 저장
- claim() 기반 출금 수행
- DAO 잔액 변화 확인

---

### Parity_Hack_1
#### WalletLibrary.sol : 취약한 Wallet Library 역할
- initWallet() 제공
- execute() 제공
- delegatecall 대상 코드 역할
- 재초기화 방지 로직 없음

#### Wallet.sol : delegatecall 기반 Wallet 역할
- ETH 보관
- fallback()에서 Library delegatecall 수행
- 실제 storage(owner, required) 보유

#### FixedWalletLibrary.sol : 수정된 Wallet Library 역할
- initialized 변수 추가
- 재초기화 방지
- execute() 유지

#### FixedWallet.sol : 수정된 Wallet 역할
- initialized storage 추가
- delegatecall storage 구조 유지

#### parityHack1.js : Unauthorized Initialization 공격 재현 스크립트
- WalletLibrary 배포
- Wallet 3개 생성
- Wallet1 정상 초기화
- Wallet2, Wallet3 공격자 초기화
- owner 탈취 확인
- execute()로 ETH drain 수행

#### testParityFix1.js : 수정 버전 테스트 스크립트
- FixedWalletLibrary 배포
- 정상 사용자 초기화 수행
- 공격자 재초기화 시도
- 공격 실패 여부 확인

#### 흐름
-> Wallet이 fallback()으로 WalletLibrary delegatecall 수행
-> 공격자가 initWallet() 호출
-> Wallet storage의 owner 값 변경
-> attacker가 execute() 호출 가능
-> Wallet ETH 출금

---

### Parity_Hack_2
#### WalletLibraryKill.sol : selfdestruct 취약 Library 역할
- initWallet() 제공
- execute() 제공
- kill() 제공
- selfdestruct 취약점 존재

#### WalletKill.sol : 공유 Library 의존 Wallet 역할
- 여러 Wallet이 하나의 Library 공유
- fallback()에서 delegatecall 수행
- ETH 저장 역할 수행

#### FixedWalletKill.sol : 수정된 Library 역할
- initialized 변수 추가
- onlyOwner modifier 적용
- selfdestruct 제거

#### parityHack2.js : Library selfdestruct 공격 재현 스크립트
- WalletLibraryKill 배포
- Wallet 3개 생성
- Wallet 초기화 수행
- 공격자가 Library 직접 initWallet()
- 공격자가 kill() 호출
- Wallet delegatecall 동작 여부 확인
- frozen funds 구조 분석

#### 흐름
-> Wallet들이 하나의 shared library 사용
-> 공격자가 Library 직접 초기화
-> attacker가 Library owner 획득
-> kill() 호출
-> 과거 Ethereum에서는 Library code 제거
-> Wallet delegatecall 실패
-> ETH는 남아있지만 출금 불가능(frozen)

-> 현재 Hardhat/Solidity 환경에서는 selfdestruct 동작 변경으로 인해 완전한 freeze는 재현되지 않음


## How to Run
터미널을 2개 사용한다.
Terminal 1 : Local Blockchain
```bash
npx hardhat node
```
Terminal 2 : Compile and Run Scripts
```bash
npx hardhat compile
npx hardhat run <project_folder>/scripts/<script_name>.js --network localhost
```
<project_folder>는 DAO_Hack, Parity_Hack_1, Parity_Hack_2 중 하나이며, 예시는 아래와 같다.
```bash
npx hardhat run DAO_Hack/scripts/attack.js --network localhost
```


## Process - 1번 : Nodit Console
1. 회원가입 후 API Key를 확인한다.
  <img width="947" height="871" alt="1" src="https://github.com/user-attachments/assets/0b06942b-b420-4971-82c1-b42959504f17" />


## Process - 2번 : GIWA 연동
1. 'Process - 1번'에서 확인한 API Key를 이용하여 MetaMask 내의 GIWA Sepolia Testnet을 구성한다.

2. API Key는 Default RPC URL에서 giwa-sepolia.nodit.io/ 뒤에 복사붙여넣기 하면 된다.
  <img width="366" height="597" alt="2-2" src="https://github.com/user-attachments/assets/cd28adaa-ef9a-4c3c-8596-074cdbaf0f3c" />


3. 아래의 사진처럼 https://faucet.lambda256.io/giwa-sepolia에 들어가서 faucet을 받는다.
  <img width="958" height="813" alt="2-1" src="https://github.com/user-attachments/assets/96575025-5486-4249-a910-060754823e41" />


## Process - 4번 : Dapp 만들기
1. BuyMeACoffeeV2.sol을 compile하고 deploy를 해야된다. 이때 Deploy & Run transactions -> Environment에서 WalletConnect(MetaMask)로 수정한다. 만약 연결 시 다른 네트워크가 잡히면 MetaMask의 네트워크를 Giwa Sepolia로 바꾸고, remix에서 지갑 연결을 끊었다가 다시 연결하면 된다.

2. Deploy 옵션을 MyStableCoin으로 설정 후 Deploy해주자. 그럼 아래처럼 MyStableCoin의 컨트랙트 주소가 나오는데 이를 복사해두자.
  <img width="285" height="806" alt="4-remix배포1" src="https://github.com/user-attachments/assets/9c9068ce-8788-45ef-8965-d33e73fe70b9" />


3. Deploy 옵션을 BuyMeACoffeeStable로 한 뒤 Deploy하자. 이때 _stableCoin에 MyStableCoin의 주소를 붙여넣고 해야된다. deploy해서 뜬 BuyMeACoffeeStable 컨트랙트 주소도 복사해두자.
  <img width="298" height="892" alt="4-remix배포2" src="https://github.com/user-attachments/assets/179ffc30-5b2e-4ba6-a67c-a201d8c1e73a" />


4. html의 TOKEN_ADDRESS에 MyStableCoin 컨트랙트 주소를, CONTRACT_ADDRESS에 BuyMeACoffeeStable 컨트랙트 주소와 붙여넣고 저장한다.
  <img width="552" height="105" alt="image" src="https://github.com/user-attachments/assets/90f95de2-7c1f-4d37-8bb3-d657be698fcc" />


5. Dapp_BuyMeACoffee.html을 vscode의 Open With Live Server로 실행한다.


## 실행결과 : 
1. MetaMask 지갑 연결 - MetaMask 지갑을 연결한다. 연결되면 연결 주소가 뜨고, 추가적으로 연결 주소가 Owner일 경우 Owner의 주소와 출금이 활성화된다. 아래 예시는 Owner의 지갑이 연결되었기 때문에 컨트랙트 잔액 출금이 활성화된 모습이다.
  <img width="881" height="919" alt="4-connectwallet" src="https://github.com/user-attachments/assets/69279319-f43a-415a-a3b1-d081a28d8327" />


2. MSC send - 1MSC, 5MSC, 10MSC의 옵션으로 응원 메시지를 입력하고, Coffee 후원을 할 수 있다. 크게 1단계:MSC 사용 승인 요청, 2단계:후원 트랜잭션 승인 과정을 거쳐 후원이 가능하다. 후원이 완료되면 '후원완료!' 메시지와 함께 TX 해시가 뜬다.
- 1단계:MSC 사용 승인 요청
  <img width="759" height="629" alt="4-coffeedonate" src="https://github.com/user-attachments/assets/86b33041-dd09-4ed9-b605-2b25f4de6459" />


- 2단계:후원 트랜잭션 승인
  <img width="787" height="699" alt="4-coffeedonate2" src="https://github.com/user-attachments/assets/18d7eca5-cba2-4ece-af02-0f0fc16ded7c" />


- 결과
  <img width="827" height="298" alt="4-donateresult" src="https://github.com/user-attachments/assets/f2e1f213-af20-4f53-8b4c-c2d0dd0a4153" />


3. 후원내역 - 후원자의 지갑주소, 금액, 메시지, 시간 등을 확인할 수 있다. 아래는 1MSC, 5MSC, 10MSC로 후원을 했을 때의 내역이다.
  <img width="828" height="954" alt="4-donatehistoryfinal" src="https://github.com/user-attachments/assets/8d3957b0-42be-4ef5-901f-5a89960e550b" />


4. 컨트랙트 잔액 송금
   아래는 커피 후원으로 지갑에서 MSC가 빠져나간 상태이다.
   <img width="829" height="903" alt="4-beforewithdraw" src="https://github.com/user-attachments/assets/9ddcf6c3-bc7b-42b1-a889-ccac870be2fb" />


   컨트랙트 잔액 송금 클릭 시 withdraw를 실행하여 Transaction Request가 뜨고,
   <img width="782" height="907" alt="4-withdraw" src="https://github.com/user-attachments/assets/7a005204-4ef3-4e97-8de6-f1a21f35cd00" />


   이를 confirm하면 owner의 지갑으로 컨트랙트에 쌓였던 MSC가 전부 들어와 있는 모습을 볼 수 있다.
   <img width="825" height="732" alt="4-afterwithdraw" src="https://github.com/user-attachments/assets/8756fdf2-0003-4566-b437-dbceb56f9bc6" />
