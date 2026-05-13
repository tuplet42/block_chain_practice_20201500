const hre = require("hardhat");

async function main() {
  const DAO = await hre.ethers.getContractFactory("SimpleDAO_Pull");
  const dao = await DAO.deploy();
  await dao.waitForDeployment();

  console.log("Pull DAO deployed to:", await dao.getAddress());

  await dao.deposit({
    value: hre.ethers.parseEther("10")
  });

  console.log("Pull DAO funded with 10 ETH");

  console.log(
    "Before request DAO balance:",
    hre.ethers.formatEther(await dao.getBalance()),
    "ETH"
  );

  await dao.requestWithdraw(hre.ethers.parseEther("1"));

  console.log("Withdraw requested: 1 ETH");

  console.log(
    "After request DAO balance:",
    hre.ethers.formatEther(await dao.getBalance()),
    "ETH"
  );

  await dao.claim();

  console.log("Claimed 1 ETH");

  console.log(
    "After claim DAO balance:",
    hre.ethers.formatEther(await dao.getBalance()),
    "ETH"
  );
}

main().catch((error) => {
  console.error(error);
  process.exitCode = 1;
});