#!/usr/bin/env python3
"""Bounded constructive extraction of the selected grade-one ancestry."""
from __future__ import annotations
import argparse, bisect, hashlib, importlib.util, json, os, struct, time
from pathlib import Path
import numpy as np

ROOT=Path(__file__).resolve().parents[1]; V3_PATH=ROOT/'search/d972_r07_a0_first_rung_grade1_v3.py'
V3_SHA='bf872b30149e1351762b243d590d7a1f876e048b92a053d8f9c17bba5c45bcff'; BODY_SHA='62412762b3a208d31febb6c6b8d4707f880471ed32cf62c79c18108065ab7b5d'; BASIS_SHA='b562c980c22a25a932bae1b548f72aeede5637b9612afc908fff9a9aecff069d'; MARKER='R07_GRADE1_SELECTED_SLP_V1_CANDIDATE'
if hashlib.sha256(V3_PATH.read_bytes()).hexdigest()!=V3_SHA: raise RuntimeError('v3_hash_preimport')
sp=importlib.util.spec_from_file_location('frozen_v3',V3_PATH)
if sp is None or sp.loader is None: raise RuntimeError('v3_loader')
v3=importlib.util.module_from_spec(sp); sp.loader.exec_module(v3)
def sha(b): return hashlib.sha256(b).hexdigest()
def canon(x): return (json.dumps(x,sort_keys=True,separators=(',',':'),ensure_ascii=True)+'\n').encode('ascii')
def fail(s): raise RuntimeError(s)
def guard(t):
    if time.monotonic()-t>float(os.environ.get('TASK601_SECONDS','2400')): fail('UNKNOWN_RESOURCE:time')
    try:
        import resource
        if resource.getrusage(resource.RUSAGE_SELF).ru_maxrss*1024 > int(os.environ.get('TASK601_MAX_RSS',str(7*1024**3))): fail('UNKNOWN_RESOURCE:rss')
    except ImportError: pass
def auth_candidate(d):
    hp=d/'decision-v2.HEAD'; hr=hp.read_bytes(); h=json.loads(hr)
    if sha(hr)!='07de7a817e8c5ae2e7346402a290c32631d05b0cc621d03702faa6cb43a948c0' or h.get('body_sha256')!=BODY_SHA: fail('candidate_head')
    br=(d/f'decision-v2.{BODY_SHA}.json').read_bytes()
    if sha(br)!=BODY_SHA: fail('candidate_body')
    b=json.loads(br)
    if b.get('terminal')!='GRADE1_DECISION_MEMBER' or b.get('prepare_sha256') is None or b.get('grade_rank')!=5044 or b.get('lower_rank')!=1661 or len(b.get('member_coefficients',[]))!=3317: fail('candidate_semantics')
    if b.get('basis_receipt',{}).get('sha256')!=BASIS_SHA: fail('candidate_basis')
    basis=(d/b['basis_receipt']['file']).read_bytes(); rem=(d/b['remainder_receipt']['file']).read_bytes()
    if sha(basis)!=BASIS_SHA or sha(rem)!=b['remainder_receipt']['sha256']: fail('candidate_blob')
    return b,basis,rem
