# libp2p

* 概述

  包含哪些方面，分别的作用以及设计目的

```
    设计考量：
    1. Transport agnostic（传输协议无关）
    2. Multi-multiplexing（多路复用）
    3. Encryption（加密）
    4. NAT traversal（NAT穿透）
    5. Relay（中继）
    6. Enable several network topologies（多种网络拓扑）
    7. Resource discovery（资源发现）
    8. Messaging（消息协议）
    
    架构：
    ┌─────────────────────────────────────────────────────────────────────────────────┐
    │                                  libp2p                                         │
    └─────────────────────────────────────────────────────────────────────────────────┘
    ┌─────────────────┐┌─────────────────┐┌──────────────────────────┐┌───────────────┐
    │   Peer Routing  ││      Swarm      ││ Distributed Record Store ││  Discovery    │
    └─────────────────┘└─────────────────┘└──────────────────────────┘└───────────────┘

    1. Peer Routing（节点路由）
        用来决定使用哪些节点来路由指定的消息。这种路由机制可以递归甚至在广播/组播模式下完成。
    2. Swarm（连接管理）
        现在叫Switch。负责管理节点之间连接的创建、维护、销毁。包括协议多路复用、流多路复用、NAT穿透和连接中继，同时进行多路传输。
    3. Distributed Record Store（分布式记录存储）
        存储和分发记录的系统，负责记录节点相关的各种信息，便于连接管理和内容寻址。
    4. Discovery（节点发现）
        发现和识别网络中的其他节点。

    内部的基础协议：
    1. identify （https://github.com/libp2p/specs/blob/master/identify/README.md）
        用来和其他节点交换私钥和地址
    2. mplex （https://github.com/libp2p/specs/blob/master/mplex/README.md）
        友好的流多路复用器
    3. plaintext （https://github.com/libp2p/specs/blob/master/plaintext/README.md）
        仅用于测试debug环境下的明文传输协议
    4. pnet（https://github.com/libp2p/specs/blob/master/pnet/Private-Networks-PSK-V1.md）
        使用预共享秘钥的私有网络
    5. pubsub（https://github.com/libp2p/specs/blob/master/pubsub/README.md）
        libp2p上的PubSub接口实现
        5.1 gossipsub（https://github.com/libp2p/specs/blob/master/pubsub/gossipsub/README.md）
            可扩展的基准PubSub协议
            5.1.1 episub（https://github.com/libp2p/specs/blob/master/pubsub/gossipsub/episub.md）
                一种基于gossipsub协议的实现
    6. relay（https://github.com/libp2p/specs/blob/master/relay/README.md）
        libp2p的电路交换（类似于TURN）
    7. rendezvous（https://github.com/libp2p/specs/blob/master/rendezvous/README.md）
        常规的节点发现协议
    8. secio（https://github.com/libp2p/specs/blob/master/secio/README.md）
        安全传输协议
    9. tls（https://github.com/libp2p/specs/blob/master/tls/tls.md）
```

* 连接认证

  是否用到了加密连接，比如TLS，用到时，如何进行TLS加密，CA证书是如何导入

  ```
    libp2p上的通信可能是：加密的、签名的、既无加密又无签名。
    它使用了TLS这样的加密模型，但并不是整个TLS。它只使用了TLS模型中用于加密的最小的一部分。（We do not use TLS directly, because we do not want the CA system baggage.
    Most TLS implementations are very big. Since the libp2p model begins with keys, libp2p only needs to apply ciphers. This is a minimal portion of the whole TLS standard.）

    https://github.com/libp2p/specs/blob/master/tls/tls.md#peer-authentication

    更准确一些，是使用libp2p自己实现的TLS，证书做了一些裁剪，如：去掉了“subjectUniqueId”和“issuerUniqueId”，还有其他别的部分。libp2p的TLS证书，包含多个“MUST” 和“MUST NOT”，以区别于普通的TLS证书。


    除了自己实现的TLS之外，还有secio（https://github.com/libp2p/go-libp2p-secio），也用来加密传输，不过这个协议（或者库）在最新的libp2p中被标记为“不推荐使用”，替代者是Noise（https://github.com/libp2p/specs/tree/master/noise）。

  
  ```

* 连接控制

  连接控制是实现的？控制的颗粒度？比如，是在启动前读取控制配置文件（如白名单或者config），还是启动后，可以动态添加连接，及认证？

  ```
  Swarm模块，主要用于连接控制。identify用于管理节点公钥和地址。暂时没有看到可以控制的配置，一般都是设置peerID之后连接的。要么是节点路由之后，Peer Discovery 连接（常见的p2p）；要么是写死对方的peerID连接（这种一般是测试目的）。

  虽然暂时没有这样的功能，不过可以通过开发，做出想要的功能。比如社区有人提出相似的问题：https://discuss.libp2p.io/t/connection-whitelisting-on-an-ongoing-basis/609
  ```

* 数据传输

  业务数据在传输时，是如何序列化的，在传输结束后，是如何反序列化的？

  ```
  libp2p不做数据的序列化和反序列化，使用时需要配合pb、json、messagepack等序列化工具。如，在应用层面，使用pb将数据序列化为字节流，放入libp2p传输，在接收端，pb将字节流反序列化为数据。
  ```

  
