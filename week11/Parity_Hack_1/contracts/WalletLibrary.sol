// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

contract WalletLibrary {
    address public owner;
    uint public required;

    function initWallet(address _owner, uint _required) public {
        owner = _owner;
        required = _required;
    }

    function execute(address payable to, uint amount) public {
        require(msg.sender == owner, "Not owner");

        (bool success, ) = to.call{value: amount}("");
        require(success, "Transfer failed");
    }
}