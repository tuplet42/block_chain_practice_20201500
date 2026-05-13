// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

contract SimpleDAO_Guard {
    mapping(address => uint) public balances;
    bool private locked;

    modifier noReentrant() {
        require(!locked, "No reentrancy");
        locked = true;
        _;
        locked = false;
    }

    function deposit() public payable {
        balances[msg.sender] += msg.value;
    }

    function withdraw(uint amount) public noReentrant {
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