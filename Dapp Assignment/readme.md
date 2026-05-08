# block_chain_practice_20201500
20201500 최진우 블록체인실습 Dapp 과제입니다.

# Overall Structures : 
```
├── README.md
├── BuyMeACoffee.sol
└── Dapp_BuyMeACoffee.html
```

## 과제 의도
나만의 Dapp을 만드는 과제였고, 그러다 생각난 아이디어가 개발자들이 종종 BuyMeACoffee와 같이 후원을 열어두고 있던 것이 떠올랐다.
그래서 이를 구현해보면 어떨까 생각해봤다.
GIWA Sepolia Testnet 환경에서 MetaMask를 연결하여 owner한테 후원을 하고, owner는 컨트랙트에 쌓인 ETH를 출금하는 것으로 구현할 수 있었다.

## 역할
BuyMeACoffee.sol : Dapp의 스마트컨트랙트(백엔드) 역할. 
크게 후원금 받기, 후원 기록 저장, 총 후원 금액 관리, owner 출금 처리 등을 한다.
- 커피 후원 기능
  ```
  function buyCoffee(string calldata message) external payable => payable 덕에 ETH 받기 가능

  require(msg.value > 0) => 0ETH 후원 방지

  totalDonationAmount += msg.value; => 누적 후원 증가
  ```
- 후원 기록 저장 : 누가 후원했는지, 얼마 보냈는지, 메시지, 시간 등이 저장됨
  ```
  struct Donation {
    address donor;
    uint256 amount;
    string message;
    uint256 timestamp;
  }
  ```
- 후원 내역 배열 관리
  ```
  Donation[] private donations; => 후원 들어올 때마다 배열에 추가되어 HTML에서 후원 내역 목록 출력 가능
  ```
- owner(deploy한 Metamask 주소가 owner) 저장 : 컨트랙트를 배포한 사람 주소를 저장하고, deploy한 MetaMask 주소가 owner가 됨.
  ```
  address pulic owner;

  constructor(){
    owner = msg.sender;
  }
  ```
- 이벤트 발생
  ```
  event Donated(...) => 후원 발생 시 블록체인 로그 기록. html에서 추적 가능.
  ```
- 후원 내역 조회
  ```
  function getDonations() => html이 이를 호출하여 후원 목록 테이블 출력함
  ```
- 컨트랙트 잔액 조회
  ```
  function getBalance() => 현재 스마트컨트랙트 안에 들어있는 ETH 반환
  ```
- 출금 기능
  ```
  function withdraw()

  require(msg.sender == owner) => owner만 실행 가능

  payable(owner).transfer(balance); => 컨트랙트 안 ETH를 owner의 지갑으로 전송
  ```

Dapp_BuyMeACoffee.html : 사용자 화면(UI/프론트앤드) 역할을 수행한다.

## Process - 1번 : Nodit Console
1. 회원가입 후 API Key를 확인한다.
<img width="947" height="871" alt="1" src="https://github.com/user-attachments/assets/0b06942b-b420-4971-82c1-b42959504f17" />


## Process - 2번 : GIWA 연동
1. 'Process - 1번'에서 확인한 API Key를 이용하여 MetaMask 내의 GIWA Sepolia Testnet을 구성한다.
2. API Key는 Default RPC URL에서 giwa-sepolia.nodit.io/ 뒤에 복사붙여넣기 하면 된다.
<img width="366" height="597" alt="2-2" src="https://github.com/user-attachments/assets/cd28adaa-ef9a-4c3c-8596-074cdbaf0f3c" />
3. 아래의 사진처럼 https://faucet.lambda256.io/giwa-sepolia에 들어가서 faucet을 받는다.
<img width="958" height="813" alt="2-1" src="https://github.com/user-attachments/assets/96575025-5486-4249-a910-060754823e41" />


## Process - 4번 : 나만의 Dapp 만들기
1. BuyMeACoffee.sol을 compile하고 deploy한다. 이때 Deploy & Run transactions -> Environment에서 WalletConnect(MetaMask)로 수정한다.
<img width="387" height="610" alt="deploy" src="https://github.com/user-attachments/assets/5a3e5b78-acae-402a-a172-7076b01d4620" />
<img width="348" height="388" alt="4-deployed contract" src="https://github.com/user-attachments/assets/15368598-a5e5-4433-a554-ba555766c299" />
2. deploy해서 뜬 컨트랙트 주소를 복사한다.
   
3. 컨트랙트 주소와 BuyMeACoffee.sol의 Solidity Compiler -> Comilation Details에서 ABI 정보를 복사하여 html의 CONTRACT_ADDRESS, CONTRACT_ABI에 넣어준다. (업로드된 html은 이것들이 이미 넣어진 상태이다.)
<img width="733" height="876" alt="4-copyABI" src="https://github.com/user-attachments/assets/aaa42d5e-f6ef-4e9a-984b-47c8ed6d52cd" />
4. Dapp_BuyMeACoffee.html을 vscode의 Open With Live Server로 실행한다.

## 실행결과 : 
1. MetaMask 지갑 연결 - MetaMask 지갑을 연결한다. 연결되면 연결 주소가 뜨고, 추가적으로 연결 주소가 Owner일 경우 Owner의 주소와 출금이 활성화된다. 아래 예시는 Owner의 지갑이 연결되었기 때문에 컨트랙트 잔액 출금이 활성화된 모습이다.
<img width="875" height="888" alt="image" src="https://github.com/user-attachments/assets/139c8871-6d22-479f-87bb-33c1afe51940" />
2. ETH send - 0.001ETH, 0.005ETH, 0.01ETH의 옵션으로 메시지를 입력하고, Coffee 후원을 할 수 있다. 후원 완료 시 아래와 같이 TX해시가 출력된다.
<img width="828" height="601" alt="4-jan" src="https://github.com/user-attachments/assets/056976a2-2ad6-435b-b6b7-fc0486794f65" />
3. 후원내역 - 후원자의 지갑주소, 금액, 메시지, 시간 등을 확인할 수 있다.
<img width="820" height="546" alt="4-naeyuck" src="https://github.com/user-attachments/assets/31e679f2-f6ce-49a0-bfe1-51e627b13d42" />
4. 컨트랙트 잔액 송금
   아래는 커피 후원으로 지갑에서 ETH가 빠져나간 상태이다.
   <img width="807" height="535" alt="4-beforemeta" src="https://github.com/user-attachments/assets/a41ae08a-abef-4480-8979-f78d24de9b1b" />
   이때 컨트랙트 잔액 송금 클릭 시 출금이 완료되었다고 뜬다.
   <img width="839" height="428" alt="4-chulgeumcomplete" src="https://github.com/user-attachments/assets/33ff041d-6fb2-4d80-bcc8-e6de299022f3" />
   그리고 다시 지갑을 확인하면 컨트랙트에 쌓였던 ETH가 전부 들어와 있는 모습을 볼 수 있다.
   <img width="816" height="536" alt="4-aftermeta" src="https://github.com/user-attachments/assets/f7fdf284-2b62-4e81-a185-87f96cc6f0a8" />

