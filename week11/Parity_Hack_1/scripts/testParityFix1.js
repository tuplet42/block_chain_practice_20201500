const hre = require("hardhat");

async function main() {
  const [deployer, legitOwner, attacker] = await hre.ethers.getSigners();

  const Library = await hre.ethers.getContractFactory("FixedWalletLibrary");
  const library = await Library.deploy();
  await library.waitForDeployment();

  const libraryAddress = await library.getAddress();
  console.log("FixedWalletLibrary deployed to:", libraryAddress);

  const Wallet = await hre.ethers.getContractFactory("FixedWallet");

  const wallet = await Wallet.deploy(libraryAddress, {
    value: hre.ethers.parseEther("3")
  });
  await wallet.waitForDeployment();

  const walletAddress = await wallet.getAddress();
  console.log("FixedWallet deployed to:", walletAddress);

  const walletAsLibrary = await hre.ethers.getContractAt("FixedWalletLibrary", walletAddress);

  await walletAsLibrary.connect(legitOwner).initWallet(legitOwner.address, 1);
  console.log("Wallet initialized by legit owner");

  console.log("Owner after legit init:", await walletAsLibrary.owner());

  try {
    await walletAsLibrary.connect(attacker).initWallet(attacker.address, 1);
    console.log("Unexpected: attacker re-initialized wallet");
  } catch (err) {
    console.log("Attack failed as expected: cannot re-initialize");
  }

  console.log("Owner after attacker attempt:", await walletAsLibrary.owner());

  console.log(
    "Wallet balance:",
    hre.ethers.formatEther(await wallet.getBalance()),
    "ETH"
  );
}

main().catch((error) => {
  console.error(error);
  process.exitCode = 1;
});