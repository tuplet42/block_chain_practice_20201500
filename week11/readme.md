# block_chain_practice_20201500
20201500 최진우 블록체인실습 11주차 실습입니다.

## Overall Structures : 
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


## 실습 - 1번 : DAO Hack - Reentracy
1. Vulnerability
   취약한 SimpleDAO 컨트랙트는 withdraw() 함수에서 사용자의 잔액을 차감하기 전에 먼저 ETH를 전송함.
``` solidity
(bool success, ) = msg.sender.call{value: amount}("");
require(success, "Transfer failed");

balances[msg.sender] -= amount;
```
  이 구조에서는 공격 컨트랙트가 ETH 받는 순간 receive() 함수에서 다시 withdraw() 호출 가능.
  즉, 잔액이 차감되지 전에 반복 출금이 가능해짐.

2. Attack Flow
   1) SimpleDAO 배포
   2) DAO에 10ETH 입금
   3) AttackDAO 배포
   4) 공격 컨트랙트가 1ETH를 deposit
   5) withdraw() 호출
   6) receive()에서 재귀적으로 withdraw() 재호출
   7) DAO 자금 drain

3. Result
DAO에 있던 10ETH와 공격지가 deposit한 1ETH까지 총 11ETH가 공격 컨트랙트로 이동하였다.
- deploy.js 실행
<img width="535" height="120" alt="deployjs실행결과" src="https://github.com/user-attachments/assets/35a6bd8c-375c-444d-b3eb-f82e077c9e28" />
<img width="549" height="852" alt="deployjs노드터미널" src="https://github.com/user-attachments/assets/5c6b997e-2394-4e3b-bd9f-0ea2725b5a1d" />


- attack.js 실행
<img width="541" height="97" alt="attackjs실행결과" src="https://github.com/user-attachments/assets/862896f0-54d0-483f-9379-410300abdbea" />
<img width="557" height="526" alt="attackjs노드터미널" src="https://github.com/user-attachments/assets/f203616a-d0a3-4786-ad8e-74ddc32bef94" />


4. Fix 1 - Checks-Effects-Interactions
상태 변경을 외부 호출보다 먼저 수행한다.
``` solidity
balances[msg.sender] -= amount;

(bool success, ) = msg.sender.call{value: amount}("");
require(success, "Transfer failed");
```
- result    
    <img width="520" height="153" alt="testCEIjs실행결과" src="https://github.com/user-attachments/assets/4603e959-6129-41ef-9b0b-6d689a707bc9" />
    <img width="519" height="511" alt="testCEIjs노드터미널1" src="https://github.com/user-attachments/assets/5426f4bd-d420-4d7e-8d53-b5c55551a03c" />
    <img width="531" height="756" alt="testCEIjs노드터미널2" src="https://github.com/user-attachments/assets/8c8b1268-e0a9-4e9f-aac8-be950a053852" />


5. Fix 2 - Reentrancy Guard
locked 변수를 사용하여 함수 실행 중 재진입을 막는다.
``` solidity
modifier noReentrant() {
    require(!locked, "No reentrancy");
    locked = true;
    _;
    locked = false;
}
```
- Result
<img width="520" height="157" alt="testGuardjs실행결과" src="https://github.com/user-attachments/assets/2ba89840-b5ad-4010-affe-20a97e570c8c" />
<img width="519" height="794" alt="testGuard노드터미널1" src="https://github.com/user-attachments/assets/f9998997-79cb-452c-8dab-49ce91abe300" />
<img width="520" height="478" alt="testGuard노드터미널2" src="https://github.com/user-attachments/assets/353437d4-13a1-44ea-9279-4ba81220285a" />


6. Fix 3 - Pull-over-push
컨트랙트가 직접 ETH를 밀어 보내는 대신, 사용자가 출금을 요청하고 나중에 직접 claim하는 구조로 변경하였다.
``` solidity
function requestWithdraw(uint amount) public {
    balances[msg.sender] -= amount;
    pendingWithdrawals[msg.sender] += amount;
}

function claim() public {
    uint amount = pendingWithdrawals[msg.sender];
    pendingWithdrawals[msg.sender] = 0;

    (bool success, ) = msg.sender.call{value: amount}("");
    require(success, "Transfer failed");
}
```
- Result
<img width="518" height="155" alt="testPulljs실행결과" src="https://github.com/user-attachments/assets/9b4aaea2-d4e7-4ec3-ab17-7dcbf928b431" />
<img width="526" height="832" alt="testPulljs노드터미널1" src="https://github.com/user-attachments/assets/39bb75ee-af77-46ac-9cf8-2f1b66215c47" />
<img width="522" height="416" alt="testPulljs노드터미널2" src="https://github.com/user-attachments/assets/e451eb79-48ec-4a57-8d77-cc1b211d831c" />


