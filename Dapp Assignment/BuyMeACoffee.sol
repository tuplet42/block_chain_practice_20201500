// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

contract BuyMeACoffeeV2 {
    address public owner;
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

    constructor() {
        owner = msg.sender;
    }

    function buyCoffee(string calldata message) external payable {
        require(msg.value > 0, "Donation must be greater than 0");
        require(bytes(message).length <= 100, "Message is too long");

        donations.push(Donation({
            donor: msg.sender,
            amount: msg.value,
            message: message,
            timestamp: block.timestamp
        }));

        totalDonationAmount += msg.value;
        emit Donated(msg.sender, msg.value, message, block.timestamp);
    }

    function getDonations() external view returns (Donation[] memory) {
        return donations;
    }

    function getDonationCount() external view returns (uint256) {
        return donations.length;
    }

    function getBalance() external view returns (uint256) {
        return address(this).balance;
    }

    function withdraw() external {
        require(msg.sender == owner, "Only owner can withdraw");
        uint256 balance = address(this).balance;
        require(balance > 0, "No balance to withdraw");

        payable(owner).transfer(balance);
        emit Withdrawn(owner, balance);
    }
}
