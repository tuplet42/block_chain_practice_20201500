# block_chain_practice_20201500
20201500 최진우 블록체인실습 6주차 실습입니다.

# This repository contains:
- 실제 metamask 지갑을 연결해서 faucet 구성.
- connect metamask wallet, refresh(새로고침), claim 0.01ETH 기능으로 구성되어있다.

# Overall Structures : 
```
├── README.md
├── faucet.sol # connect 주소 생성을 위해 compile & deploy한 faucet.sol
└── week5_assignment_faucet.html # 실제 metamask 지갑 연결해서 faucet을 구성하는 시뮬레이션 html
```

## 구성
시뮬레이션 과정의 이미지 예시에서도 나오겠지만 html은 이렇게 구성되어있다.
- 윗부분 : 지갑 주소와 Contract 주소, Request 양, Last Transaction Hash, log로 구성
- 아랫부분 : Refresh나 Claim할 때의 잔액이 기록되는 Faucet Balance Over Time 그래프가 나온다.

## Before simulation
1. faucet.sol을 통해 remix 환경에서 compile & deploy를 실행한다.
2. 이때 Deploy & Run Transcriptions에서 Environment를 Browser Extension (MetaMask)로 바꿔주고 Account도 Account1로 수정해주자.
3. Deploy 버튼을 눌러 Contract 주소를 생성해주자. 이를 이용해 Claim 시 Contract 주소 -> MetaMask 지갑 주소로 ETH가 이동할 예정이다.

   1~3 img :
<img width="291" height="809" alt="previous" src="https://github.com/user-attachments/assets/1baef7bd-337e-4b65-b33f-ba7a81ee611e" />

5. MetaMask 지갑에서 Contract 주소로 어느정도 송금해서 시뮬레이션 준비를 끝내자. (본인은 0.02ETH정도를 Contract 주소로 보냄)
   참조 : Remix를 통해서도 Contract 주소로 송금이 가능한것으로 보이긴 한데 그 시도는 실패했었다.
<img width="804" height="956" alt="previous2" src="https://github.com/user-attachments/assets/db2ed248-c1cb-4d11-bdd7-141d27724ff4" />

6. VScode의 Open with Live Server로 html을 실행한다. 

## Simulation 실행
0. ConnectWallet, Refresh Info, Claim 등 실행 시 그 결과를 로그를 통해 확인이 가능하다.
1. ConnectWallet 버튼 누르면 MetaMask 지갑과 연결된다. MetaMask와 html파일이 같은 브라우저에 있어야 한다.
   <img width="874" height="734" alt="connectwallet" src="https://github.com/user-attachments/assets/31a57ef5-eb5f-4d89-9075-58175ccf0072" />
   
2. Refresh Info를 통해 최신 상태를 확인할 수 있다.
<img width="874" height="815" alt="refresh1" src="https://github.com/user-attachments/assets/e115e960-542b-4bac-9837-8310b56fe1ca" />
<img width="874" height="472" alt="refresh2" src="https://github.com/user-attachments/assets/915779f7-0ef7-4607-a38b-5507464d4715" />

3. Claim을 통해 0.01ETH를 지갑으로 보낸다. 이에 따라 Last Transaction Hash와 그래프에서 Contract 주소의 ETH 양이 줄어든 것을 확인할 수 있다. 또한 다시 Claim을 시도하면 24시간이 지나지 않아 claim에 실패한 로그도 확인 가능하다.
<img width="906" height="863" alt="claim1" src="https://github.com/user-attachments/assets/63d64c1d-3dcc-4782-9f76-8b63dbfb54c3" />
<img width="872" height="821" alt="claim3" src="https://github.com/user-attachments/assets/7eab8980-5f59-49c5-9bdd-a0228395f9c6" />
<img width="872" height="472" alt="claimfaucet0" src="https://github.com/user-attachments/assets/ed855770-0abb-4faf-9013-7d9df739f721" />
<img width="873" height="823" alt="claimfailed" src="https://github.com/user-attachments/assets/58bef44a-afc7-4cf2-bdc4-22dbdfdec50a" />



