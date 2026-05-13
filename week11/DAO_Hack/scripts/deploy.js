const hre = require("hardhat");

async function main() {

    const DAO = await hre.ethers.getContractFactory("SimpleDAO");
    const dao = await DAO.deploy();

    await dao.waitForDeployment();

    console.log("DAO deployed to:", await dao.getAddress());

    // DAO에 10 ETH 넣기
    await dao.deposit({
        value: hre.ethers.parseEther("10")
    });

    console.log("DAO funded with 10 ETH");

    const Attack = await hre.ethers.getContractFactory("AttackDAO");

    const attack = await Attack.deploy(await dao.getAddress());

    await attack.waitForDeployment();

    console.log("Attack contract:", await attack.getAddress());
}

main().catch((error) => {
    console.error(error);
    process.exitCode = 1;
});