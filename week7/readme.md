# block_chain_practice_20201500
20201500 최진우 블록체인실습 7주차 실습입니다.

# Overall Structures : 
```
├── README.md
├── token.sol
└── stacking.sol
```
## 역할
token.sol : ERC-20 토큰. 주요 함수는 아래와 같다.
- transfer() : 내가 직접 토큰을 보냄.
- approve() : 다른 컨트랙트에게 사용 허락.
- transferFrom() : 허락받은 컨트랙트가 대신 이동
- balanceOf() : 잔액조회

stacking.sol : 
- stack() - token.sol의 transferFrom()을 써서 토큰을 컨트랙트로 가져온다.
- withdraw() - token.sol의 transfer()을 써서 토큰을 돌려준다.
- getStakedBalance() - 내가 얼마 맡겼는지 조회한다.

## Process
1. token.sol을 compile하고 deploy한다. 이때 Deploy & Run transactions -> Environment에서 WalletConnect(MetaMask)로 수정한다.
2. deploy해서 뜬 컨트랙트 주소를 복사한다.
3. stacking.sol을 compile하고 deploy한다. 이때 Deploy & Run transactions -> Environment에서 WalletConnect(MetaMask)로 수정하고, '_token'에 token.sol을 deploy해서 뜬 컨트랙트 주소를 복붙하고 deploy해야 한다.
4. stacking.sol을 deploy한 컨트랙트 주소를 복사한다.
5. Stake 트랙잭션 수행을 위해 Deployed Contracts에서 MyToken을 펼쳐서 approve 함수를 클릭하고, spender에 stacking 컨트랙트 주소, amount에 가져가도록 할 양을 입력한다. 
6. stacking 컨트랙트 펼쳐서 stake 함수를 클릭하고, amount에 이전과 같은 양을 입력한다. 그 후 transact를 누른다.
7. 트랜잭션 해시를 저장한다.
8. Etherscan으로 트랜잭션 해시나 컨트랙트 주소를 입력하여 각 TX 상태가 Success인지 확인한다.

## 실행결과 : 
Deployment TX Hash(Token) : 0x8f9fa24436acb1c69cb864912eb986f4653d3d36bcfa9d8635cbc8fed66b7f0a

Deployment TX Hash(Stacking) : 0x7e207061997d59583f25068372b1391d20b7fd707dc8580b582e22234575911f

Stake TX Hash : 0xe38f4c9a6e36ded851a0336027433d6b83709c4421a742adfa1e032109b9eec3

Withdraw TX Hash : 0xdd664337dad89b5c78517a1070594aa989a12b6c76002b79654f24bded6f6c07

<img width="781" height="396" alt="image" src="https://github.com/user-attachments/assets/6758eff1-bc2b-4995-9390-f5c59f7b40c9" />
<img width="1468" height="626" alt="image" src="https://github.com/user-attachments/assets/f679d52d-4471-438c-888b-7a18a9f796b9" />
