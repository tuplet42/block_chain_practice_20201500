// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

interface IERC20 {
    function transferFrom(address from, address to, uint amount) external returns (bool);
    function transfer(address to, uint amount) external returns (bool);
    function balanceOf(address account) external view returns (uint);
}

contract Staking {
    IERC20 public token;

    mapping(address => uint) public stakedBalance;

    constructor(address _token) {
        token = IERC20(_token);
    }

    // stake tokens
    function stake(uint amount) external {
        require(amount > 0, "Amount must be > 0");

        bool success = token.transferFrom(msg.sender, address(this), amount);
        require(success, "Transfer failed");

        stakedBalance[msg.sender] += amount;
    }

    // withdraw staked tokens
    function withdraw(uint amount) external {
        require(amount > 0, "Amount must be > 0");
        require(stakedBalance[msg.sender] >= amount, "Not enough staked");

        stakedBalance[msg.sender] -= amount;

        bool success = token.transfer(msg.sender, amount);
        require(success, "Transfer failed");
    }

    // check balance
    function getStakedBalance(address user) external view returns (uint) {
        return stakedBalance[user];
    }
}
