# Week2 - Ethereum RPC Practice

## Project Description
This project demonstrates two different ways to retrieve Ethereum blockchain data using Infura:

1. **Raw JSON-RPC** – Directly sending JSON-RPC requests to an Ethereum node.
2. **ethers.js** – Using the ethers.js library to interact with the Ethereum network.

Both programs retrieve:
- The **latest Ethereum block number**
- The **number of transactions in the latest block**

The goal of this project is to compare low-level JSON-RPC calls with a higher-level library approach.

---

## Project Structure
```
week2
├─ ethers
│ └─ index.js
│
├─ json-rpc
│ └─ index.js
│
├─ .env.example
├─ .gitignore
├─ package.json
└─ package-lock.json
```

## Install Dependences
1. Install Node.js if it is not installed.
2. Install required dependences:
    - npm init -y
    - npm install dotenv ethers

## How to setup .env file
Create a `.env` file in the project root directory and add your Infura API key.
Sign in for Infura is necessary to get API key if you didn't sign up.

## How to Run Each Program
node json-rpc/index.js
: This program directly sends JSON-RPC requests to the Ethereum network using Infura.

node ethers/index.js
: This program uses the ethers.js library to retrieve the latest block number and the number of transactions in the latest block.
