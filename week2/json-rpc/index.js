// dotenv 라이브러리를 사용하여 .env 파일에 있는 환경변수를 로드
require("dotenv").config();

// .env 파일에 저장된 INFURA API KEY를 읽어옴
const INFURA_API_KEY = process.env.INFURA_API_KEY;

// Infura Ethereum Mainnet RPC endpoint 생성
const RPC_URL = `https://mainnet.infura.io/v3/${INFURA_API_KEY}`;

async function main() {
  try {
    // 최신 블록 번호 조회
    // JSON-RPC 메서드: eth_blockNumber

    // Infura RPC 서버에 POST 요청을 보내 최신 블록 번호를 요청
    const blockNumberRes = await fetch(RPC_URL, {
      method: "POST",
      headers: {
        "Content-Type": "application/json", // JSON 형식 요청
      },
      body: JSON.stringify({
        jsonrpc: "2.0",            // JSON-RPC 프로토콜 버전
        id: 1,                     // 요청 ID (응답 매칭용)
        method: "eth_blockNumber", // 최신 블록 번호 조회 메서드
        params: [],                // 이 메서드는 파라미터 없음
      }),
    });

    // RPC 응답을 JSON 형태로 변환
    const blockNumberData = await blockNumberRes.json();

    // RPC 요청 중 오류가 발생했는지 확인
    if (blockNumberData.error) {
      throw new Error(blockNumberData.error.message);
    }

    // 최신 블록 번호는 16진수(hex) 문자열 형태로 반환됨
    const latestBlockHex = blockNumberData.result;

    // hex 문자열을 10진수 숫자로 변환
    const latestBlockNumber = parseInt(latestBlockHex, 16);

    // 최신 블록 정보 조회
    // JSON-RPC 메서드: eth_getBlockByNumber

    // 최신 블록 번호를 이용해 해당 블록의 상세 정보를 요청
    const blockRes = await fetch(RPC_URL, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({
        jsonrpc: "2.0",
        id: 2,
        method: "eth_getBlockByNumber", // 특정 블록 정보 조회
        params: [
          latestBlockHex, // 조회할 블록 번호 (hex 형식)
          false,          // false = transaction hash만 반환 (전체 tx 정보는 반환 안함)
        ],
      }),
    });

    // 블록 정보 응답을 JSON으로 변환
    const blockData = await blockRes.json();

    if (blockData.error) {
      throw new Error(blockData.error.message);
    }

    // 블록 안의 transactions 배열이 길이가 해당 블록에 포함된 트랜잭션 개수
    const txCount = blockData.result.transactions.length;

    // 결과 출력
    console.log("=== JSON-RPC version ===");
    console.log("Latest block number:", latestBlockNumber);
    console.log("Transaction count in latest block:", txCount);

  } catch (error) {
    console.error("Error:", error.message);
  }
}

main();