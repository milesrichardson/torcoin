# TorCoin
---

Anonymous monetization of Tor using the Bitcoin protocol for payment and bandwidth monitoring verification.

Miles Richardson and Mainak Ghosh

CS 490 Project


## Problem Statement


Tor is slow. The slow speeds on the Tor network are a result of oversubscription to the network. As more users join the network without exit relay parity, bandwidth costs increase over the same number of machines, so speeds slow. As the network grows, it requires faster exit nodes. But exit nodes and bandwidth are expensive, the the Tor network is comprised of volunteers who are not compensated for providing bandwidth and computing resources.

## Proposed Solution

We will build a system that enables deployment of a secondary, monetized Tor network. Independent communities can launch a private or public network that routes traffic over Tor, but “clients” (bandwidth consumers) pay “hosts” (bandwidth providers) per bit of bandwidth. TorCoin will anonymize payments such that no host knows which client is paying him. Theoretically, this secondary network would have faster speeds than the main Tor network.


#Major Obstacles
---

## Verifiable Bandwidth Monitoring and Consensus

One of the major obstacles to implementing a reliable incentive system has been the problem of verifiably monitoring bandwidth in a scalable and anonymous manner. Since relays cannot be trusted to self-report their bandwidth contributions, we will build upon the research of Eigenspeed to determine each relay’s contribution. Our novel contribution of using the Bitcoin protocol for exchanging bandwidth and money will solve many of the decentralization problems presented by Eigenspeed.

## Coin Distribution

In general, this is a major obstacle for us, but we can solve it by either:

1. Using every nth packet as a ‘token’. These tokens are then verified using a consensus algorithm by all the neighbours of the relay in question. Thus, the more bandwidth the relay serves, the more coins they will get.

2. Using Eigenspeed as a central trusted authority. The Eigenspeed authority will distribute the coins based on its estimate of the relays in the network.

We intend to use the decentralized token distribution method as it corresponds to the Bitcoin mining model. This also reduces the need for a trusted central authority in our Tor network.


# Prior Research

Two papers address major obstacles we will face, which we addressed in the “major obstacles” section. These two papers seem the most relevant to our research. Links are in the references section.

## LIRA: Lightweight Incentivized Routing for Anonymity

Lira is a lightweight system providing “performance incentives for users to contribute bandwidth to the Tor network.” It uses coins, similar to “in game currency,” to distribute payment. Lira uses coins with tunable probability of being right, and clients can guess lottery tickets with probability, p of being right. 

Lira provides a nice base of prior research for us to build upon. We will adopt some of the work, and also improve upon it by introducing the Bitcoin protocol into the system, enabling us to gain from its advantages.


##Eigenspeed: Secure Peer-to-peer Bandwidth Evaluation

Eigenspeed is a peer-to-peer consensus building algorithm for monitoring bandwidth over a network, specifically implemented for Tor. Unfortunately it requires a central authority for computing Principal Component Analysis operations. While we believe these operations could be decentralized, we are not interested in extending Eigenspeed. Instead, we will exploit properties of the Bitcoin protocol to allow for bandwidth monitoring that is sufficient to generate payment tickets.

# Novel Contributions
---

We have two novel contributions: we exploit the bitcoin protocol for use as a bandwidth accounting mechanism, and we introduce a concept of client batching based on partially contributed randomness for resistance against Sybil attacks.

## Batching of clients

We modify the directory server to randomly group clients wishing to use the TorCoin network into batches of size n. These batches then use a consensus algorithm to derive a common relay list. For each client, the “batch” chooses a list of three relays using a decentralized random algorithm that is seeded by each client in the batch.

The batch then communicates to each relay the list of clients it is supposed to connect to.
The relays only communicate with these clients, and no other clients.
Each client now has an ordered triple of the relays it can connect to. It now proceeds to communicate using the existing Tor protocol.
	
This scheme requires small modifications to the tor directory server code (grouping clients into batches), client code (path selection algorithm), and relay servers (to accept/deny connections from certain clients). We will also need to build a separate, localized layer on top of the relay and client code for the purposes of accounting.

## Bitcoin for Bandwidth Accounting

We propose a modification of the ‘proof of work’ used in the Bitcoin protocol. Instead of cracking hashes of a given number of ciphers as proof of work to produce a coin, we will use the bandwidth transmitted by a relay. We hope to implement the monetization procedure by a direct translation of the Bitcoin protocol so that every nth packet generated by a client is a special token. When it is received by a relay, it can be converted into a coin and is added to the TorCoin blockchain, with the relay as the owner.

# Security Considerations
---

**Robustness under attack**: The initial decentralized relay selection mechanism is robust to groups of adversaries colluding to attack the network. If the adversaries control up to half the network, there is a probability of only 1/16 that an adversary client gets a path of three colluding relays. 

A separate rate-limiting mechanism can then be deployed to detect  dishonest relays  and assign them a lower weightage in the path selection procedure. An independent verification authority, such as one based on Eigenspeed, could be used to detect these discrepancies.

# Deliverables
---

1. Modified Tor client. We will wrap the existing Tor client  with a layer that generates and injects a token into the client’s packet stream at a given frequency. These tokens form the basis of the proof-of-work concept for the TorCoin protocol.
2. Modified Tor relays: We will also wrap the existing Tor relays with the packet inspection layer that can generate TorCoins in proportion to the bandwidth served by the relay.
3. TorCoin protocol: The Bitcoin protocol must be modified to accept our revised proof-of-work concept.
Division of Work
We are allocating a few blocks of hours per week when we will meet and pair-program most of the major modifications we need to make. This will give each of us a holistic understanding of the entire codebase, ensure accountability to each other, and increase productivity. We will have distinct areas of focus. Miles will focus on Tor client modifications and implementing the TorCoin protocol with the novel proof-of-work, while Mainak will focus on implementing the Tor relay selection protocol and consensus-based authorization of clients. 

#References
---

- http://cs.gmu.edu/~astavrou/research/Par_PET_2008.pdf
- http://www.ohmygodel.com/publications/lira-ndss13.pdf
- https://bitcointalk.org/index.php?topic=62107.20
- http://www.reddit.com/r/Bitcoin/comments/1f97um/- what_about_a_torcoin_that_would_help_secure_and/
- https://www.usenix.org/legacy/event/iptps09/tech/full_papers/snader/snader.pdf
- http://www.bitcloudproject.org/


