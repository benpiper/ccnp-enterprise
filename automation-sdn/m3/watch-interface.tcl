event manager applet WatchGig0/1
event syslog pattern "Line protocol on Interface GigabitEthernet0/1, changed state to down" period 1
action 1.0 cli command "enable"
action 2.0 cli command "configure terminal"
action 3.0 cli command "interface gi0/1"
action 4.0 cli command "shut"
action 5.0 cli command "no shut"
exit

#    To test:
#    R1(config)#int gi0/1
#    R1(config-if)#shut
#    R1(config-if)end
#    R1#
#    %SYS-5-CONFIG_I: Configured from console by console
#    %LINK-5-CHANGED: Interface GigabitEthernet0/1, changed state to administratively down
#    %LINEPROTO-5-UPDOWN: Line protocol on Interface GigabitEthernet0/1, changed state to down
#    %LINK-3-UPDOWN: Interface GigabitEthernet0/1, changed state to up
#    %LINEPROTO-5-UPDOWN: Line protocol on Interface GigabitEthernet0/1, changed state to up