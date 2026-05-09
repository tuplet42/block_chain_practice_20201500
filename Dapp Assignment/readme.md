# block_chain_practice_20201500
20201500 최진우 블록체인실습 Dapp 과제입니다.

# Overall Structures : 
```
├── README.md
├── BuyMeACoffee.sol
└── Dapp_BuyMeACoffee.html
```

## 과제 의도
Stable Coin 결제 DApp을 만드는 과제였고, Nodit과 Giwa Chain 사용, 자신만의 Stable Coin과 상호작용할 수 있는 컨트랙트를 만들어야 했다.
그러다 생각난 아이디어가 개발자들이 종종 BuyMeACoffee와 같이 후원을 열어두고 있던 것이 떠올랐다.
그래서 이를 구현해보면 어떨까 생각해봤다.
GIWA Sepolia Testnet 환경에서 MetaMask를 연결하여 토큰을 이용하여 owner한테 후원을 하고, owner는 컨트랙트에 쌓인 토큰을 출금하는 것으로 구현할 수 있었다.

## 역할
BuyMeACoffeeV2.sol : Dapp의 스마트컨트랙트(백엔드) 역할. 
- MyStableCoin - 스테이블코인
  - ERC-20 토큰 생성
  - 심볼 : MSC
  - 배포자에게 1,000,000 MSC 발행
  - 사용자가 approve()로 결제 컨트랙트에 토큰 사용 권한을 줄 수 있게 함.
- BuyMeACoffeeStable - 실제 DApp의 결제/후원 컨트랙트
  - 어떤 스테이블코인을 받을지 저장
  - 사용자가 MSC로 커피 후원 가능
  - 후원자 주소, 금액, 메시지, 시간을 저장
  - 총 후원 금액 관리
  - 후원 횟수 조회
  - 컨트랙트가 보유한 MSC 잔액 조회
  - owner만 컨트랙트에 쌓인 MSC를 출금 가능
- 흐름
  -> approve로 BuyMeACoffeeStable에게 MSC 사용 허용
  -> buyCoffee 실행
  -> BuyMeACoffeeStable이 사용자 MSC를 가져감
  -> 후원 내역 저장
  -> owner가 withdraw로 쌓인 MSC 출금

Dapp_BuyMeACoffee.html : 사용자 화면(UI/프론트앤드) 역할을 수행한다.
  - MetaMask 지갑 연결
  - 다른 네트워크로 연결될 경우 대비 GIWA Sepolia 네트워크로 자동 전환
  - MyStableCoin 컨트랙트 연결
  - BuyMeACoffeeStable 컨트랙트 연결
  - 내 MSC 잔액 표시
  - 컨트랙트 MSC 잔액 표시
  - 후원 횟수 표시
  - 커피 후원 버튼 제공
  - approve() 트랜잭션 실행
  - buyCoffee() 트랜잭션 실행
  - 후원 내역 표로 출력
  - owner일 경우 출금 버튼 표시
  - withdraw() 실행

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
