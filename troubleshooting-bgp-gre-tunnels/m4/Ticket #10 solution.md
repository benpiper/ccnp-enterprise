Ticket #10

Problem: R3 can't reach R9's loopback (2001::9). Diagnose and resolve.

*Topology analysis* R3 is in EIGRP AS 29897, and its path to R9 is via R4, which is an ABR bordering OSPF A0 and A1. R9 is in A1.

Process
===
Verify
---
```
R3#ping 2001::9 timeout 1 repeat 3
Type escape sequence to abort.
Sending 3, 100-byte ICMP Echos to 2001::9, timeout is 1 seconds:
...
Success rate is 0 percent (0/3)
```

Narrow
---
```
R3#traceroute         
Protocol [ip]: ipv6
Target IPv6 address: 2001::9
Source address: 
Insert source routing header? [no]: 
Numeric display? [no]: 
Timeout in seconds [3]: 1
Probe count [3]: 1
Minimum Time to Live [1]: 
Maximum Time to Live [30]: 4
Priority [0]: 
Port Number [0]: 
Type escape sequence to abort.
Tracing the route to 2001::9

  1 2001:9897::4 7 msec
  2 2001:14::1 51 msec
  3  * 
  4  * 
```

*IPv4 Topology* Packet seems to go from R3>R4>R1. This path is suboptimal. Rather than trying to figure out why it stops after R1, let's determine why packet doesn't go from R4 to R9.

R4:
```
R4#show ipv6 route 2001::9
Routing entry for 2001::9/128
  Known via "static", distance 1, metric 0
  Route count is 1/1, share count 0
  Routing paths:
    2001::1
      Last updated 23:02:02 ago

Static route seems to point to r1.

R4#show ipv6 route 2001::1 
Routing entry for 2001::1/128
  Known via "ospf 1", distance 110, metric 1000, type intra area
  Redistributing via eigrp 29897
  Route count is 1/1, share count 0
  Routing paths:
    FE80::F816:3EFF:FE60:4659, Tunnel14
      Last updated 23:04:16 ago

R4#show int tun14 description 
Interface                      Status         Protocol Description
Tu14                           up             up       Tunnel to R1
```

Static route points to R1, and this is wrong. Hence this is a L3 issue caused by a static route on R4. Let's locate and remove it.

```
R4#show run | i ipv6 route 
ipv6 route 2001::9/128 2001::1
R4(config)#no ipv6 route 2001::9/128 2001::1

Now check the route again
R4#show ipv6 route 2001::9
Routing entry for 2001::8/127
  Known via "ospf 1", distance 110, metric 1002, type intra area
  Redistributing via eigrp 29897
  Route count is 1/1, share count 0
  Routing paths:
    FE80::F816:3EFF:FE60:4659, Tunnel14
      Last updated 1d16h ago
```

The next hop is still R1 with a next hop of tun14. This time the route is via ospf 1 and it's an intra area route meaning that it's coming from within the OSPF area. But what OSPF area? R4 is an area border router with connections to both area 0 and area 1.  The next hop is via tunnel 14. According to the topology diagram that's in area 0. But let's double check.

```
show ipv6 ospf int br
Interface    PID   Area            Intf ID    Cost  State Nbrs F/C
Lo14         1     0               14         1     LOOP  0/0
Gi0/3        1     0               5          1     DR    0/0
Tu14         1     0               15         1000  P2P   1/1
Tu49         1     1               16         1000  P2P   1/1
```

The tun14 interface is in area 0. But 2001::9 is the loopback for R9, which sits squarely in area 1. The tun49 interface is in area 1. Let's first get the router ID of R9.

```
show ipv6 ospf nei
```

It's 9.9.9.9. Now let's look at the OSPF link state database to see what prefixes we're learning from R9.

```
show ipv6 ospf dat adv-router 9.9.9.9
```

And we've got an INTER area prefix, that's a type-3 summary LSA, in area 1. So R4 IS learning the prefix from R9. But R4 and R9 are attached in area 1. R9 should NOT be sending a type-3 summary LSA into area 1 because R9 is not an area border router. It sits squarely in area 1, or at least it should. SO R9 should be sending an INTRA area prefix LSA. Let's check R9. 


R9:
Let's check the LSDB. R9 should be advertising a INTRA area prefix LSA.

```
show ipv6 ospf dat prefix self-originate
```

And there it is, 2001::9. It's an INTRA area prefix LSA, but look at the area: Area 0. R9 should advertise this prefix into area 1. Let's check the OSPF interfaces.

```
R9#show ipv6 ospf inter br
Interface    PID   Area            Intf ID    Cost  State Nbrs F/C
Lo0          1     0               20         1     LOOP  0/0
Gi0/14       1     1               16         1     DR    0/0
Tu49         1     1               23         1000  P2P   1/1
Tu19         1     1               22         1000  P2P   1/1
```

Loopback0 is in area 0. Let's check the configuration on that.

```
show run int lo0
interface Loopback0
 ip address 9.9.9.9 255.255.255.255
 ipv6 address 2001::9/128
 ipv6 ospf 1 area 0
 ```

Let's change this to area 1.

Troubleshoot
---

```
R9(config)#int lo0
R9(config-if)#ipv6 ospf 1 area 1
```

Verify
---
Now let's check that R9's advertising the right INTRA area prefix LSA into area 1.
show ipv6 ospf dat prefix self-originate

Let's go back to R4 and see if the routing table ahs changed there.

R4:
```
R4#show ipv6 route 2001::9
Routing entry for 2001::9/128
  Known via "ospf 1", distance 110, metric 1000, type intra area
  Redistributing via eigrp 29897
  Route count is 1/1, share count 0
  Routing paths:
    FE80::9, Tunnel49
      Last updated 00:01:59 ago
```

Looks good! Let's go back to R3 and try to ping R9's loopback.

R3:
```
ping 2001::9
R3#traceroute 2001::9
Type escape sequence to abort.
Tracing the route to 2001::9

  1 2001:9897::4 8 msec 5 msec 8 msec
  2 2001:49::9 33 msec 25 msec 25 msec
```