def pack_records(rows): return b''.join(struct.pack('<IBQIQI',*r) for r in rows)
def edge_bytes(edges): return b''.join(struct.pack('<HB',int(p),int(c)) for p,c in edges)
def bitset(flags):
    out=bytearray((len(flags)+7)//8)
    for i,x in enumerate(flags):
        if x: out[i//8]|=1<<(i%8)
    return bytes(out)
def write_receipt(out,name,data):
    (out/name).write_bytes(data); return {'file':name,'bytes':len(data),'sha256':sha(data)}
def main():
    ap=argparse.ArgumentParser(); ap.add_argument('--state',type=Path); ap.add_argument('--candidate',type=Path); ap.add_argument('--out',type=Path); ap.add_argument('--selftest',action='store_true'); a=ap.parse_args()
    if a.selftest:
        tiny=v3.PackedEchelon(8); coeff2=tiny.insert(np.asarray([0,2,0,0,0,0,0,0],dtype=np.uint8)); nonmono=v3.PackedEchelon(8); nonmono.insert(np.asarray([0,1,0,0,0,0,0,0],dtype=np.uint8)); nonmono.insert(np.asarray([1,0,0,0,0,0,0,0],dtype=np.uint8)); flags=[False,True,False]; edge_map=[[],[(0,1)],[]];
        for j in range(2,-1,-1):
            if flags[j]:
                for p,_ in edge_map[j]: flags[p]=True
        reverse=flags==[True,True,False]
        if not coeff2.get('accepted') or coeff2.get('scale')!=2 or nonmono.leads!=[1,0] or not reverse: raise RuntimeError('fixture_failure')
        print(json.dumps({'fixture':'PASS','coefficient_2':'PASS','nonmonotone_lead':'PASS','reverse_closure':'PASS'},sort_keys=True)); return 0
    if not a.state or not a.candidate or not a.out: fail('usage: --state STATE --candidate CANDIDATE --out OUT')
    started=time.monotonic()
    try:
        if sha(V3_PATH.read_bytes())!=V3_SHA: fail('v3_hash')
        decision,basis_blob,remainder_blob=auth_candidate(a.candidate); candidate_remainder=np.frombuffer(remainder_blob,dtype=np.uint8).copy()
        if candidate_remainder.shape != (v3.PHYSICAL_GRADE_WIDTH//4,): fail('candidate_remainder_shape')
        prepare,prepare_digest=v3.read_sealed_state(a.state,'prepare'); _,receipt=v3.load_pinned_inputs()
        v3.validate_prepare_state(a.state,prepare,receipt,fixture=False,authenticate_residual=True,authenticate_old=True,authenticate_packets=range(4))
        blocks=[v3.read_sealed_state(a.state,f'block-{i}',prepare_digest) for i in range(4)]
        for i,(body,digest) in enumerate(blocks): v3.validate_block_state(a.state,body,prepare,prepare_digest,i,authenticate_basis=True)
        if prepare_digest!=decision['prepare_sha256'] or [d for _,d in blocks]!=decision['block_sha256']: fail('parent_binding')
        if decision['residual_receipt']!=prepare['residual_blob']: fail('residual_binding')
        context=v3.context_for_state(prepare); lower=v3.PackedEchelon(v3.PHYSICAL_LOWER_WIDTH); grade=v3.PackedEchelon(v3.PHYSICAL_GRADE_WIDTH)
        lower_comp=[]; lower_nodes=[]; lower_edges=[]; grade_nodes=[]; grade_edges=[]; lower_origin_rows=[]; lower_stored_rows=[]; lower_companion_rows=[]; grade_origin_rows=[]; old_lower_zero_rows=[]; logical=0; lower_offers=grade_offers=0
        def add_lower(rem,reds,origin):
            nz=int(v3.np.flatnonzero(rem)[0]); lead=4*nz+int(v3._PACKED_FIRST[int(rem[nz])]); c=lower.coefficient(rem,lead); scale=1 if c==1 else 2; norm=rem.copy() if scale==1 else v3._PACKED_SCALE2[rem]; pivot=len(lower.rows); lower.rows.append(norm.copy()); lower.leads.append(lead); pos=bisect.bisect_left(lower._ordered_keys,(lead,pivot)); lower._ordered_keys.insert(pos,(lead,pivot)); lower.ordered_pivots.insert(pos,pivot); lower.lead_to_pivot[lead]=pivot; es=len(lower_edges); lower_edges.extend((int(p),int(q)) for p,q in reds); lower_nodes.append((int(origin),scale,es,len(reds),0,0)); return scale
        def old_route(ch,lr,og,aux,origin):
            nonlocal logical,lower_offers,grade_offers
            pl,pg=v3.aggregate_pair(context,lr,og,aux); lower_offers+=1; rem,reds=lower.reduce_packed(v3.pack_trits(pl)); comp=pg.copy()
            for p,c in reds: v3._add_mod3(comp,lower_comp[int(p)],-int(c))
            if np.any(v3.unpack_trits(rem,v3.PHYSICAL_LOWER_WIDTH)):
                scale=add_lower(rem,reds,origin)
                lower_origin_rows.append(v3.pack_trits(pl).tobytes())
                if scale==2: comp[:]=(2*comp.astype(np.uint16)%3).astype(np.uint8)
                lower_comp.append(comp)
                lower_companion_rows.append(v3.pack_trits(comp).tobytes())
                lower_stored_rows.append(lower.rows[-1].tobytes())
            else:
                # Every old offer promoted into grade has an authenticated
                # physical lower remainder, which must be exactly zero.
                old_lower_zero_rows.append(rem.tobytes())
                r=grade.insert(comp); grade_offers+=1
                if r['accepted']:
                    grade_origin_rows.append(v3.pack_trits(comp).tobytes())
                    ls=len(lower_edges); lower_edges.extend((int(p),int(c)) for p,c in reds); es=len(grade_edges); grade_edges.extend((int(p),int(c)) for p,c in r['reductions']); grade_nodes.append((origin,r['scale'],es,len(r['reductions']),ls,len(reds)))
            logical+=1
        source_refs=[]
        for item in prepare['old_blocks']:
            ch=int(item['character_index']); rank=int(item['rank']); low=np.frombuffer(v3.read_blob(a.state,item['lower_basis_blob']),dtype=np.uint8).reshape(rank,v3.LOWER_ECHELON_WIDTH//4); lift=np.frombuffer(v3.read_blob(a.state,item['lifted_grade_blob']),dtype=np.uint8).reshape(rank,v3.SOURCE_TOTAL_WIDTH//4)
            for p in range(rank):
                lr=v3.unpack_trits(low[p],v3.LOWER_ECHELON_WIDTH); ol=np.zeros((4,v3.SOURCE_BASE_WIDTH),dtype=np.uint8); ol[ch]=lr[:v3.SOURCE_BASE_WIDTH]; og=v3.unpack_trits(lift[p],v3.SOURCE_TOTAL_WIDTH).reshape(4,v3.SOURCE_BLOCK_WIDTH); old_route(ch,ol,og,lr[v3.SOURCE_BASE_WIDTH:],logical); rec=item.get('record',{}); node=rec.get('dag_nodes',[None])[p] if p<len(rec.get('dag_nodes',[])) else None; origin_node=node.get('origin',{}) if isinstance(node,dict) else {}; seed=int(origin_node.get('seed',0)) if origin_node.get('kind')=='projected_seed' else None; source_refs.append({'logical':logical-1,'kind':'old','character':ch,'pivot':p,'old_dag_node':node,'defect_origin_range':item.get('defect_origin_range'),'seed_index':seed,'seed_reduction':rec.get('seed_reductions',[None])[seed-1] if seed and seed<=len(rec.get('seed_reductions',[])) else None,'ancestry_key':f'old:{ch}:{p}'})
        if logical!=2014: fail('old_cursor')
        for i,(b,bd) in enumerate(blocks):
            owner=v3.load_block_owner(a.state,b)
            for p in range(len(owner.rows)):
                origin_grade=v3.aggregate_pure_grade(context,i,owner.dense_row(p)); r=grade.insert(origin_grade); grade_offers+=1
                if r['accepted']:
                    grade_origin_rows.append(v3.pack_trits(origin_grade).tobytes())
                    es=len(grade_edges); grade_edges.extend((int(q),int(c)) for q,c in r['reductions']); grade_nodes.append((logical,r['scale'],es,len(r['reductions']),0,0))
                node=b.get('dag_nodes',[None])[p] if p<len(b.get('dag_nodes',[])) else None; source_refs.append({'logical':logical,'kind':'block','block':i,'pivot':p,'block_dag_node':node,'ancestry_key':f'block:{i}:{p}'}); logical+=1
            guard(started)
        grade_basis_bytes=grade.matrix_bytes()
        if (logical,len(lower.rows),grade_offers,len(grade.rows))!=(8059,1661,6398,5044) or sha(grade_basis_bytes)!=BASIS_SHA or grade_basis_bytes!=basis_blob: fail('route_mismatch')
        guard(started)
        residual=v3.np.frombuffer(v3.read_blob(a.state,prepare['residual_blob']),dtype=v3.np.uint8).copy(); rem,coeffs=grade.reduce_packed(residual)
        if np.any(rem) or coeffs!=decision['member_coefficients'] or not np.array_equal(rem,candidate_remainder): fail('member_mismatch')
        # Reverse least closure, retaining original pivot identities and edge order.
        gsel=np.zeros(len(grade_nodes),dtype=bool); lsel=np.zeros(len(lower_nodes),dtype=bool)
        for p,c in coeffs: gsel[int(p)]=True
        for j in range(len(grade_nodes)-1,-1,-1):
            if gsel[j]:
                _,_,es,n,ls,ln=grade_nodes[j]
                for p,c in grade_edges[es:es+n]: gsel[p]=True
                for p,c in lower_edges[ls:ls+ln]:
                    if p<len(lsel): lsel[p]=True
        for j in range(len(lower_nodes)-1,-1,-1):
            if lsel[j]:
                _,_,es,n,_,_=lower_nodes[j]
                for p,c in lower_edges[es:es+n]:
                    if p>=j: fail('closure_order')
                    lsel[p]=True
        out=a.out; out.mkdir(parents=True,exist_ok=True); files={}
        if len(grade_nodes)*struct.calcsize('<IBQIQI')+len(lower_nodes)*struct.calcsize('<IBQIQI')+3*(len(grade_edges)+len(lower_edges))>7*1024**3: fail('UNKNOWN_RESOURCE:durable_cap')
        selected_origins={grade_nodes[i][0] for i in range(len(grade_nodes)) if gsel[i]}; selected_origins.update(lower_nodes[i][0] for i in range(len(lower_nodes)) if lsel[i]); selected_refs=[x for x in source_refs if x['logical'] in selected_origins]
        refs_by_logical={int(x['logical']):x for x in source_refs}; pending={}; states=[]; root_emissions=[]; leaf_map={}
        def prepend(prefix,suffix): return tuple(v3.floor.wm(tuple(prefix),tuple(suffix)))
        def push(kind,ids,prefix,coefficient,children):
            coefficient=int(coefficient)%3
            if not coefficient: return
            key=(kind,)+tuple(int(x) for x in ids)+(tuple(prefix),); pending[key]=(pending.get(key,0)+coefficient)%3
            if pending[key]==0: pending.pop(key)
            children.append({'kind':kind,'ids':[int(x) for x in ids],'prefix':[int(x) for x in prefix],'coefficient':coefficient})
        def leaf(seed,word,coefficient):
            coefficient=int(coefficient)%3
            key=(int(seed),tuple(int(x) for x in word)); value=(leaf_map.get(key,0)+coefficient)%3
            if value: leaf_map[key]=value
            else: leaf_map.pop(key,None)
        for pivot,coefficient in coeffs: push('grade',(int(pivot),),(),int(coefficient),root_emissions)
        while pending:
            key,coefficient=pending.popitem(); kind=key[0]; ids=tuple(int(x) for x in key[1:-1]); prefix=tuple(key[-1]); children=[]; state={'kind':kind,'ids':[int(x) for x in ids],'prefix':[int(x) for x in prefix],'coefficient':int(coefficient),'children':children}
            if kind=='grade':
                pivot=ids[0]; origin=refs_by_logical[int(grade_nodes[pivot][0])]; node=origin.get('old_dag_node') if origin['kind']=='old' else origin.get('block_dag_node'); state['source_ref']=origin; state['source_node']=node; scale=int(grade_nodes[pivot][1]);
                if origin['kind']=='old':
                    push('old',(int(origin['character']),int(origin['pivot'])),prefix,coefficient*scale,children); ls,ln=grade_nodes[pivot][4:6]
                    for q,c in lower_edges[ls:ls+ln]: push('lower',(int(q),),prefix,-coefficient*scale*int(c),children)
                elif origin['kind']=='block': push('block',(int(origin['block']),int(origin['pivot'])),prefix,coefficient*scale,children)
                else: fail('ancestry_grade_origin')
                es,n=grade_nodes[pivot][2:4]
                for q,c in grade_edges[es:es+n]: push('grade',(int(q),),prefix,-coefficient*scale*int(c),children)
            elif kind=='lower':
                origin=refs_by_logical[int(lower_nodes[ids[0]][0])]; state['source_ref']=origin; state['source_node']=origin.get('old_dag_node'); scale=int(lower_nodes[ids[0]][1]); push('old',(int(origin['character']),int(origin['pivot'])),prefix,coefficient*scale,children); es,n=lower_nodes[ids[0]][2:4]
                for q,c in lower_edges[es:es+n]: push('lower',(int(q),),prefix,-coefficient*scale*int(c),children)
            elif kind=='block':
                block,pivot=ids; b=blocks[block][0]; node=b['dag_nodes'][pivot]; state['source_node']=node; state['source_block']=block; scale=int(node['scale']); origin=node['origin']
                if origin['kind']=='defect':
                    label=v3.CHARACTER_LABELS[block]
                    for parity,word in v3.PURE_Q1_WORDS.items(): push('defect',(int(origin['origin']),),prepend(prefix,word),coefficient*scale*v3.cv(label,parity[0],parity[1]),children)
                elif origin['kind']=='actor': push('block',(block,int(origin['parent'])),prepend(prefix,(int(origin['letter']),)),coefficient*scale,children)
                else: fail('ancestry_block_origin')
                for q,c in node['reductions']: push('block',(block,int(q)),prefix,-coefficient*scale*int(c),children)
            elif kind=='defect':
                oi=ids[0]; origin=prepare['defect_origins'][oi]; state['defect_origin']=origin; character=int(origin['lower_character']); old=prepare['old_blocks'][character];
                if origin['kind']=='seed':
                    seed=int(origin['seed']); state['seed_reduction']=old['record']['seed_reductions'][seed-1]
                    for parity,word in v3.PURE_Q1_WORDS.items(): leaf(seed,prepend(prefix,word),coefficient*v3.cv(v3.CHARACTER_LABELS[character],parity[0],parity[1]))
                    expression=state['seed_reduction']
                elif origin['kind']=='transition':
                    pivot,letter=int(origin['pivot']),int(origin['letter']); state['actor_transition']=old['record']['actor_transitions'][pivot][v3.ACTORS.index(letter)]; push('old',(character,pivot),prepend(prefix,(letter,)),coefficient,children); expression=state['actor_transition']
                else: fail('ancestry_defect_origin')
                for q,c in expression: push('old',(character,int(q)),prefix,-coefficient*int(c),children)
            elif kind=='old':
                character,pivot=ids; old=prepare['old_blocks'][character]; node=old['record']['dag_nodes'][pivot]; state['source_node']=node; scale=int(node['scale']); origin=node['origin']
                if origin['kind']=='projected_seed':
                    seed=int(origin['seed']); state['seed_index']=seed; state['seed_reduction']=old['record']['seed_reductions'][seed-1]
                    for parity,word in v3.PURE_Q1_WORDS.items(): leaf(seed,prepend(prefix,word),coefficient*scale*v3.cv(v3.CHARACTER_LABELS[character],parity[0],parity[1]))
                elif origin['kind']=='actor':
                    state['actor_transition']=old['record']['actor_transitions'][pivot][v3.ACTORS.index(int(origin['letter']))]; push('old',(character,int(origin['parent'])),prepend(prefix,(int(origin['letter']),)),coefficient*scale,children)
                else: fail('ancestry_old_origin')
                for q,c in node['reductions']: push('old',(character,int(q)),prefix,-coefficient*scale*int(c),children)
            else: fail('ancestry_kind')
            states.append(state)
            if len(states)+len(leaf_map)>7*1024*1024: fail('UNKNOWN_RESOURCE:ancestry_cap')
        leaves=[{'seed':seed,'word':list(word),'coefficient':coefficient} for (seed,word),coefficient in sorted(leaf_map.items(),key=lambda item:(item[0][0],item[0][1]))]
        source_nodes={}; defect_nodes={}; expressions={}
        def old_node(ch,p):
            key=f'old:{int(ch)}:{int(p)}'
            if key in source_nodes: return key
            rec=prepare['old_blocks'][ch]['record']; node=rec['dag_nodes'][p]; origin=node['origin']; children=[]
            if origin['kind']=='actor': children.append(f'old:{int(ch)}:{int(origin["parent"])}')
            for q,_ in node['reductions']: children.append(f'old:{int(ch)}:{int(q)}')
            item={'key':key,'kind':'old','character':int(ch),'pivot':int(p),'node':node,'children':children,'expression_key':None,'syntax':{'origin':origin,'reductions':[{'pivot':int(q),'coefficient':int(c)} for q,c in node['reductions']],'scale':int(node['scale'])}}
            source_nodes[key]=item
            for child in children: old_node(ch,int(child.rsplit(':',1)[1]))
            return key
        def block_node(ch,p):
            key=f'block:{int(ch)}:{int(p)}'
            if key in source_nodes: return key
            body=blocks[ch][0]; node=body['dag_nodes'][p]; origin=node['origin']; children=[]
            if origin['kind']=='actor': children.append(f'block:{int(ch)}:{int(origin["parent"])}')
            elif origin['kind']=='defect':
                oi=int(origin['origin']); dkey=f'defect:{oi}'; children.append(dkey)
                if dkey not in defect_nodes:
                    defect_nodes[dkey]={'key':dkey,'kind':'defect','source_block':int(ch),'origin':prepare['defect_origins'][oi],'children':[]}
                    ex=prepare['defect_origins'][oi]; oldch=int(ex['lower_character'])
                    if ex['kind']=='seed': expressions[f'seed:{oldch}:{int(ex["seed"])}']={'key':f'seed:{oldch}:{int(ex["seed"])}','kind':'seed_reduction','character':oldch,'seed':int(ex['seed']),'expression':prepare['old_blocks'][oldch]['record']['seed_reductions'][int(ex['seed'])-1]}
                    elif ex['kind']=='transition': expressions[f'actor:{oldch}:{int(ex["pivot"])}:{int(ex["letter"])}']={'key':f'actor:{oldch}:{int(ex["pivot"])}:{int(ex["letter"])}','kind':'actor_transition_expression','character':oldch,'pivot':int(ex['pivot']),'letter':int(ex['letter']),'expression':prepare['old_blocks'][oldch]['record']['actor_transitions'][int(ex['pivot'])][v3.ACTORS.index(int(ex['letter']))]}
                    expression=prepare['old_blocks'][oldch]['record']['seed_reductions'][int(ex['seed'])-1] if ex['kind']=='seed' else prepare['old_blocks'][oldch]['record']['actor_transitions'][int(ex['pivot'])][v3.ACTORS.index(int(ex['letter']))]
                    defect_nodes[dkey]['expression_key']=f'seed:{oldch}:{int(ex["seed"])}' if ex['kind']=='seed' else f'actor:{oldch}:{int(ex["pivot"])}:{int(ex["letter"])}'
                    if ex['kind']=='transition': old_node(oldch,int(ex['pivot'])); defect_nodes[dkey]['children'].append(f'old:{oldch}:{int(ex["pivot"])}')
                    for q,_ in expression: old_node(oldch,int(q)); defect_nodes[dkey]['children'].append(f'old:{oldch}:{int(q)}')
            for q,_ in node['reductions']: children.append(f'block:{int(ch)}:{int(q)}')
            source_nodes[key]={'key':key,'kind':'block','character':int(ch),'pivot':int(p),'node':node,'children':children,'syntax':{'origin':origin,'reductions':[{'pivot':int(q),'coefficient':int(c)} for q,c in node['reductions']],'scale':int(node['scale'])}}
            if origin['kind']=='actor': block_node(ch,int(origin['parent']))
            for q,_ in node['reductions']: block_node(ch,int(q))
            return key
        for ref in selected_refs:
            if ref['kind']=='old': old_node(int(ref['character']),int(ref['pivot']))
            else: block_node(int(ref['block']),int(ref['pivot']))
        words_path=ROOT/'scratchpad/a0_paper_words_v1.json'; words_raw=words_path.read_bytes(); words=json.loads(words_raw.decode('utf-8'))
        literal_dictionary={'schema':'d972.r07.a0.literal-dictionary.v1','source_file':'scratchpad/a0_paper_words_v1.json','source_sha256':sha(words_raw),'relators_sha256':words.get('relators_sha256'),'relators':words['relators'],'pure_q1_words':{str(k):list(v) for k,v in v3.PURE_Q1_WORDS.items()},'literal_actor_words':{'x':[1],'x_inverse':[-1],'y':[2],'y_inverse':[-2]}}
        structural={'schema':'d972.r07.a0.selected-slp-structure.v2','syntax_contract':['origin','ordered_signed_reductions','scale_power'],'member_roots':[{'pivot':int(p),'coefficient':int(c)} for p,c in coeffs],'grade_selected':[int(i) for i,x in enumerate(gsel) if x],'lower_selected':[int(i) for i,x in enumerate(lsel) if x],'source_nodes':[source_nodes[k] for k in sorted(source_nodes)],'defect_nodes':[defect_nodes[k] for k in sorted(defect_nodes)],'expressions':[expressions[k] for k in sorted(expressions)],'literal_dictionary':literal_dictionary}
        ancestry={'schema':'d972.r07.a0.selected-ancestry.v2','selected_refs':selected_refs,'roots':root_emissions,'structure':structural,'derived':{'schema':'d972.r07.a0.selected-literal-derived.v1','states':states,'literal_leaves':leaves}}
        guard(started)
        refs_raw=canon(selected_refs); ancestry_raw=canon(ancestry); grade_nodes_raw=pack_records(grade_nodes); grade_edges_raw=edge_bytes(grade_edges); lower_nodes_raw=pack_records(lower_nodes); lower_edges_raw=edge_bytes(lower_edges); lower_origins_raw=b''.join(lower_origin_rows); lower_stored_raw=b''.join(lower_stored_rows); lower_companions_raw=b''.join(lower_companion_rows); grade_origins_raw=b''.join(grade_origin_rows); old_lower_zero_raw=b''.join(old_lower_zero_rows)
        durable=sum(len(x) for x in (grade_nodes_raw,grade_edges_raw,lower_nodes_raw,lower_edges_raw,lower_origins_raw,lower_stored_raw,lower_companions_raw,grade_origins_raw,old_lower_zero_raw,bitset(gsel),bitset(lsel),refs_raw,ancestry_raw))
        if durable>7*1024**3: fail('UNKNOWN_RESOURCE:durable_cap')
        files['grade_nodes']=write_receipt(out,'grade-nodes.bin',grade_nodes_raw); files['grade_edges']=write_receipt(out,'grade-edges.bin',grade_edges_raw); files['lower_nodes']=write_receipt(out,'lower-nodes.bin',lower_nodes_raw); files['lower_edges']=write_receipt(out,'lower-edges.bin',lower_edges_raw); files['lower_origins']=write_receipt(out,'lower-origins.bin',lower_origins_raw); files['lower_stored']=write_receipt(out,'lower-stored.bin',lower_stored_raw); files['lower_companions']=write_receipt(out,'lower-companions.bin',lower_companions_raw); files['grade_origins']=write_receipt(out,'grade-origins.bin',grade_origins_raw); files['old_lower_zero']=write_receipt(out,'old-lower-zero.bin',old_lower_zero_raw); files['selected_grade']=write_receipt(out,'selected-grade.bits',bitset(gsel)); files['selected_lower']=write_receipt(out,'selected-lower.bits',bitset(lsel)); files['source_refs']=write_receipt(out,'source-refs.json',refs_raw); files['source_ancestry']=write_receipt(out,'source-ancestry.json',ancestry_raw)
        roots={'C_T':{'type':'OrderedProduct','children':[{'type':'GradeNodeRef','pivot':int(p),'coefficient':int(c)} for p,c in coeffs]},'C_<1':{'type':'RegisteredPriorProduct','terms':prepare.get('canonical_solution',{}).get('terms',[])},'C_1':{'type':'Compose','left':'C_<1','right':'C_T'},'direct_occurrence_replay':False,'next_degree2_residual':None,'cross_checked':False,'verified':False,'A0':False,'COMMON':False,'FAKE':False,'IHARA':False}
        files['roots']=write_receipt(out,'roots.json',canon(roots)); manifest={'schema':'d972.r07.a0.grade1-selected-slp.v1','marker':MARKER,'decision_sha256':BODY_SHA,'prepare_sha256':prepare_digest,'block_sha256':[d for _,d in blocks],'cursor':logical,'lower_offer_count':lower_offers,'lower_rank':len(lower.rows),'grade_offer_count':grade_offers,'grade_rank':len(grade.rows),'coefficient_count':len(coeffs),'files':files,'roots':'roots.json','direct_occurrence_replay':False,'next_degree2_residual':None,'cross_checked':False,'verified':False,'A0':False,'COMMON':False,'FAKE':False,'IHARA':False,'elapsed_seconds':time.monotonic()-started}; (out/'manifest.json').write_bytes(canon(manifest)); print(json.dumps({'marker':MARKER,'cursor':logical,'lower_rank':len(lower.rows),'grade_rank':len(grade.rows),'coefficient_count':len(coeffs)},sort_keys=True)); return 0
    except Exception as e:
        print(json.dumps({'status':'NOT_READY','error':str(e)}),file=os.sys.stderr); return 1
if __name__=='__main__': raise SystemExit(main())
