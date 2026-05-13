// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

contract FixedWalletLibrary {
    address public owner;
    uint public required;
    bool public initialized;

    function initWallet(address _owner, uint _required) public {
        require(!initialized, "Already initialized");

        owner = _owner;
        required = _required;
        initialized = true;
    }

    function execute(address payable to, uint amount) public {
        require(msg.sender == owner, "Not owner");

        (bool success, ) = to.call{value: amount}("");
        require(success, "Transfer failed");
    }
}