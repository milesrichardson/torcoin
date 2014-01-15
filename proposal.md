# Two Proposals

I have been kicking around two proposals in my head, and would be interested in working on either one. I'm curious to hear your thoughts.

---

## 1. Monetize Tor nodes with Bitcoin

This is a new problem that we have not previously discussed, but I think it's a really cool idea and could potentially be brought to market.

### Problem Statement

- Problem with Tor network is **slow speeds**
- Tor network is **oversubscribed**
- As network grows, it requires more and **faster exit nodes**
- Exit nodes are **expensive to run**, especially on dedicated hardware
- Exit node operators assume economic and possibly legal **risk**, but see **little reward**

### Research Question

Can we use Bitcoin to incentivize server operators to contribute servers to the Tor network?

### Prior Research

Not research, but people have thought of this idea before:

- [bitcointalk](https://bitcointalk.org/index.php?topic=62107.20)
- [reddit thread](http://www.reddit.com/r/Bitcoin/comments/1f97um/what_about_a_torcoin_that_would_help_secure_and/)

Distributed market:

- "A Distributed Market Framework for Large-scale Resource Sharing"
    - [http://www.comp.nus.edu.sg/~teoym/pub/10/europar2010.pdf](http://www.comp.nus.edu.sg/~teoym/pub/10/europar2010.pdf)


### The Problem

- Proof of Work
    - How does a Tor operator prove data transfer?
    - [Blind Signature?](http://en.wikipedia.org/wiki/Blind_signature)

### Overview of Proposed Solution

I have not thought too much about this.

- Private Tor network of nodes participating in market
- Each node has different role
- Software would be layer on top of current Tor implementation
	- Client
	- Host
	- Should be no need to modify underlying Tor software
- Must be easily deployable in datacenters
- This is an appealing proposition because it's an easy way for server operators to get bitcoin without paying directly for it


---

## 2. Auction Based Tor Bridge Distribution

This is the original problem I talked to you about researching. 

### Problem Statement

- Anonymity often requires conneting to specific network with specific address
	- e.g. Tor network requires connecting through bridge server
- State censors and ISPs can block connections to specific addresses
- Functional anonymity network requires distribution of bridges
- Simple distribution schemes reveal addresses to state censors and ISPs
- Revealing address of bridge = death of bridge

### Research Question

Can we improve upon prior research to find a way of distributing bridges to maximize network integrity?

### Prior Research

- rBridge: User Reputation based Tor Bridge Distribution with Privacy Preservation
	- [http://www-users.cs.umn.edu/~hopper/rbridge_ndss13.pdf](http://www-users.cs.umn.edu/~hopper/rbridge_ndss13.pdf)
- Proximax: A Measurement Based System for Proxies Dissemination
	- [http://cseweb.ucsd.edu/~klevchen/mml-fc11.pdf](http://cseweb.ucsd.edu/~klevchen/mml-fc11.pdf)

### Overview of Proposed Solution

Auction Based Tor Bridge Distribution. This is a rough brain-dump of my thoughts so far.

Terminology:

- Node = system participant
- Object = tor bridge
- Value = f(object)
- Trust = f(node)

"Marketplace for Trust and Value"

- Trust = currency
- Value = bridge node quality
- More trust buys higher quality objects
- High quality objects visible only to high trust nodes
- Object quality increases with time

Node Behavior

- Every node has pricing function given a certain object
- Every node has portfolio of objects (limited number -- how to limit?)
- Node goal is to increase average object value in portfolio
- When node receives object
	- if price_func(obj) < avg_price(portfolio):
		- hold_auction(obj)
	- else:
		- hold_auction(min(portfolio))

Auction

- Any node can hold an auction
- Every node can participate in any auction
- Currency of auction is trust, which nodes build by holding objects for long time
- All participants can see properties of object for auction
	- e.g. for tor bridges: speed, uptime
- Multiple nodes can win auction
		
Trust

- Nodes gain trust by holding high value objects for a long time

Misc

- Object maintains list of nodes that have owned it
- Objects can have multiple owners