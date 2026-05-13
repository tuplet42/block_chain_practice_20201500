// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

contract SimpleDAO_CEI {
    mapping(address => uint) public balances;

    function deposit() public payable {
        balances[msg.sender] += msg.value;
    }

    function withdraw(uint amount) public {
        require(balances[msg.sender] >= amount, "Not enough balance");

        // Effects: 상태 변경 먼저
        balances[msg.sender] -= amount;

        // Interactions: 외부 호출 나중
        (bool success, ) = msg.sender.call{value: amount}("");
        require(success, "Transfer failed");
    }

    function getBalance() public view returns(uint) {
        return address(this).balance;
    }
}