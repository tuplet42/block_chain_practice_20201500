// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

contract Faucet {
    address payable public owner;
    uint256 public constant WITHDRAWAL_AMOUNT = 0.01 ether;
    uint256 public constant LOCK_TIME = 1 days;

    mapping(address => uint256) public lastWithdrawalTime;

    event Deposit(address indexed user, uint256 amount);
    event Withdrawal(address indexed user, uint256 amount);

    modifier onlyOwner() {
        require(msg.sender == owner, "Only the owner can call this function.");
        _;
    }

    constructor() {
        owner = payable(msg.sender);
    }

    function withdraw() external {
        require(
            block.timestamp >= lastWithdrawalTime[msg.sender] + LOCK_TIME,
            "You must wait 24 hours between withdrawals."
        );
        require(
            address(this).balance >= WITHDRAWAL_AMOUNT,
            "Insufficient balance in the faucet."
        );

        lastWithdrawalTime[msg.sender] = block.timestamp;
        payable(msg.sender).transfer(WITHDRAWAL_AMOUNT);
        emit Withdrawal(msg.sender, WITHDRAWAL_AMOUNT);
    }

    function deposit() external payable onlyOwner {
        emit Deposit(msg.sender, msg.value);
    }

    function withdrawAll() external onlyOwner {
        uint256 amount = address(this).balance;
        owner.transfer(amount);
        emit Withdrawal(owner, amount);
    }

    receive() external payable {
        emit Deposit(msg.sender, msg.value);
    }
}
