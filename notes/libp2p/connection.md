# Connection

我们以libp2p官方的[例子](https://github.com/libp2p/go-libp2p-examples)为例，看看libp2p中，两个peer的连接实现。

我们在例子中，参考`chat-with-rendezvous`的例子来做研究。先上例子代码：

```go
var logger = log.Logger("rendezvous")

func handleStream(stream network.Stream) {
	logger.Info("Got a new stream!")

	// Create a buffer stream for non blocking read and write.
	rw := bufio.NewReadWriter(bufio.NewReader(stream), bufio.NewWriter(stream))

	go readData(rw)
	go writeData(rw)

	// 'stream' will stay open until you close it (or the other side closes it).
}

func readData(rw *bufio.ReadWriter) {
	for {
		str, err := rw.ReadString('\n')
		if err != nil {
			fmt.Println("Error reading from buffer")
			panic(err)
		}

		if str == "" {
			return
		}
		if str != "\n" {
			// Green console colour: 	\x1b[32m
			// Reset console colour: 	\x1b[0m
			fmt.Printf("\x1b[32m%s\x1b[0m> ", str)
		}

	}
}

func writeData(rw *bufio.ReadWriter) {
	stdReader := bufio.NewReader(os.Stdin)

	for {
		fmt.Print("> ")
		sendData, err := stdReader.ReadString('\n')
		if err != nil {
			fmt.Println("Error reading from stdin")
			panic(err)
		}

		_, err = rw.WriteString(fmt.Sprintf("%s\n", sendData))
		if err != nil {
			fmt.Println("Error writing to buffer")
			panic(err)
		}
		err = rw.Flush()
		if err != nil {
			fmt.Println("Error flushing buffer")
			panic(err)
		}
	}
}

func main() {
	log.SetAllLoggers(logging.WARNING)
	log.SetLogLevel("rendezvous", "info")
	help := flag.Bool("h", false, "Display Help")
	config, err := ParseFlags()
	if err != nil {
		panic(err)
	}

	if *help {
		fmt.Println("This program demonstrates a simple p2p chat application using libp2p")
		fmt.Println()
		fmt.Println("Usage: Run './chat in two different terminals. Let them connect to the bootstrap nodes, announce themselves and connect to the peers")
		flag.PrintDefaults()
		return
	}

	ctx := context.Background()

	// libp2p.New constructs a new libp2p Host. Other options can be added
	// here.
	host, err := libp2p.New(ctx,
		libp2p.ListenAddrs([]multiaddr.Multiaddr(config.ListenAddresses)...),
	)
	if err != nil {
		panic(err)
	}
	logger.Info("Host created. We are:", host.ID())
	logger.Info(host.Addrs())

	// Set a function as stream handler. This function is called when a peer
	// initiates a connection and starts a stream with this peer.
	host.SetStreamHandler(protocol.ID(config.ProtocolID), handleStream)

	// Start a DHT, for use in peer discovery. We can't just make a new DHT
	// client because we want each peer to maintain its own local copy of the
	// DHT, so that the bootstrapping node of the DHT can go down without
	// inhibiting future peer discovery.
	kademliaDHT, err := dht.New(ctx, host)
	if err != nil {
		panic(err)
	}

	// Bootstrap the DHT. In the default configuration, this spawns a Background
	// thread that will refresh the peer table every five minutes.
	logger.Debug("Bootstrapping the DHT")
	if err = kademliaDHT.Bootstrap(ctx); err != nil {
		panic(err)
	}

	// Let's connect to the bootstrap nodes first. They will tell us about the
	// other nodes in the network.
	var wg sync.WaitGroup
	for _, peerAddr := range config.BootstrapPeers {
		peerinfo, _ := peer.AddrInfoFromP2pAddr(peerAddr)
		wg.Add(1)
		go func() {
			defer wg.Done()
			if err := host.Connect(ctx, *peerinfo); err != nil {
				logger.Warning(err)
			} else {
				logger.Info("Connection established with bootstrap node:", *peerinfo)
			}
		}()
	}
	wg.Wait()

	// We use a rendezvous point "meet me here" to announce our location.
	// This is like telling your friends to meet you at the Eiffel Tower.
	logger.Info("Announcing ourselves...")
	routingDiscovery := discovery.NewRoutingDiscovery(kademliaDHT)
	discovery.Advertise(ctx, routingDiscovery, config.RendezvousString)
	logger.Debug("Successfully announced!")

	// Now, look for others who have announced
	// This is like your friend telling you the location to meet you.
	logger.Debug("Searching for other peers...")
	peerChan, err := routingDiscovery.FindPeers(ctx, config.RendezvousString)
	if err != nil {
		panic(err)
	}

	for peer := range peerChan {
		if peer.ID == host.ID() {
			continue
		}
		logger.Debug("Found peer:", peer)

		logger.Debug("Connecting to:", peer)
		stream, err := host.NewStream(ctx, peer.ID, protocol.ID(config.ProtocolID))

		if err != nil {
			logger.Warning("Connection failed:", err)
			continue
		} else {
			rw := bufio.NewReadWriter(bufio.NewReader(stream), bufio.NewWriter(stream))

			go writeData(rw)
			go readData(rw)
		}

		logger.Info("Connected to:", peer)
	}

	select {}
}
```

我们本次重点研究连接，所以先讲连接。

首先，使用`libp2p.New`函数，生成一个libp2p的node。注意，函数返回值类型是`host.Host`，这个是个`interface`，在`github.com/libp2p/go-libp2p-core/host/host.go`中声明。这儿打断一下，这个设计就是调用和实现分开的架构设计了，调用使用接口，只关心调用时能做什么，而对怎么实现的并不关心，Go项目中，处处会用到这个架构。

我们也看一下，本质上，`host.Host`是如何实现的。在`libp2p/go-libp2p/config/config.go`代码中，`NewNode`函数即为生成`host.Host`，我们可以看到，本质上，是`libp2p/go-libp2p/p2p/host/basic/basic_host.go`的`BasicHost`结构体，它实现了接口`host.Host`的所有方法，所以`BasicHost`就是`host.Host`的一种实现。

我们继续往下看，略过设置流处理函数，这个是在节点建立连接以后，数据读写的处理。

`dht.New`启动一个DHT（分布式哈希表，Distributed Hash Table），用于节点发现。TODO

`host.Connect`用来连接一个peer。这个是接口`host.Host`的一个方法，它的实现，还是要看`BasicHost`中。首先，它会解析peer的地址信息，TODO。其次，它会调用内部方法`dialPeer`。在`dialPeer`中，`c, err := h.Network().DialPeer(ctx, p)`这步，它会使用host的network来进行实际的连接，同样的，`network`也是一个接口，真实的`network`在创建host时指定的，用的是`swarm`，这样，相当于一个peer的网络处理都在`swarm`中实现了。

那`swarm`的`DialPeer`处理，在哪呢？在`libp2p/go-libp2p-swarm/swarm_dial.go`中，它会首先判断，现在要连接的那个目标节点，是不是已经在已连接的`connections`里，若有，直接返回，若没有，则尝试连接。实际的连接在这个源文件的`dial`函数中，先去找找，本地的节点是否有私钥，若有，后续连接使用私钥进行加密，若没有，则连接不加密。



`filterKnownUndialables` 返回过滤后的可去连接节点，然后使用`dialAddrs`函数去连接。

讲到filter，貌似有个`libp2p/go-maddr-filter/filter.go`，里面有对filter的一些定义。增加一个filter，filter匹配时，其动作有以下几种：

```go
const (
	ActionNone Action = iota // zero value.
	ActionAccept
	ActionDeny
)
```

即啥都不做、接受、拒绝。

还有`AddFilter`和`Remove`的接口，都是以ip地址为唯一标识的。

`swarm`增加`Filter`的函数是`AddAddrFilter`，通过将一个`multiaddr`添加，解析其`IPNet`，加入Deny 的Filters中。

这么回头看的话，在`libp2p/go-libp2p/config/config.go`中`NewNode`时，就已经有对`swarm`的filters的设置了。--！

```go
	// TODO: Make the swarm implementation configurable.
	swrm := swarm.NewSwarm(ctx, pid, cfg.Peerstore, cfg.Reporter)
	if cfg.Filters != nil {
		swrm.Filters = cfg.Filters
	}

	h, err := bhost.NewHost(ctx, swrm, &bhost.HostOpts{
		ConnManager:  cfg.ConnManager,
		AddrsFactory: cfg.AddrsFactory,
		NATManager:   cfg.NATManager,
		EnablePing:   !cfg.DisablePing,
		UserAgent:    cfg.UserAgent,
	})
```