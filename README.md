## Note Mar 20, 2017:

TorCoin was my undergraduate senior thesis at Yale, co-authored with Mainak Ghosh (fellow undergraduate), Bryan Ford (professor advisor, now teaching at EPFL), and Rob Jansen (US Naval Research Laboratory).

Given the time-frame of a senior thesis (one semester), our research was focused on developing the theoretical framework for TorCoin. Unfortunately there is no working implementation of its code.

You can view the links to the research at the Yale or Navy websites:

http://dedis.cs.yale.edu/dissent/papers/hotpets14-torpath-abs
www.nrl.navy.mil/itd/chacs/ghosh-torpath-torcoin-proof-bandwidth-altcoins-compensating-relays

You can also view the presentation Mainak and I gave at HotPETS (Hot topics in Privacy Enhancing Technologies) Amsterdam 2014:

https://www.slideshare.net/MilesRichardson/torcoinslides

## Abstract

The Tor network relies on volunteer relay operators for relay bandwidth, which may limit its growth and scaling potential. We propose an incentive scheme for Tor relying on two novel concepts. We introduce TorCoin, an “altcoin” that uses the Bitcoin protocol to reward relays for contributing bandwidth. Relays “mine” TorCoins, then sell them for cash on any existing altcoin exchange. To verify that a given TorCoin represents actual bandwidth transferred, we introduce TorPath, a decentralized protocol for forming Tor circuits such that each circuit is privately-addressable but publicly verifiable. Each circuit’s participants may then collectively mine a limited number of TorCoins, in proportion to the end-to-end transmission goodput they measure on that circuit.

## (old readme follows, this was originally for Mainak and I to store latex files)

WHAT THIS IS
====

This is the repository to hold all work related to TorCoin research, specificially research done during CS 490 by Miles and Mainak.

CS 490
------

Mainak and Miles

Original Proposal:

- [Shortened, markdown version](spec.md)
- [PDF version](OfficialProposal.pdf)
- [Google Docs](https://docs.google.com/document/d/1Q9BODmfSHf9TJqxv-8Ya8z0nykU30kZ4bCg3mHkauTg/edit?usp=sharing)
