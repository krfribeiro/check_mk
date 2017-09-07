This Check_MK plugin monitors health on Cisco Nexus Fibre Channel Switches

It will only be critical based on 5 conditions.
If the Link Failure counter exceeds one.
If the Sync Losses counter exceeds one.
If the Link Reset Ins counter exceeds one.
If the Link Reset Outs counter exceeds one.
Or, if the link is down.

It retreives the following PerfData :
(At the time, this won't be considered for critical or warning conditions - perhaps in the future)

inOctets and outOctets          
InvalidCRCs  
LinkFailures 
SyncLosses   
LinkResetIns and LinkResetOuts
TXBBFromZero 
CFramesIn and CFramesOut   
C3Discards   
FFramesIn and FFramesOut    
RXBCredits andTXBCredits

Any sugestions or developments, please share it with me so i could learn a little more!

Thanks!
