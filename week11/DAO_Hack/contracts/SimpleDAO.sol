// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

contract SimpleDAO {
    mapping(address => uint) public balances;

    // ETH 입금
    function deposit() public payable {
        balances[msg.sender] += msg.value;
    }

    // 취약한 withdraw 함수
    function withdraw(uint amount) public {
        require(balances[msg.sender] >= amount, "Not enough balance");

        (bool success, ) = msg.sender.call{value: amount}("");
        require(success, "Transfer failed");

        unchecked {
            balances[msg.sender] -= amount;
        }
    }

    function getBalance() public view returns(uint) {
        return address(this).balance;
    }
}