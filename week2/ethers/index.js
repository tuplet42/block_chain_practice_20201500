// dotenv를 사용하여 .env 파일에 저장된 환경변수를 로드
require("dotenv").config();

// ethers 라이브러리 불러오기
const { ethers } = require("ethers");

// .env 파일에서 Infura API Key 읽기
const INFURA_API_KEY = process.env.INFURA_API_KEY;

// Infura Ethereum Mainnet RPC endpoint 생성
const RPC_URL = `https://mainnet.infura.io/v3/${INFURA_API_KEY}`;

async function main() {
  try {
    // Ethereum RPC Provider 생성
    // JsonRpcProvider는 Ethereum 노드(RPC 서버)와 연결해주는 객체
    // Infura 노드를 통해 Ethereum 메인넷에 접근
    const provider = new ethers.JsonRpcProvider(RPC_URL);


    // 최신 블록 번호 조회
    // 내부적으로 JSON-RPC의 eth_blockNumber 호출
    const latestBlockNumber = await provider.getBlockNumber();

    // 최신 블록 정보 조회
    // "latest"를 전달하면 가장 최근 블록 정보를 가져옴
    // 내부적으로 JSON-RPC의 eth_getBlockByNumber 호출
    const latestBlock = await provider.getBlock("latest");


    // 트랜잭션 개수 계산
    // 블록 객체의 transactions 배열 길이가 해당 블록에 포함된 트랜잭션 개수
    const txCount = latestBlock.transactions.length;

    // 결과 출력
    console.log("=== ethers.js version ===");
    console.log("Latest block number:", latestBlockNumber);
    console.log("Transaction count in latest block:", txCount);

  } catch (error) {
    console.error("Error:", error.message);
  }
}

main();