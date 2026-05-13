const hre = require("hardhat");

async function main() {
  const DAO = await hre.ethers.getContractFactory("SimpleDAO_CEI");
  const dao = await DAO.deploy();
  await dao.waitForDeployment();

  console.log("CEI DAO deployed to:", await dao.getAddress());

  await dao.deposit({
    value: hre.ethers.parseEther("10")
  });

  console.log("CEI DAO funded with 10 ETH");

  const Attack = await hre.ethers.getContractFactory("AttackDAO");
  const attack = await Attack.deploy(await dao.getAddress());
  await attack.waitForDeployment();

  console.log("Attack contract:", await attack.getAddress());

  console.log(
    "Before attack DAO balance:",
    hre.ethers.formatEther(await dao.getBalance()),
    "ETH"
  );

  try {
    const tx = await attack.attack({
      value: hre.ethers.parseEther("1")
    });
    await tx.wait();
  } catch (err) {
    console.log("Attack failed as expected");
  }

  console.log(
    "After attack DAO balance:",
    hre.ethers.formatEther(await dao.getBalance()),
    "ETH"
  );

  const attackBalance = await hre.ethers.provider.getBalance(await attack.getAddress());
  console.log("Attack contract balance:", hre.ethers.formatEther(attackBalance), "ETH");
}

main().catch((error) => {
  console.error(error);
  process.exitCode = 1;
});