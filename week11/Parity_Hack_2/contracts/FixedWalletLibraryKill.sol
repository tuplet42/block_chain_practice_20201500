// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

contract FixedWalletLibraryKill {
    address public owner;
    uint public required;
    bool public initialized;

    modifier onlyOwner() {
        require(msg.sender == owner, "Not owner");
        _;
    }

    function initWallet(address _owner, uint _required) public {
        require(!initialized, "Already initialized");

        owner = _owner;
        required = _required;
        initialized = true;
    }

    function execute(address payable to, uint amount) public onlyOwner {
        (bool success, ) = to.call{value: amount}("");
        require(success, "Transfer failed");
    }

    // selfdestruct 제거
}