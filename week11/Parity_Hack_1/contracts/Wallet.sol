// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

contract Wallet {
    address public owner;
    uint public required;
    address public libraryAddress;

    constructor(address _libraryAddress) payable {
        libraryAddress = _libraryAddress;
    }

    receive() external payable {}

    fallback() external payable {
        (bool success, ) = libraryAddress.delegatecall(msg.data);
        require(success, "Delegatecall failed");
    }

    function getBalance() public view returns (uint) {
        return address(this).balance;
    }
}