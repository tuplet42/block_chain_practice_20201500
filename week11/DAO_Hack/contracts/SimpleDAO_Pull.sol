// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

contract SimpleDAO_Pull {
    mapping(address => uint) public balances;
    mapping(address => uint) public pendingWithdrawals;

    function deposit() public payable {
        balances[msg.sender] += msg.value;
    }

    function requestWithdraw(uint amount) public {
        require(balances[msg.sender] >= amount, "Not enough balance");

        balances[msg.sender] -= amount;
        pendingWithdrawals[msg.sender] += amount;
    }

    function claim() public {
        uint amount = pendingWithdrawals[msg.sender];
        require(amount > 0, "Nothing to claim");

        pendingWithdrawals[msg.sender] = 0;

        (bool success, ) = msg.sender.call{value: amount}("");
        require(success, "Transfer failed");
    }

    function getBalance() public view returns(uint) {
        return address(this).balance;
    }
}