# StakeOptimiser   

StakeOptimiser is a tool to enable users to increase decentralisation of stake on Cosmos-based networks.  
You can try it at: https://stake-optimise.vercel.app/  

1- The user connects to the tool with the Keplr wallet  
2- Enter the amount to stake and request an optimisation  
3- We split the delegation between validators, depending on their current stake and the user's target staking amount, to maximize the decentralisation ratio of the network  
4- The user can then execute the staking transaction and send its stake to multiple validators at once 

This tool currently only supports the Cosmoshub testnet

This project was created as a submission for the [AEZ Boost hackaton on DoraHacks](https://dorahacks.io/hackathon/aez-boost/buidl)  


## Motivation  

In Proof of Stake (PoS) cryptocurrency networks, it's crucial to evenly distribute stakes among validators for several key reasons:  
- Security: A balanced stake distribution reduces the risk of centralization, enhancing network security.  
- Decentralization: Equal stakes support the network's goal of avoiding control by a single entity or small group.  
- Preventing Cartels: Balanced stakes discourage validator cartels that can undermine fair competition.  
- Incentives: Equal distribution encourages more validators to participate, increasing network resilience.  
- Resilience: A balanced distribution makes the network more resistant to targeted attacks.  
- Trustworthiness: Users trust networks that distribute stakes fairly, fostering user confidence.  

StakeOptimizer helps strengthen the network by splitting your delegations between validators to approach an equal staking value for all validators.


## Usage    

### Online Demo  

An online version is available for Cosmos Hub testnet: https://stake-optimise.vercel.app/  

### Run locally  

This tool makes use of Vercel cloud functions written on python, so you need the Vercel client and Python installed  

1- Clone this repository  
2- Install js dependencies (pnpm install) and python dependencies 
3- Run the app (pnpm vercel dev)  
4- Open "http://localhost:3000/"   
5- Connect your wallet   
6- Choose an amount to stake    
7- Click "Optimize Stake". The validators which will receive a stake will be listed on the right and the new decentralization ratio will be displayed  
8- Click on "Execute Stake" to send the staking messages.  


## Improvements and Issues  

- Support more networks     
- Add more control over parameters (minimum stake allocation, include commission rate in the optimization, avoid previously slashed validators...)   
- UI improvements   