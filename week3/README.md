# Week3 - Blockchain Lab #3
20201500 최진우 3주차 실습입니다.

## Project Description
MetaMask 지갑을 연결하고, 다른 사람의 MetaMask 지갑 주소로 송금을 하는 예제:

1. **01-connect_wallet.html** – 지급과 connect. 완료 시 지갑 주소, ETH 잔액, 현재 Nonce가 뜬다.
2. **02-send_eht.html** – 왼쪽에 자신의 지갑 주소, ETH 잔액, 현재 Nonce가 뜬다. 오른쪽에는 다른 사용자의 지갑 주소를 입력하여 Eth를 송금 가능하다. 송금되면 왼쪽의 자신의 Nonce가 올라간다.

## How to run
1. Download VSCode extension : Live Server
2. Right click the html file you want to run and click 'Open With Live Server'
---

## Project Structure
```
week3
├─ 01-connect_wallet.html # 환경설정이 끝난 후, 
├─ 02-send_eth.html
```

## Before running the html
1. 사용하는 브라우저에 MetaMask extension을 다운받는다.
2. 계정을 생성해서 지갑을 만든다.
3. 기본 브라우저를 extension으로 다운받은 브라우저로 설정한다. 그렇지 않으면 html 실행 시 metamask가 연결되지 않는 문제가 발생한다.
4. 지갑에 로그인한 상태라면 오른쪽 의 3개줄 버튼을 누르고 Manage -> Network -> 사용자 지정 네트워크 추가
   로 Base Sepolia, GIWA Sepolia를 추가한다. (이미 테스트 네트워크에 Sepolia는 있을 것이다. 만약 없다면 추가를 추천한다.)
5. 지갑 주소를 입력해서 3개 네트워크의 faucet을 받는다.
   (필자는 Spolia만 받아져서 다음의 주소로 받았다. https://cloud.google.com/application/web3/faucet/ethereum/sepolia)
6. faucet을 받았으면 01-connect_wallet.html html을 실행한 상태로 MetaMask 연결을 누른다. 
7. 실행 완료 시 02-send_eht.html을 실행시킨다. 상대의 지갑 주소와 보낼 금액을 입력하고 송금을 실행 시 완료되었다는 메시지와 함께 Nonce가 올라갈 것이다.

## Result Examples
1. 01-connect_wallet.html 결과
<img width="946" height="598" alt="result_01" src="https://github.com/user-attachments/assets/903749c1-a6a3-4477-86ff-d79bb5aaed45" />

2. 02-send_eht.html 결과
<img width="932" height="837" alt="result_02_3" src="https://github.com/user-attachments/assets/ed62131d-f903-442a-ade5-7fa07a4cfa49" />

