// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

import "@openzeppelin/contracts/token/ERC20/ERC20.sol";

contract MyStableCoin is ERC20 {
    constructor() ERC20("My Stable Coin", "MSC") {
        _mint(msg.sender, 1000000 * 10 ** decimals());
    }
}

contract BuyMeACoffeeStable {
    address public owner;
    MyStableCoin public stableCoin;
    uint256 public totalDonationAmount;

    struct Donation {
        address donor;
        uint256 amount;
        string message;
        uint256 timestamp;
    }

    Donation[] private donations;

    event Donated(address indexed donor, uint256 amount, string message, uint256 timestamp);
    event Withdrawn(address indexed owner, uint256 amount);

    constructor(address _stableCoin) {
        owner = msg.sender;
        stableCoin = MyStableCoin(_stableCoin);
    }

    function buyCoffee(uint256 amount, string calldata message) external {
        require(amount > 0, "Donation must be greater than 0");
        require(bytes(message).length <= 100, "Message is too long");

        bool success = stableCoin.transferFrom(msg.sender, address(this), amount);
        require(success, "Token transfer failed");

        donations.push(Donation({
            donor: msg.sender,
            amount: amount,
            message: message,
            timestamp: block.timestamp
        }));

        totalDonationAmount += amount;

        emit Donated(msg.sender, amount, message, block.timestamp);
    }

    function getDonations() external view returns (Donation[] memory) {
        return donations;
    }

    function getDonationCount() external view returns (uint256) {
        return donations.length;
    }

    function getBalance() external view returns (uint256) {
        return stableCoin.balanceOf(address(this));
    }

    function withdraw() external {
        require(msg.sender == owner, "Only owner can withdraw");

        uint256 balance = stableCoin.balanceOf(address(this));
        require(balance > 0, "No balance to withdraw");

        bool success = stableCoin.transfer(owner, balance);
        require(success, "Withdraw failed");

        emit Withdrawn(owner, balance);
    }
}