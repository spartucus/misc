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
1. Are collator and validator same?
2. What if evil validator continue submit same one shard collation, deos LOOKAHEAD_PERIODS smaller than confirmed number, and that's the reason?
3. Proposer and executor earn gas fee, and does Collator earn gas fee too?
4. SMC(sharding manager contract) add collation to main chain (or root chain), is it or how? And if it is, what if one evil man call SMC in a infinite loop and make SMC busy so others can't do anything?
