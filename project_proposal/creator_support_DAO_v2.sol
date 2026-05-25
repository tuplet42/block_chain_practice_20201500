// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

import "@openzeppelin/contracts/token/ERC20/ERC20.sol";
import "@openzeppelin/contracts/access/Ownable.sol";
import "@openzeppelin/contracts/utils/ReentrancyGuard.sol";

contract CoffeeToken is ERC20, Ownable {
    constructor() ERC20("CoffeeToken", "COFFEE") Ownable(msg.sender) {
        _mint(msg.sender, 1000000 * 10 ** decimals());
    }

    function mint(address to, uint256 amount) external onlyOwner {
        _mint(to, amount);
    }

    function burnFrom(address from, uint256 amount) external onlyOwner {
        _burn(from, amount);
    }
}

contract CreatorSupportDAO is Ownable, ReentrancyGuard {
    CoffeeToken public coffeeToken;

    uint256 public vipThreshold = 1 ether;
    uint256 public constant PROPOSAL_COST = 10 ether;

    uint256 public generalDonationBalance;
    uint256 public proposalDonationBalance;

    struct Donation {
        address donor;
        uint256 amount;
        string message;
        uint256 timestamp;
        bool forProposal;
    }

    struct Proposal {
        uint256 id;
        address proposer;
        string title;
        string description;
        uint256 yesVotes;
        uint256 noVotes;
        bool executed;
    }

    Donation[] public donations;
    Proposal[] public proposals;

    mapping(address => uint256) public totalDonated;
    mapping(uint256 => mapping(address => bool)) public voted;

    event Donated(address indexed donor, uint256 amount, string message, bool forProposal);
    event ProposalCreated(uint256 indexed proposalId, string title);
    event Voted(uint256 indexed proposalId, address indexed voter, bool support);
    event ProposalExecuted(uint256 indexed proposalId);
    event VipThresholdUpdated(uint256 oldThreshold, uint256 newThreshold);
    event GeneralWithdrawn(address indexed owner, uint256 amount);
    event ProposalFundWithdrawn(address indexed owner, uint256 proposalId, uint256 amount);

    constructor(address tokenAddress) Ownable(msg.sender) {
        coffeeToken = CoffeeToken(tokenAddress);
    }

    function setVipThreshold(uint256 newThreshold) external onlyOwner {
        require(newThreshold > 0, "Threshold must be greater than 0");
        emit VipThresholdUpdated(vipThreshold, newThreshold);
        vipThreshold = newThreshold;
    }

    function donate(string memory message) external payable nonReentrant {
        require(msg.value > 0, "Must send ETH");

        generalDonationBalance += msg.value;

        _recordDonation(msg.sender, msg.value, message, false);
    }

    function donateToProposalFund(string memory message) external payable nonReentrant {
        require(msg.value > 0, "Must send ETH");

        proposalDonationBalance += msg.value;

        _recordDonation(msg.sender, msg.value, message, true);
    }

    function _recordDonation(
        address donor,
        uint256 amount,
        string memory message,
        bool forProposal
    ) internal {
        donations.push(Donation({
            donor: donor,
            amount: amount,
            message: message,
            timestamp: block.timestamp,
            forProposal: forProposal
        }));

        totalDonated[donor] += amount;

        uint256 reward = amount * 100;
        coffeeToken.mint(donor, reward);

        emit Donated(donor, amount, message, forProposal);
    }

    function isVIP(address user) public view returns (bool) {
        return totalDonated[user] >= vipThreshold;
    }

    function createProposal(
        string memory title,
        string memory description
    ) external {
        require(isVIP(msg.sender), "Only VIP can create proposal");

        require(
            coffeeToken.balanceOf(msg.sender) >= PROPOSAL_COST,
            "Need at least 10 COFFEE"
        );

        coffeeToken.burnFrom(msg.sender, PROPOSAL_COST);

        proposals.push(Proposal({
            id: proposals.length,
            proposer: msg.sender,
            title: title,
            description: description,
            yesVotes: 0,
            noVotes: 0,
            executed: false
        }));

        emit ProposalCreated(proposals.length - 1, title);
    }

    function vote(uint256 proposalId, bool support) external {
        require(proposalId < proposals.length, "Invalid proposal");
        require(!voted[proposalId][msg.sender], "Already voted");

        require(
            coffeeToken.balanceOf(msg.sender) > 0,
            "Need CoffeeToken to vote"
        );

        voted[proposalId][msg.sender] = true;

        if (support) {
            proposals[proposalId].yesVotes += 1;
        } else {
            proposals[proposalId].noVotes += 1;
        }

        emit Voted(proposalId, msg.sender, support);
    }

    function executeProposal(uint256 proposalId) external onlyOwner {
        require(proposalId < proposals.length, "Invalid proposal");

        Proposal storage proposal = proposals[proposalId];

        require(!proposal.executed, "Already executed");
        require(proposal.yesVotes > proposal.noVotes, "Proposal rejected");

        proposal.executed = true;

        emit ProposalExecuted(proposalId);
    }

    function withdrawGeneral() external onlyOwner nonReentrant {
        uint256 amount = generalDonationBalance;
        require(amount > 0, "No general funds");

        generalDonationBalance = 0;

        (bool success, ) = payable(owner()).call{value: amount}("");
        require(success, "Transfer failed");

        emit GeneralWithdrawn(owner(), amount);
    }

    function withdrawProposalFund(uint256 proposalId) external onlyOwner nonReentrant {
        require(proposalId < proposals.length, "Invalid proposal");
        require(proposals[proposalId].executed, "Proposal not executed");

        uint256 amount = proposalDonationBalance;
        require(amount > 0, "No proposal funds");

        proposalDonationBalance = 0;

        (bool success, ) = payable(owner()).call{value: amount}("");
        require(success, "Transfer failed");

        emit ProposalFundWithdrawn(owner(), proposalId, amount);
    }

    function getDonationsCount() external view returns (uint256) {
        return donations.length;
    }

    function getProposalsCount() external view returns (uint256) {
        return proposals.length;
    }
}