## 실습 - 2번 : Parity Wallet Hack #1 - Unathorized Initialization
1. Vulnerability
Parity Wallet 구조는 Wallet 컨트랙트가 직접 로직을 가지지 않고, Library 컨트랙트에 delegatecall을 수행하는 구조이다.
취약한 WalletLibrary에는 initWallet() 함수가 존재하고, 이 함수에 접근 제어와 초기화 여부 검사가 없다.
``` solidity
function initWallet(address _owner, uint _required) public {
    owner = _owner;
    required = _required;
}
```

2. delegatecall Storage Structure
```
[Wallet Contract]                         [WalletLibrary Contract]
storage                                   code
---------------------------------------------------------------
slot 0 : owner        <--- delegatecall --- initWallet()
slot 1 : required                         execute()
slot 2 : libraryAddress
```
delegatecall은 Library의 코드를 실행하지만, storage는 호출한 Wallet의 storage를 사용한다.
따라서 공격자가 Wallet 주소에 대해 initWallet(attacker, 1)을 호출하면, Library의 코드가 실행되지만 실제로 변경되는 값은 Wallet의 owner이다.

3. Attack Flow
   1) WalletLibrary 배포
   2) Wallet 3개 배포
   3) 각 Wallet에 3ETH 입금
   4) Wallet1은 정상 사용자가 초기화
   5) Wallet2, Wallet3은 공격자가 initWallet() 호출
   6) Wallet2, Wallet3의 owner가 attacker로 변경
   7) attacker가 execute()를 호출하여 ETH 송금
  

4. Result
<img width="517" height="330" alt="ParityHack1js실행결과" src="https://github.com/user-attachments/assets/bd8a682a-589d-4e8c-a05f-af84c6aef979" />
<img width="523" height="850" alt="ParityHack1js노드터미널1" src="https://github.com/user-attachments/assets/347a118b-5b57-47f0-b1b9-92659f593ee9" />
<img width="523" height="835" alt="ParityHack1js노드터미널2" src="https://github.com/user-attachments/assets/2ca666bc-2ee9-4dd4-a18b-0c955ca087b3" />
<img width="522" height="670" alt="ParityHack1js노드터미널3" src="https://github.com/user-attachments/assets/0e4e2d44-6eac-43f6-8ce3-201965d6be16" />
<img width="521" height="634" alt="ParityHack1js노드터미널4" src="https://github.com/user-attachments/assets/182ff136-2de3-4600-ad28-5fff6150b2e7" />


5. Fix
initialized 변수를 추가하여 한 번 초기화된 Wallet은 다시 초기화할 수 없도록 수정하였다.
``` solidity
bool public initialized;

function initWallet(address _owner, uint _required) public {
    require(!initialized, "Already initialized");

    owner = _owner;
    required = _required;
    initialized = true;
}
```

6. Fixed Result
공격자가 다시 initWallet()을 호출했지만 실패했고, owner는 정상 사용자 주소로 유지되었다.
<img width="516" height="174" alt="testParityFix1js실행결과" src="https://github.com/user-attachments/assets/15384e4a-fbf7-4f18-bbd5-a2c453a0de57" />
<img width="520" height="867" alt="testParityFix1js노드터미널1" src="https://github.com/user-attachments/assets/42e6fa68-8f5e-4737-ba5d-01bd5911d232" />
<img width="521" height="524" alt="testParityFix1js노드터미널2" src="https://github.com/user-attachments/assets/ac4d8e9c-64dc-4807-90bc-cd39c579756b" />

## 실습 - 3번 : Parity Wallet Hack #2 - Library Selfdestruct
1. Vulnerability
세 번째 실습은 여러 Wallet이 하나의 공유 Library에 의존하고, 해당 Library에 public kill()함수가 존재하는 구조를 재현하였다.
``` solidity
function kill() public {
    selfdestruct(payable(msg.sender));
}
```
공격자가 Library 자체에 initWallet()을 호출하여 Library의 owner가 된 후, kill()을 호출하면 Library가 제거되어 모든 Wallet의 delegatecall 대상이 사라지는 구조이다.

2. Attack Flow
    1) WalletLibaryKill 배포
    2) Wallet 3개 배포
    3) 모든 Wallet이 같은 Libary 주소를 참조
    4) 각 Wallet에 3 ETH 입금
    5) 정상 사용자가 Wallet들을 초기화
    6) 공격자가 Library 자체에 initWallet(attacker, 1) 호출
    7) 공격자가 Library의 owner가 됨
    8) 공격자가 kill() 호출
    9) Wallet들이 delegatecall할 Library code를 잃어 기능이 정지됨

