# Ethereum sharding related

## Resources
1. [Sharding github](https://github.com/ethereum/sharding)
2. [Sharding FAQs](https://github.com/ethereum/wiki/wiki/Sharding-FAQs)
3. [Great article on reddit that Vbuterin post](https://www.reddit.com/r/ethereum/comments/8g1q55/vitalik_teases_sharding_release_on_twitter/dy85pq0/)
4. [以太坊扩容问题与分片（sharding）解决方案](http://www.8btc.com/sharding-finality) from 8btc.com
5. [Sharding introduction R&D compendium](https://github.com/ethereum/wiki/wiki/Sharding-introduction-R&D-compendium)
6. [Sharding roadmap](https://github.com/ethereum/wiki/wiki/Sharding-roadmap)
7. [Ethereum Sharding General Introduction](https://docs.google.com/presentation/d/1mdmmgQlRFUvznq1jdmRwkwEyQB0YON5yAg4ArxtanE4/edit#slide=id.p4) (Greate intro btw :))

## Issue tracking
1. [P2P networking](https://medium.com/@icebearhww/ethereum-sharding-workshop-in-taipei-a44c0db8b8d9) from "Recap: Ethereum Sharding Workshop in Taipei" in mid march 2018.
    > For sharding, collator shuffling requires the ability to jump between the P2P networks quickly, but the current Ethereum P2P network doesn’t support this. Thus, a new sharding network topology will be an important topic for implementation.

## Questions
1. Are collator and validator same?<br>
-- from what Vitalik Buterin [said](https://docs.google.com/presentation/d/1mGI3yyq7bq-RT3TyGFXN8bkiFdWdArM2yQzo-FMUjSY/edit#slide=id.g313dc9dd54_0_0), yes. And for three roles of proposer, collator, executor, qoute:
    > Proposers propose “collations” (think: shard blocks)<br>
    Collators approve collations and combine them into a chain<br>
    Executors calculate state<br>
    --<br>
    Proposers are shard-specific<br>
    Collators are randomly shuffled between shards<br>
    Executors are shard-specific (or possibly reshuffled infrequently)
2. What if evil validator continue submit same one shard collation, deos LOOKAHEAD_PERIODS smaller than confirmed number, and that's the reason?
3. Proposer and executor earn gas fee, and does Collator earn gas fee too?
4. SMC(sharding manager contract) add collation to main chain (or root chain), is it or how? And if it is, what if one evil man call SMC in a infinite loop and make SMC busy so others can't do anything?<br>
-- nope, strictly speaking, it's not by SMC, it's [commitee](https://github.com/ethereum/wiki/wiki/Sharding-FAQs#what-might-a-basic-design-of-a-sharded-blockchain-look-like).
    > A committee can then also check these votes from notaries and decide whether to include a collation header in the main chain, thus establishing a cross-link to the collation in the shard. Other parties may challenge the committee, notaries, proposers, validators (with Casper Proof of Stake), etc., e.g. with an interactive verification game, or by verifying a proof of validity.
