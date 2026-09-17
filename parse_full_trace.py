from pathlib import Path
import gzip,json
base=Path(__file__).parent;folder=base/'results/ilp/full_trace'
path=folder/'trace.out.gz'
groups={};record=None;micro_count=0;micro_total=0
with gzip.open(path,'rt') as source:
 for line in source:
  a=line.rstrip().split(':')
  if len(a)<3:continue
  if a[1]=='fetch':
   record={'fetch':int(a[2]),'pc':a[3],'micro_pc':int(a[4]),'seq':int(a[5])}
  elif record is not None and a[1]=='retire':
   tick=int(a[2]);key=(record['pc'],record['seq']-record['micro_pc'])
   if tick>0:
    g=groups.setdefault(key,{'fetch':record['fetch'],'retire':tick,'indices':[]})
    g['fetch']=min(g['fetch'],record['fetch']);g['retire']=max(g['retire'],tick);g['indices'].append(record['micro_pc'])
    micro_count+=1;micro_total+=(tick-record['fetch'])/500
   record=None
valid=[]
for g in groups.values():
 indices=sorted(g['indices'])
 if indices==list(range(len(indices))):valid.append(g)
data={'retired_microops':micro_count,'microop_mean_fetch_to_retire_cycles':micro_total/micro_count,'architectural_groups':len(valid),'all_groups':len(groups),'mean_group_fetch_to_last_retire_cycles':sum((g['retire']-g['fetch'])/500 for g in valid)/len(valid),'method':'Group by PC and (sequence number minus micro-PC); require contiguous micro-PCs from zero; compare group count with simInsts before treating groups as complete architectural instructions.'}
(base/'Saved_Assignments/Full_Trace_Summary.json').write_text(json.dumps(data,indent=2));print(json.dumps(data,indent=2))