3. Actual Result in Current Environment
현재 Hardhat / Solidity 환경에서는 selfdestruct 동작이 과거 Ethereum과 다르게 처리된다.
특히 Cancun 이후의 EVM에서는 selfdestruct가 기존 컨트랙트 코드를 완전히 삭제하지 않는다.

- result
<img width="533" height="801" alt="ParityHack2js실행결과" src="https://github.com/user-attachments/assets/78043260-fb64-4825-ba10-0234ead1a3e2" />
<img width="520" height="602" alt="ParityHack2js노드터미널1" src="https://github.com/user-attachments/assets/0b277adc-99ca-4aaf-8058-d38f183c7b63" />
<img width="525" height="497" alt="ParityHack2js노드터미널2" src="https://github.com/user-attachments/assets/8ca6622c-1a37-4aa8-a11a-da93bb9a4124" />
<img width="518" height="801" alt="ParityHack2js노드터미널3" src="https://github.com/user-attachments/assets/0161b6a5-a884-4c5c-b36e-59f179fce711" />
<img width="521" height="739" alt="ParityHack2js노드터미널4" src="https://github.com/user-attachments/assets/b23e7ec6-3fd9-4122-978c-cd9e0a4ca608" />
<img width="521" height="763" alt="ParityHack2js노드터미널5" src="https://github.com/user-attachments/assets/f9011c8b-5ec5-4d8d-8c8e-5fcb03674dc5" />
<img width="523" height="76" alt="ParityHack2js노드터미널6" src="https://github.com/user-attachments/assets/01cfd25c-e0cb-45c0-9753-7db917e399f0" />

즉, 공격자는 Library의 owner가 되었고 kill() 호출도 수행했지만, 현재 환경에서는 Library bytecode가 삭제되지 않았다.
그 결과 Wallet의 delegatecall이 계속 동작했고, 과거 Parity Wallet freeze 현상이 완전히 재현되지는 않았다.

4. Analysis
과거 Parity Wallet Hack #2에서는 Library 컨트랙트가 selfdestruct되면서 해당 Library를 참조하던 모든 Wallet이 로직을 잃었다.
Wallet 내부 ETH는 그대로 남아 있었지만, 출금 로직을 실행할 수 없었기 때문에 자금이 도난된 것이 아니라 동결되었다.

이번 실습에서는 최신 EVM의 selfdestruct 동작 변경으로 인해 같은 현상이 완전히 발생하지 않았다.
하지만 하나의 공유 Library에 여러 Wallet이 의존하고, Library에 위험한 public 함수가 존재할 경우 전체 시스템에 치명적인 영향을 줄 수 있음을 확인하였다.


5. Fix
수정 방향은 다음과 같다.
1) selfdestruct 제거
2) initWallet() 재초기화 방지
3) 중요 함수에 접근 제어 추가
``` solidity
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

contract FixedWalletLibraryKill {
    address public owner;
    uint public required;
    bool public initialized;

    modifier onlyOwner() {
        require(msg.sender == owner, "Not owner");
        _;
    }

    function initWallet(address _owner, uint _required) public {
        require(!initialized, "Already initialized");

        owner = _owner;
        required = _required;
        initialized = true;
    }

    function execute(address payable to, uint amount) public onlyOwner {
        (bool success, ) = to.call{value: amount}("");
        require(success, "Transfer failed");
    }

    // selfdestruct function removed
}
```


## Conclusion
이번 실습을 통해 다음 내용을 확인하였다.
1. Reentrancy는 외부 호출 전에 상태 변경을 하지 않을 때 발생할 수 있다.
2. delegatecall은 Library의 코드를 실행하지만, storage는 호출한 컨트랙트의 storage를 사용한다.
3. 초기화 함수에는 반드시 접근 제어 또는 재초기화 방지 로직이 필요하다.
4. 여러 Wallet이 하나의 Library에 의존하는 구조에서는 Library의 취약점이 전체 Wallet에 영향을 줄 수 있다.
5. selfdestruct는 과거에는 컨트랙트 코드를 제거할 수 있었지만, 최신 EVM에서는 동작이 변경되었으므로 과거 취약점 재현 결과가 달라질 수 있다.
   <img width="825" height="732" alt="4-afterwithdraw" src="https://github.com/user-attachments/assets/8756fdf2-0003-4566-b437-dbceb56f9bc6" />
