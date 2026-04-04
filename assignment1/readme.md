# block_chain_practice_20201500
20201500 최진우 블록체인실습 과제1입니다.

# This repository contains:
- Counter, CounterNumber, Faucet에 대한 과제 html 시뮬레이션

# Overall Structures : 
```
├── README.md
└── week5_assignment_faucet.html
```
## week5_assignment_faucet.html Descriptions
1. 탭1 - Counter.sol
2. 탭2 - CounterNumber.sol
3. 탭3 - Faucet.sol

## Task Item : Counter.sol, CounterNumber.sol
1. Counter.sol 동작 확인
: Counter는 public 변수로 자동 getter를 사용하는 간단한 상태 변경 컨트랙트이다. 컴파일, 배포를 수행한 후, counter(), get()함수 실행시키고, count()로 상태 변경 후 counter(), get()을 실행하였다.
<img width="1575" height="945" alt="image" src="https://github.com/user-attachments/assets/d39f8a2d-637e-4600-bf24-a96f8d49b4c6" />
2. CounterNumber.sol 동작 확인
: CounterNumber는 private 변수와 getter/setter를 통해 접근을 제어하며, 인터페이스를 이용해 다른 컨트랙트에서 값을 읽을 수 있다.
처음에 getNumber()로 10이 호출되고 외부 조회 결과도 마찬가지지만, setNumber(25)가 실행된 후 getNumber()랑 외부 조회 결과도 25가 된다.
<img width="1581" height="941" alt="image" src="https://github.com/user-attachments/assets/240a649a-6d01-470f-a368-ac6f06f7066b" />


## Task Item : Faucet.sol
1. Faucet.sol 배포 & 테스트
: 배포한 계정이 owner가 되기 때문에 withdrawAll() 권한을 가지게 된다.
<img width="1581" height="953" alt="1" src="https://github.com/user-attachments/assets/f670b553-c7ab-468f-a873-f3e3c3aa153e" />

2. msg.sender 계정 변경 확인
: Faucet을 한 계정(Account1)으로 배포하고 deposit이나 withdraw 실행 시 성공하는 반면
그렇지 않은 계정(Account2)로 같은 행동 수행 시 owner가 아니라 실패하는 모습을 보인다.
<img width="1563" height="946" alt="2-1" src="https://github.com/user-attachments/assets/d58b29c7-9f0c-4961-af55-5b7450450b32" />
<img width="1584" height="930" alt="2-2" src="https://github.com/user-attachments/assets/7750f348-5d20-41cc-9c6d-9e92c43e5fea" />

3. msg.value 다양한 값 테스트
: msg.value 값을 바꿔가며 deposit, receive 등 테스트를 진행하였다.
<img width="1574" height="937" alt="3-1" src="https://github.com/user-attachments/assets/a47a2419-477d-4f18-98a5-9f2ab6a56a54" />
<img width="1614" height="947" alt="3-2receive직접전송" src="https://github.com/user-attachments/assets/ca98de7b-6fe9-4adb-b74b-a02ce0c0b4aa" />
<img width="381" height="205" alt="3-3로그" src="https://github.com/user-attachments/assets/f7d0b021-7db5-49c1-80ce-49300af22390" />

4. withdraw() 24시간 제한 확인
: withdraw()를 한번 실행한 후 다시 실행하면 하루가 지나지 않아 실패했다는 로그가 뜨지만,
+1day 버튼을 누른 후 withdraw()를 다시 실행하면 하루가 지난 상태기 때문에 성공한 로그가 뜬다.
<img width="1580" height="942" alt="4-1withdraw" src="https://github.com/user-attachments/assets/132c5575-5056-463d-af11-fcc052fa8438" />
<img width="1578" height="922" alt="4-2withdrawafteroneday" src="https://github.com/user-attachments/assets/15aaa949-0275-4e2b-86e1-46f774ea720b" />

5. 다른 계정으로 withdrawAll() 결과
: owner 계정만 가능하기 때문에 Account2의 경우 실패하는 모습이다. Owner 계정인 Account1에서는 성공한 모습을 보인다.
<img width="1602" height="868" alt="5-1withdrawallnotowner" src="https://github.com/user-attachments/assets/944b35ed-e3ef-4310-bdc2-afa050d9065c" />
<img width="1573" height="884" alt="5-2withdrawallowner" src="https://github.com/user-attachments/assets/1e102105-b948-4c03-acc9-3ee8898253d9" />
