"""Reproducible x86 ILP experiments with a parameterized O3 pipeline."""
import argparse
import m5
from m5.objects import *
p=argparse.ArgumentParser()
p.add_argument('--binary',required=True)
p.add_argument('--mode',default='integer')
p.add_argument('--width',type=int,default=1)
p.add_argument('--predictor',choices=['local','tournament','none'],default='local')
p.add_argument('--threads',type=int,default=1)
a=p.parse_args()
s=System()
s.multi_thread=a.threads>1
s.clk_domain=SrcClockDomain(clock='2GHz',voltage_domain=VoltageDomain(voltage='1V'))
s.mem_mode='timing'; s.mem_ranges=[AddrRange('512MB')]
s.cpu=X86O3CPU(numThreads=a.threads)
for field in ['fetchWidth','decodeWidth','renameWidth','dispatchWidth','issueWidth','wbWidth','commitWidth']:
    setattr(s.cpu,field,a.width)
direction=LocalBP() if a.predictor=='local' else (TournamentBP() if a.predictor=='tournament' else NoDirectionPrediction())
s.cpu.branchPred=BranchPredictor(conditionalBranchPred=direction)
s.cpu.numROBEntries=128
s.cpu.forwardComSize=64; s.cpu.backComSize=64
s.membus=SystemXBar()
s.cpu.icache=Cache(size='16kB',assoc=2,tag_latency=1,data_latency=1,response_latency=1,mshrs=4,tgts_per_mshr=20)
s.cpu.dcache=Cache(size='16kB',assoc=2,tag_latency=1,data_latency=1,response_latency=1,mshrs=4,tgts_per_mshr=20)
s.cpu.icache_port=s.cpu.icache.cpu_side; s.cpu.dcache_port=s.cpu.dcache.cpu_side
s.cpu.icache.mem_side=s.membus.cpu_side_ports; s.cpu.dcache.mem_side=s.membus.cpu_side_ports
s.cpu.createInterruptController()
for interrupt in s.cpu.interrupts:
    interrupt.pio=s.membus.mem_side_ports
    interrupt.int_requestor=s.membus.cpu_side_ports
    interrupt.int_responder=s.membus.mem_side_ports
s.cpu.mmu.connectWalkerPorts(s.membus.cpu_side_ports,s.membus.cpu_side_ports)
s.mem=SimpleMemory(range=s.mem_ranges[0],latency='50ns',bandwidth='4GiB/s')
s.mem.port=s.membus.mem_side_ports; s.system_port=s.membus.cpu_side_ports
s.workload=SEWorkload.init_compatible(a.binary)
s.cpu.workload=[Process(pid=100+i,cmd=[a.binary,a.mode]) for i in range(a.threads)]
s.cpu.createThreads()
root=Root(full_system=False,system=s)
m5.instantiate(); event=m5.simulate()
print('Exit tick',m5.curTick(),event.getCause())
