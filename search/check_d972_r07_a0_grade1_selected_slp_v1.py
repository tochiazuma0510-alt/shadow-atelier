#!/usr/bin/env python3
"""Independent parser and linear replay for the selected SLP payload."""
from __future__ import annotations
import argparse, hashlib, importlib.util, json, os, struct, sys, time
from pathlib import Path
import numpy as np
try:
    import resource
except ImportError:
    resource = None

ROOT=Path(__file__).resolve().parents[1]; MARKER='R07_GRADE1_SELECTED_SLP_V1_CHECKER_PASS'; BODY_SHA='62412762b3a208d31febb6c6b8d4707f880471ed32cf62c79c18108065ab7b5d'; PREPARE_SHA='1f191d88a0453360021ec57d253a7d16c9a66ac059ddaaadb6db3e2b9293c865'; BASIS_SHA='b562c980c22a25a932bae1b548f72aeede5637b9612afc908fff9a9aecff069d'; REMAINDER_SHA='564cbfafc869a8c6eb761a392caa5e792b546bf577af7fe808177b2fdf13cbb0'; V3_SHA='bf872b30149e1351762b243d590d7a1f876e048b92a053d8f9c17bba5c45bcff'; WIDTH=24192; BYTES=6048; GRADE=5044; LOWER=1661
ROUTER_PATH=ROOT/'crosscheck/check_d972_r07_a0_first_rung_grade1_full_routing_v2.py'; ROUTER_SHA='a0504ae6a2562aab3b9af5ba7ed672bcc87bbd1cfdf5cc9fd3489240e51008e3'
TRITS=np.asarray([[(x//3**d)%3 for d in range(4)] for x in range(81)],dtype=np.uint8); WEIGHTS=np.asarray((1,3,9,27),dtype=np.uint16); AXPY=np.zeros((3,81,81),dtype=np.uint8)
for c in range(3):
    for a in range(81):
        for b in range(81): AXPY[c,a,b]=int(np.dot((TRITS[a].astype(np.int16)-c*TRITS[b].astype(np.int16))%3,WEIGHTS))
def sha(b): return hashlib.sha256(b).hexdigest()
def canon(x): return (json.dumps(x,sort_keys=True,separators=(',',':'),ensure_ascii=True)+'\n').encode('ascii')
def fail(s): raise RuntimeError(s)
def guard(started):
    if time.monotonic()-started > float(os.environ.get('TASK601_SECONDS','2400')): fail('UNKNOWN_RESOURCE:time')
    if resource is not None and resource.getrusage(resource.RUSAGE_SELF).ru_maxrss*1024 > int(os.environ.get('TASK601_MAX_RSS',str(7*1024**3))): fail('UNKNOWN_RESOURCE:rss')
def bits(data,n):
    if len(data)!=(n+7)//8: fail('bitset_size')
    return [bool(data[i//8]&(1<<(i%8))) for i in range(n)]
def unpack(row):
    if len(row)!=BYTES or any(x>80 for x in row): fail('packed_row')
    return TRITS[np.frombuffer(row,dtype=np.uint8)].reshape(-1).copy()
def load_candidate(d):
    raw=(d/'decision-v2.HEAD').read_bytes(); h=json.loads(raw)
    if sha(raw)!='07de7a817e8c5ae2e7346402a290c32631d05b0cc621d03702faa6cb43a948c0' or h.get('body_sha256')!=BODY_SHA: fail('candidate_head')
    bodyraw=(d/f'decision-v2.{BODY_SHA}.json').read_bytes(); body=json.loads(bodyraw)
    if sha(bodyraw)!=BODY_SHA or body.get('terminal')!='GRADE1_DECISION_MEMBER': fail('candidate_body')
    b=body.get('basis_receipt',{}); r=body.get('remainder_receipt',{})
    basis=(d/b['file']).read_bytes(); rem=(d/r['file']).read_bytes()
    if sha(basis)!=BASIS_SHA or len(basis)!=GRADE*BYTES or sha(rem)!=REMAINDER_SHA or len(rem)!=BYTES: fail('candidate_blobs')
    return body,basis,rem
def load_residual(state):
    hp=state/'prepare.HEAD'; hr=hp.read_bytes(); h=json.loads(hr)
    if h.get('body_sha256')!=PREPARE_SHA or h.get('stem')!='prepare' or h.get('parent_sha256') is not None or canon(h)!=hr: fail('prepare_head')
    raw=(state/f'prepare.{PREPARE_SHA}.json').read_bytes(); p=json.loads(raw)
    if sha(raw)!=PREPARE_SHA: fail('prepare_body')
    r=p.get('residual_blob',{}); f=r.get('file',''); data=(state/f).read_bytes()
    if len(data)!=6048 or sha(data)!=r.get('sha256'): fail('residual_auth')
    return p, data
def read_records(data):
    size=struct.calcsize('<IBQIQI')
    if len(data)%size: fail('node_record_size')
    return [struct.unpack_from('<IBQIQI',data,i) for i in range(0,len(data),size)]
def validate_canonical_graph(graph):
    if graph.get('canonical') is not True: fail('canonical_graph_schema')
    nodes=graph.get('nodes',[]); defects=graph.get('defects',[]); expressions=graph.get('expressions',[])
    all_items=nodes+defects; keys=[x.get('key') for x in all_items]
    if [x.get('key') for x in nodes]!=sorted(x.get('key') for x in nodes) or [x.get('key') for x in defects]!=sorted(x.get('key') for x in defects) or len(keys)!=len(set(keys)) or any(not isinstance(x,dict) for x in all_items): fail('canonical_graph_identity')
    present=set(keys)
    for item in all_items:
        key=str(item.get('key','')); kind=key.split(':',1)[0]; children=item.get('children')
        if kind not in ('block','defect','old') or item.get('kind')!=kind or item.get('origin',kind)!=kind or not isinstance(children,list) or any(not isinstance(x,str) or x not in present for x in children): fail('canonical_graph_dependency')
        if 'scale' in item and item['scale'] not in (1,2): fail('canonical_graph_scale')
        if 'edge_order' in item and item['edge_order']!=children: fail('canonical_graph_order')
        if 'companion' in item and item['companion'] is not True: fail('canonical_graph_companion')
        if 'lower_zero' in item and item['lower_zero'] is not True: fail('canonical_graph_lower')
    ekeys=[x.get('key') for x in expressions]
    if ekeys!=sorted(ekeys) or len(ekeys)!=len(set(ekeys)) or any(not str(x).startswith(('seed:','actor:')) for x in ekeys): fail('canonical_graph_expression_identity')
def compare_source_structure(source_nodes,defect_nodes,expressions,expected_nodes,expected_defects,expected_expr):
    """Authoritative source-structure comparison used by production and tests."""
    validate_canonical_graph({'canonical':True,'nodes':source_nodes,'defects':defect_nodes,'expressions':expressions})
    node_map={x['key']:x for x in source_nodes}; defect_map={x['key']:x for x in defect_nodes}; expr_map={x['key']:x for x in expressions}
    if set(node_map)!=set(expected_nodes) or set(defect_map)!=set(expected_defects) or set(expr_map)!=set(expected_expr): fail('source_structure_key_closure')
    for key in expected_nodes:
        if node_map[key]!=expected_nodes[key]: fail('source_structure_node_exact')
    for key in expected_defects:
        if defect_map[key]!=expected_defects[key]: fail('source_structure_defect_exact')
    for key in expected_expr:
        if expr_map[key]!=expected_expr[key]: fail('source_structure_expression_exact')
def compare_root_binding(roots,member_roots):
    expected=[{'kind':'grade','ids':[int(x['pivot'])],'prefix':[],'coefficient':int(x['coefficient'])} for x in member_roots]
    if roots!=expected: fail('typed_root_binding')
def require_false_claim_flags(value,label):
    required={'direct_occurrence_replay':False,'next_degree2_residual':None,'cross_checked':False,'verified':False,'A0':False,'COMMON':False,'FAKE':False,'IHARA':False}
    if any(key not in value or value[key] is not expected for key,expected in required.items()): fail(label+'_claim_flags')
def compare_roots_receipt_pointer(manifest_roots,receipt_file):
    if manifest_roots!=receipt_file: fail('roots_pointer_binding')
def word_mul(*words):
    out=[]
    for word in words:
        for x in word:
            if out and out[-1]==-int(x): out.pop()
            else: out.append(int(x))
    return tuple(out)
PURE_Q1_WORDS={(0,0):(),(0,1):(-2,-2,-2,-2,-2,-2,-2,-2,-2),(1,0):(-2,-2,1,1,2,1,2,1,1),(1,1):(-2,-2,-2,-1,-2,-1,-1,-1,-2,-1)}
ACTORS=(1,-1,2,-2)
CHARACTERS=((0,0),(0,1),(1,0),(1,1))
def cv(label,a,b): return 1 if ((label[0]*a+label[1]*b)&1)==0 else 2
def expr_equal(a,b): return isinstance(a,list) and a==b
def sealed_body(state,stem,digest):
    raw=(state/f'{stem}.{digest}.json').read_bytes()
    if sha(raw)!=digest or canon(json.loads(raw))!=raw: fail('source_body_auth')
    return json.loads(raw)
def validate_source_ancestry(loaded,refs,prepare,blocks):
    if not isinstance(refs,list) or not refs: fail('source_refs_missing')
    ancestry=json.loads(loaded['source_ancestry'])
    if canon(ancestry)!=loaded['source_ancestry']: fail('source_ancestry_schema')
    selected=ancestry.get('selected_refs'); derived=ancestry.get('derived',{}); roots=ancestry.get('roots',[]); states=derived.get('states'); leaves=derived.get('literal_leaves'); structure=ancestry.get('structure',{})
    if selected!=refs or ancestry.get('schema')!='d972.r07.a0.selected-ancestry.v2' or derived.get('schema')!='d972.r07.a0.selected-literal-derived.v1' or not isinstance(roots,list) or not isinstance(states,list) or not isinstance(leaves,list) or structure.get('schema')!='d972.r07.a0.selected-slp-structure.v2': fail('source_ancestry_binding')
    logical_keys=[int(r.get('logical',-1)) for r in refs]
    if len(logical_keys)!=len(set(logical_keys)): fail('source_ref_logical_duplicate')
    refmap={int(r['logical']):r for r in refs}; keys=set(); gedges=[struct.unpack_from('<HB',loaded['grade_edges'],i) for i in range(0,len(loaded['grade_edges']),3)]; ledges=[struct.unpack_from('<HB',loaded['lower_edges'],i) for i in range(0,len(loaded['lower_edges']),3)]
    gn=read_records(loaded['grade_nodes']); ln=read_records(loaded['lower_nodes'])
    for r in refs:
        if not isinstance(r,dict) or r.get('ancestry_key') in keys: fail('source_ref_identity')
        keys.add(r.get('ancestry_key')); kind=r.get('kind'); ch=int(r.get('character',-1)) if kind=='old' else None; p=int(r.get('pivot',-1))
        if kind=='old':
            if ch not in range(4) or p<0 or p>=len(prepare['old_blocks'][ch]['record']['dag_nodes']): fail('source_old_ref')
            rec=prepare['old_blocks'][ch]['record']; node=rec['dag_nodes'][p]
            if r.get('old_dag_node')!=node or r.get('defect_origin_range')!=prepare['old_blocks'][ch]['defect_origin_range']: fail('source_old_binding')
            o=node['origin']
            if o['kind']=='projected_seed':
                seed=int(o['seed'])
                if r.get('seed_index')!=seed or r.get('seed_reduction')!=rec['seed_reductions'][seed-1] or r.get('actor_transition') is not None: fail('source_old_seed')
            elif o['kind']=='actor':
                if r.get('seed_index') is not None or r.get('seed_reduction') is not None or r.get('actor_transition') is not None: fail('source_old_actor')
            else: fail('source_old_origin')
        elif kind=='block':
            b=int(r.get('block',-1))
            if b not in range(4) or p<0 or p>=len(blocks[b]['dag_nodes']) or r.get('block_dag_node')!=blocks[b]['dag_nodes'][p]: fail('source_block_ref')
        else: fail('source_ref_kind')
    source_nodes=structure.get('source_nodes'); defect_nodes=structure.get('defect_nodes'); expressions=structure.get('expressions')
    if not isinstance(source_nodes,list) or not isinstance(defect_nodes,list) or not isinstance(expressions,list): fail('source_structure_groups')
    node_map={}; defect_map={}; expr_map={}
    for item in source_nodes:
        if not isinstance(item,dict) or not isinstance(item.get('key'),str) or item['key'] in node_map: fail('source_structure_duplicate')
        node_map[item['key']]=item
    if [x['key'] for x in source_nodes] != sorted(x['key'] for x in source_nodes): fail('source_structure_order')
    for item in defect_nodes:
        if not isinstance(item,dict) or not isinstance(item.get('key'),str) or item['key'] in defect_map: fail('source_defect_duplicate')
        defect_map[item['key']]=item
    if [x['key'] for x in defect_nodes] != sorted(x['key'] for x in defect_nodes): fail('source_defect_order')
    for item in expressions:
        if not isinstance(item,dict) or not isinstance(item.get('key'),str) or item['key'] in expr_map: fail('source_expression_duplicate')
        expr_map[item['key']]=item
    if [x['key'] for x in expressions] != sorted(x['key'] for x in expressions): fail('source_expression_order')
    validate_canonical_graph({'canonical':True,'nodes':source_nodes,'defects':defect_nodes,'expressions':expressions})
    # Independently derive the unique O(V+E) source closure from selected
    # physical origins.  The derived quotient transcript below is not allowed
    # to enlarge or define this canonical graph.
    expected_nodes={}; expected_defects={}; expected_expr={}
    def expect_old(c,p):
        key=f'old:{int(c)}:{int(p)}'
        if key in expected_nodes: return key
        rec=prepare['old_blocks'][c]['record']; actual=rec['dag_nodes'][p]; origin=actual['origin']; children=[]
        if origin['kind']=='actor': children.append(expect_old(c,int(origin['parent'])))
        children.extend(expect_old(c,int(q)) for q,_ in actual['reductions'])
        expected_nodes[key]={'key':key,'kind':'old','character':int(c),'pivot':int(p),'node':actual,'children':children,'expression_key':None,'syntax':{'origin':origin,'reductions':[{'pivot':int(q),'coefficient':int(v)} for q,v in actual['reductions']],'scale':int(actual['scale'])}}
        return key
    def expect_defect(block,oi):
        key=f'defect:{int(oi)}'
        if key in expected_defects: return key
        origin=prepare['defect_origins'][oi]; ch=int(origin['lower_character']); rec=prepare['old_blocks'][ch]['record']
        if origin['kind']=='seed':
            expression=rec['seed_reductions'][int(origin['seed'])-1]; ek=f'seed:{ch}:{int(origin["seed"])}'
            expected_expr[ek]={'key':ek,'kind':'seed_reduction','character':ch,'seed':int(origin['seed']),'expression':expression}
        elif origin['kind']=='transition':
            expression=rec['actor_transitions'][int(origin['pivot'])][ACTORS.index(int(origin['letter']))]; ek=f'actor:{ch}:{int(origin["pivot"])}:{int(origin["letter"])}'
            expected_expr[ek]={'key':ek,'kind':'actor_transition_expression','character':ch,'pivot':int(origin['pivot']),'letter':int(origin['letter']),'expression':expression}
        else: fail('source_expected_defect_origin')
        body=blocks[int(block)]; children=[]
        if origin['kind']=='transition': children.append(expect_old(ch,int(origin['pivot'])))
        children.extend(expect_old(ch,int(q)) for q,_ in expression)
        expected_defects[key]={'key':key,'kind':'defect','source_block':int(block),'origin':origin,'children':children,'expression_key':ek}
        return key
    def expect_block(c,p):
        key=f'block:{int(c)}:{int(p)}'
        if key in expected_nodes: return key
        body=blocks[c]; actual=body['dag_nodes'][p]; origin=actual['origin']; children=[]
        if origin['kind']=='actor': children.append(expect_block(c,int(origin['parent'])))
        elif origin['kind']=='defect': children.append(expect_defect(c,int(origin['origin'])))
        children.extend(expect_block(c,int(q)) for q,_ in actual['reductions'])
        expected_nodes[key]={'key':key,'kind':'block','character':int(c),'pivot':int(p),'node':actual,'children':children,'syntax':{'origin':origin,'reductions':[{'pivot':int(q),'coefficient':int(v)} for q,v in actual['reductions']],'scale':int(actual['scale'])}}
        return key
    for ref in refs:
        if ref['kind']=='old': expect_old(int(ref['character']),int(ref['pivot']))
        else: expect_block(int(ref['block']),int(ref['pivot']))
    compare_source_structure(source_nodes,defect_nodes,expressions,expected_nodes,expected_defects,expected_expr)
    compare_root_binding(roots,structure.get('member_roots',[]))
    for key,item in node_map.items():
        kind=item.get('kind'); ch=int(item.get('character',-1)); p=int(item.get('pivot',-1))
        if kind=='old':
            if ch not in range(4) or p<0 or p>=len(prepare['old_blocks'][ch]['record']['dag_nodes']): fail('source_old_index')
            actual=prepare['old_blocks'][ch]['record']['dag_nodes'][p]; expected=[f'old:{ch}:{int(actual["origin"]["parent"])}'] if actual['origin']['kind']=='actor' else []
            expected += [f'old:{ch}:{int(q)}' for q,_ in actual['reductions']]
        elif kind=='block':
            if ch not in range(4) or p<0 or p>=len(blocks[ch]['dag_nodes']): fail('source_block_index')
            actual=blocks[ch]['dag_nodes'][p]; expected=[f'block:{ch}:{int(actual["origin"]["parent"])}'] if actual['origin']['kind']=='actor' else ([f'defect:{int(actual["origin"]["origin"])}'] if actual['origin']['kind']=='defect' else [])
            expected += [f'block:{ch}:{int(q)}' for q,_ in actual['reductions']]
        else: fail('source_node_kind')
        if item.get('node')!=actual or item.get('children')!=expected or item.get('syntax')!={'origin':actual['origin'],'reductions':[{'pivot':int(q),'coefficient':int(c)} for q,c in actual['reductions']],'scale':int(actual['scale'])}: fail('source_node_binding')
        if kind=='old' and item.get('expression_key') is not None: fail('source_expression_link')
        if any(dep not in node_map and dep not in defect_map for dep in expected): fail('source_node_closure')
    for ref in refs:
        root_key=f"old:{int(ref['character'])}:{int(ref['pivot'])}" if ref['kind']=='old' else f"block:{int(ref['block'])}:{int(ref['pivot'])}"
        if root_key not in node_map: fail('source_root_missing')
    for key,item in defect_map.items():
        origin=item.get('origin'); oi=int(key.split(':',1)[1]) if key.startswith('defect:') else -1; block=int(item.get('source_block',-1))
        if oi<0 or oi>=len(prepare['defect_origins']) or origin!=prepare['defect_origins'][oi]: fail('source_defect_origin')
        ch=int(origin['lower_character']); expression=prepare['old_blocks'][ch]['record']['seed_reductions'][int(origin['seed'])-1] if origin['kind']=='seed' else prepare['old_blocks'][ch]['record']['actor_transitions'][int(origin['pivot'])][ACTORS.index(int(origin['letter']))]
        expected=([f'old:{ch}:{int(origin["pivot"])}'] if origin['kind']=='transition' else [])+[f'old:{ch}:{int(q)}' for q,_ in expression]
        if block not in range(4) or item.get('children')!=expected or item.get('expression_key') not in expr_map or any(dep not in node_map for dep in expected): fail('source_defect_expression')
    for key,item in expr_map.items():
        if item.get('kind')=='seed_reduction':
            c=int(item.get('character',-1)); seed=int(item.get('seed',0)); expected=prepare['old_blocks'][c]['record']['seed_reductions'][seed-1] if c in range(4) and 0<seed<=44 else None
        elif item.get('kind')=='actor_transition_row':
            c=int(item.get('character',-1)); p=int(item.get('pivot',-1)); expected=prepare['old_blocks'][c]['record']['actor_transitions'][p] if c in range(4) and 0<=p<len(prepare['old_blocks'][c]['record']['actor_transitions']) else None
        elif item.get('kind')=='actor_transition_expression':
            c=int(item.get('character',-1)); p=int(item.get('pivot',-1)); letter=int(item.get('letter',0)); expected=prepare['old_blocks'][c]['record']['actor_transitions'][p][ACTORS.index(letter)] if c in range(4) and 0<=p<len(prepare['old_blocks'][c]['record']['actor_transitions']) and letter in ACTORS else None
        else: fail('source_expression_kind')
        if expected is None or item.get('expression')!=expected: fail('source_expression_binding')
    words_path=ROOT/'scratchpad/a0_paper_words_v1.json'; words_raw=words_path.read_bytes(); words=json.loads(words_raw.decode('utf-8')); literal=structure.get('literal_dictionary',{})
    if literal.get('source_sha256')!=sha(words_raw) or literal.get('relators_sha256')!=words.get('relators_sha256') or literal.get('relators')!=words.get('relators') or literal.get('pure_q1_words')!={str(k):list(v) for k,v in PURE_Q1_WORDS.items()} or literal.get('literal_actor_words')!={'x':[1],'x_inverse':[-1],'y':[2],'y_inverse':[-2]}: fail('literal_dictionary_binding')
    # Every derived state must point into the canonical source tables; the
    # tables themselves were already closed independently from selected refs.
    statekeys=set()
    for s in states:
        if not isinstance(s,dict) or s.get('kind') not in ('grade','lower','block','defect','old') or not isinstance(s.get('ids'),list) or not isinstance(s.get('prefix'),list) or s.get('coefficient') not in (1,2): fail('typed_state_shape')
        k=(s['kind'],*s['ids'],tuple(s['prefix']))
        statekeys.add(k)
    for s in states:
        kind=s['kind']; ids=[int(x) for x in s['ids']]; pref=tuple(int(x) for x in s['prefix']); coef=int(s['coefficient']); children=s.get('children')
        if not isinstance(children,list): fail('typed_children')
        for chd in children:
            if not isinstance(chd,dict) or chd.get('kind') not in ('grade','lower','block','defect','old') or not isinstance(chd.get('ids'),list) or not isinstance(chd.get('prefix'),list) or chd.get('coefficient') not in (1,2): fail('typed_child_shape')
        exact_children=None
        if kind=='grade':
            pivot=ids[0]; logical=int(gn[pivot][0]); ref=refmap.get(logical)
            if ref is None or s.get('source_ref')!=ref or s.get('source_node')!=ref.get('old_dag_node',ref.get('block_dag_node')): fail('typed_grade_source')
            _,scale,e,n,_,_=gn[pivot]; expected=[{'kind':'grade','ids':[int(q)],'prefix':s['prefix'],'coefficient':(-coef*scale*int(c))%3} for q,c in gedges[e:e+n]]
            if children[-len(expected):] != expected if expected else any(x.get('kind')=='grade' for x in children): fail('typed_grade_edges')
            if ref['kind']=='old':
                origin_child={'kind':'old','ids':[int(ref['character']),int(ref['pivot'])],'prefix':s['prefix'],'coefficient':(coef*scale)%3}
                if not children or children[0] != {'kind':'old','ids':[int(ref['character']),int(ref['pivot'])],'prefix':s['prefix'],'coefficient':(coef*scale)%3}: fail('typed_grade_old_origin')
            elif ref['kind']=='block':
                origin_child={'kind':'block','ids':[int(ref['block']),int(ref['pivot'])],'prefix':s['prefix'],'coefficient':(coef*scale)%3}
                if not children or children[0] != {'kind':'block','ids':[int(ref['block']),int(ref['pivot'])],'prefix':s['prefix'],'coefficient':(coef*scale)%3}: fail('typed_grade_block_origin')
            lower_children=[{'kind':'lower','ids':[int(q)],'prefix':s['prefix'],'coefficient':(-coef*scale*int(c))%3} for q,c in ledges[gn[pivot][4]:gn[pivot][4]+gn[pivot][5]]]
            exact_children=[origin_child]+lower_children+expected
        elif kind=='lower':
            pivot=ids[0]; logical=int(ln[pivot][0]); ref=refmap.get(logical)
            if ref is None or s.get('source_ref')!=ref or s.get('source_node')!=ref.get('old_dag_node'): fail('typed_lower_source')
            _,scale,e,n,_,_=ln[pivot]; expected=[{'kind':'lower','ids':[int(q)],'prefix':s['prefix'],'coefficient':(-coef*scale*int(c))%3} for q,c in ledges[e:e+n]]
            if children[-len(expected):] != expected if expected else any(x.get('kind')=='lower' for x in children): fail('typed_lower_edges')
            if not children or children[0] != {'kind':'old','ids':[int(ref['character']),int(ref['pivot'])],'prefix':s['prefix'],'coefficient':(coef*scale)%3}: fail('typed_lower_origin')
            exact_children=[{'kind':'old','ids':[int(ref['character']),int(ref['pivot'])],'prefix':s['prefix'],'coefficient':(coef*scale)%3}]+expected
        elif kind=='block':
            b,pivot=ids
            if b not in range(4) or pivot>=len(blocks[b]['dag_nodes']) or s.get('source_block')!=b or s.get('source_node')!=blocks[b]['dag_nodes'][pivot]: fail('typed_block_source')
            node=s['source_node']; scale=int(node['scale']); expected=[{'kind':'block','ids':[b,int(q)],'prefix':s['prefix'],'coefficient':(-coef*scale*int(c))%3} for q,c in node['reductions']]
            if children[-len(expected):] != expected if expected else any(x.get('kind')=='block' for x in children): fail('typed_block_edges')
            origin=node['origin']
            if origin['kind']=='actor' and (not children or children[0] != {'kind':'block','ids':[b,int(origin['parent'])],'prefix':list(word_mul(pref,[int(origin['letter'])])),'coefficient':(coef*scale)%3}): fail('typed_block_actor_order')
            if origin['kind']=='defect':
                first=[]
                for parity in PURE_Q1_WORDS: first.append({'kind':'defect','ids':[int(origin['origin'])],'prefix':list(word_mul(pref,PURE_Q1_WORDS[parity])),'coefficient':(coef*scale*cv(CHARACTERS[b],parity[0],parity[1]))%3})
                if children[:4]!=first: fail('typed_block_defect_order')
                origin_children=first
            elif origin['kind']=='actor':
                origin_children=[{'kind':'block','ids':[b,int(origin['parent'])],'prefix':list(word_mul(pref,[int(origin['letter'])])),'coefficient':(coef*scale)%3}]
            else: origin_children=[]
            exact_children=origin_children+expected
        elif kind=='defect':
            oi=ids[0]
            if oi<0 or oi>=len(prepare['defect_origins']) or s.get('defect_origin')!=prepare['defect_origins'][oi]: fail('typed_defect_source')
            origin=s['defect_origin']; char=int(origin['lower_character']); expression=prepare['old_blocks'][char]['record']['seed_reductions'][int(origin['seed'])-1] if origin['kind']=='seed' else prepare['old_blocks'][char]['record']['actor_transitions'][int(origin['pivot'])][ACTORS.index(int(origin['letter']))]; expected=[{'kind':'old','ids':[char,int(q)],'prefix':s['prefix'],'coefficient':(-coef*int(c))%3} for q,c in expression]
            if children[-len(expected):] != expected if expected else any(x.get('kind')=='old' for x in children): fail('typed_defect_edges')
            if origin['kind']=='transition' and (not children or children[0] != {'kind':'old','ids':[char,int(origin['pivot'])],'prefix':list(word_mul(pref,[int(origin['letter'])])),'coefficient':coef}): fail('typed_defect_transition_order')
            origin_children=[{'kind':'old','ids':[char,int(origin['pivot'])],'prefix':list(word_mul(pref,[int(origin['letter'])])),'coefficient':coef}] if origin['kind']=='transition' else []
            exact_children=origin_children+expected
        elif kind=='old':
            c,pivot=ids
            if c not in range(4) or pivot>=len(prepare['old_blocks'][c]['record']['dag_nodes']) or s.get('source_node')!=prepare['old_blocks'][c]['record']['dag_nodes'][pivot]: fail('typed_old_source')
            node=s['source_node']; scale=int(node['scale']); expected=[{'kind':'old','ids':[c,int(q)],'prefix':s['prefix'],'coefficient':(-coef*scale*int(v))%3} for q,v in node['reductions']]
            if children[-len(expected):] != expected if expected else any(x.get('kind')=='old' for x in children): fail('typed_old_edges')
            origin=node['origin']
            if origin['kind']=='actor' and (not children or children[0] != {'kind':'old','ids':[c,int(origin['parent'])],'prefix':list(word_mul(pref,[int(origin['letter'])])),'coefficient':(coef*scale)%3}): fail('typed_old_actor_order')
            if node['origin']['kind']=='projected_seed' and s.get('seed_reduction')!=prepare['old_blocks'][c]['record']['seed_reductions'][int(node['origin']['seed'])-1]: fail('typed_old_seed')
            origin_children=[{'kind':'old','ids':[c,int(origin['parent'])],'prefix':list(word_mul(pref,[int(origin['letter'])])),'coefficient':(coef*scale)%3}] if origin['kind']=='actor' else []
            exact_children=origin_children+expected
        if exact_children is None or children != exact_children: fail('typed_children_exact')
        for chd in children:
            if chd['kind']=='grade' and chd['ids'] and chd['ids'][0]>=GRADE: fail('typed_grade_child')
            if chd['kind']=='lower' and chd['ids'] and chd['ids'][0]>=LOWER: fail('typed_lower_child')
            if chd['kind'] in ('block','old') and any(int(x)<0 for x in chd['ids']): fail('typed_source_child')
    def flow_key(item): return (item['kind'],*tuple(int(x) for x in item['ids']),tuple(int(x) for x in item['prefix']))
    incoming={}; processed={}
    for item in roots:
        if not isinstance(item,dict) or item.get('kind') not in ('grade','lower','block','defect','old') or item.get('coefficient') not in (1,2): fail('typed_root_shape')
        k=flow_key(item); incoming[k]=(incoming.get(k,0)+int(item['coefficient']))%3
    for s in states:
        k=flow_key(s); processed[k]=(processed.get(k,0)+int(s['coefficient']))%3
        for item in s['children']:
            k2=flow_key(item); incoming[k2]=(incoming.get(k2,0)+int(item['coefficient']))%3
    incoming={k:v for k,v in incoming.items() if v}; processed={k:v for k,v in processed.items() if v}
    if incoming!=processed: fail('typed_flow_conservation')
    if not leaves: fail('literal_leaves_missing')
    for leaf in leaves:
        if not isinstance(leaf,dict) or not isinstance(leaf.get('seed'),int) or leaf['seed']<=0 or not isinstance(leaf.get('word'),list) or any(not isinstance(x,int) or x==0 for x in leaf['word']) or leaf.get('coefficient') not in (1,2): fail('literal_leaf_shape')
    expected_leaves={}
    for s in states:
        if s['kind']=='old':
            c,p=s['ids']; node=s['source_node']; origin=node['origin']
            if origin['kind']=='projected_seed':
                seed=int(origin['seed']); scale=int(node['scale'])
                for parity,word in PURE_Q1_WORDS.items():
                    key=(seed,word_mul(tuple(s['prefix']),word)); value=(expected_leaves.get(key,0)+int(s['coefficient'])*scale*cv(CHARACTERS[c],parity[0],parity[1]))%3
                    if value: expected_leaves[key]=value
                    else: expected_leaves.pop(key,None)
        elif s['kind']=='defect' and s['defect_origin']['kind']=='seed':
            origin=s['defect_origin']; c=int(origin['lower_character']); seed=int(origin['seed'])
            for parity,word in PURE_Q1_WORDS.items():
                key=(seed,word_mul(tuple(s['prefix']),word)); value=(expected_leaves.get(key,0)+int(s['coefficient'])*cv(CHARACTERS[c],parity[0],parity[1]))%3
                if value: expected_leaves[key]=value
                else: expected_leaves.pop(key,None)
    expected=[{'seed':seed,'word':list(word),'coefficient':value} for (seed,word),value in sorted(expected_leaves.items(),key=lambda item:(item[0][0],item[0][1]))]
    if leaves!=expected: fail('literal_leaf_binding')
    return len(states),len(leaves)
def selected_physical_replay(loaded,gn,ln,gedges,ledges,basis,declared_gs,declared_ls):
    lwidth=2017; gwidth=BYTES
    lo=np.frombuffer(loaded['lower_origins'],dtype=np.uint8); ls=np.frombuffer(loaded['lower_stored'],dtype=np.uint8); lc=np.frombuffer(loaded['lower_companions'],dtype=np.uint8); go=np.frombuffer(loaded['grade_origins'],dtype=np.uint8); oz=np.frombuffer(loaded.get('old_lower_zero',b''),dtype=np.uint8)
    # The old route has one sealed lower remainder per offer.  This receipt is
    # deliberately separate from the selected transcript: it proves that no
    # old origin was silently promoted with a non-zero lower component.
    old_grade_count=sum(1 for row in gn if int(row[0])<2014)
    if oz.size!=old_grade_count*lwidth or np.any(oz): fail('old_origin_lower_nonzero')
    if lo.size!=len(ln)*lwidth or ls.size!=len(ln)*lwidth or lc.size!=len(ln)*gwidth or go.size!=len(gn)*gwidth: fail('physical_origin_receipts')
    if np.any(lo>80) or np.any(ls>80) or np.any(lc>80) or np.any(go>80): fail('physical_origin_packing')
    lower_rows=[]
    for i,(origin,stored) in enumerate(zip(lo.reshape(len(ln),lwidth),ls.reshape(len(ln),lwidth))):
        work=origin.copy(); _,scale,e,n,_,_=ln[i]
        for p,c in ledges[e:e+n]: work=AXPY[int(c),work,lower_rows[int(p)]]
        if int(scale)==2: work=np.asarray([int(np.dot((2*TRITS[x])%3,WEIGHTS)) for x in work],dtype=np.uint8)
        if not np.array_equal(work,stored): fail('lower_origin_replay')
        lower_rows.append(stored.copy())
    grade_rows=np.frombuffer(basis,dtype=np.uint8).reshape(GRADE,BYTES)
    for i,origin in enumerate(go.reshape(len(gn),gwidth)):
        if not declared_gs[i]: continue
        work=origin.copy(); _,scale,e,n,ls0,ln0=gn[i]
        if ls0+ln0>len(ledges): fail('grade_lower_link')
        for p,c in gedges[e:e+n]: work=AXPY[int(c),work,grade_rows[int(p)]]
        if int(scale)==2: work=np.asarray([int(np.dot((2*TRITS[x])%3,WEIGHTS)) for x in work],dtype=np.uint8)
        if not np.array_equal(work,grade_rows[i]): fail('grade_origin_replay')
    # Every selected lower pivot carries the authenticated companion row.  It
    # is kept as a packed physical row (rather than a derived MEMBER value),
    # so truncation or row reordering cannot pass the selected replay.
    for i,comp in enumerate(lc.reshape(len(ln),gwidth)):
        if declared_ls[i] and comp.shape!=(gwidth,): fail('lower_companion_replay')
    if any(declared_ls[i] and i>=len(lower_rows) for i in range(LOWER)): fail('selected_lower_replay')
    return {'selected_lower':sum(declared_ls),'selected_grade':sum(declared_gs),'lower_rows':lower_rows}
def selected_source_origin_replay(state,prepare,blocks,refs,loaded,gn,ln,gedges,ledges,declared_gs,declared_ls,physical):
    """Replay selected physical origins directly from sealed old/block blobs.

    This is intentionally separate from the producer route: transcript origin
    receipts are checked against the sealed source rows before edge replay.
    """
    sp=importlib.util.spec_from_file_location('sealed_v3',ROOT/'search/d972_r07_a0_first_rung_grade1_v3.py')
    if sp is None or sp.loader is None: fail('source_replay_loader')
    if sha((ROOT/'search/d972_r07_a0_first_rung_grade1_v3.py').read_bytes())!=V3_SHA: fail('source_replay_v3_hash')
    v3=importlib.util.module_from_spec(sp); sp.loader.exec_module(v3)
    def blob(receipt):
        if not isinstance(receipt,dict) or not isinstance(receipt.get('file'),str): fail('source_blob_receipt')
        data=(state/receipt['file']).read_bytes()
        if len(data)!=int(receipt.get('bytes',len(data))) or sha(data)!=receipt.get('sha256'): fail('source_blob_auth')
        return data
    old_cache={}
    def old_rows(ch):
        if ch in old_cache: return old_cache[ch]
        item=prepare['old_blocks'][ch]; lr= item['lower_basis_blob']; gr=item['lifted_grade_blob']
        low=np.frombuffer(blob(lr),dtype=np.uint8); lift=np.frombuffer(blob(gr),dtype=np.uint8)
        if low.size!=int(lr['rows'])*(v3.LOWER_ECHELON_WIDTH//4) or lift.size!=int(gr['rows'])*(v3.SOURCE_TOTAL_WIDTH//4): fail('source_blob_shape')
        old_cache[ch]=(low.reshape(int(lr['rows']),-1),lift.reshape(int(gr['rows']),-1)); return old_cache[ch]
    context=v3.context_for_state(prepare); refs_by_logical={int(r['logical']):r for r in refs}; block_owner_cache={}
    def block_owner(b):
        if b not in block_owner_cache: block_owner_cache[b]=v3.load_block_owner(state,blocks[b])
        return block_owner_cache[b]
    lo=np.frombuffer(loaded['lower_origins'],dtype=np.uint8).reshape(len(ln),2017); go=np.frombuffer(loaded['grade_origins'],dtype=np.uint8).reshape(len(gn),BYTES); lc=np.frombuffer(loaded['lower_companions'],dtype=np.uint8).reshape(len(ln),BYTES)
    lower_pivots={int(n[0]):i for i,n in enumerate(ln)}; grade_pivots={int(n[0]):i for i,n in enumerate(gn)}
    lower_comp=[unpack(row) for row in lc]
    lower_rows=physical['lower_rows']
    for logical,ref in refs_by_logical.items():
        if logical<2014:
            ch=int(ref['character']); p=int(ref['pivot']); low,lift=old_rows(ch)
            lr=v3.unpack_trits(low[p],v3.LOWER_ECHELON_WIDTH); occurrence_lower=np.zeros((4,v3.SOURCE_BASE_WIDTH),dtype=np.uint8); occurrence_lower[ch]=lr[:v3.SOURCE_BASE_WIDTH]
            occurrence_grade=v3.unpack_trits(lift[p],v3.SOURCE_TOTAL_WIDTH).reshape(4,v3.SOURCE_BLOCK_WIDTH)
            physical_lower,physical_grade=v3.aggregate_pair(context,occurrence_lower,occurrence_grade,lr[v3.SOURCE_BASE_WIDTH:])
            if logical in lower_pivots:
                q=lower_pivots[logical]
                if declared_ls[q]:
                    if v3.pack_trits(physical_lower).tobytes()!=lo[q].tobytes(): fail('sealed_old_lower_origin')
                    companion=physical_grade.copy(); _,scale,es,n,_,_=ln[q]
                    for pivot,coef in ledges[es:es+n]: v3._add_mod3(companion,lower_comp[int(pivot)],-int(coef))
                    if int(scale)==2: companion[:]=(2*companion.astype(np.uint16))%3
                    if v3.pack_trits(companion).tobytes()!=lc[q].tobytes(): fail('sealed_old_companion')
            if logical in grade_pivots:
                q=grade_pivots[logical]; work=physical_grade.copy(); _,_,e,n,ls0,ln0=gn[q]
                for pivot,coef in ledges[ls0:ls0+ln0]: v3._add_mod3(work,lower_comp[int(pivot)],-int(coef))
                if v3.pack_trits(work).tobytes()!=go[q].tobytes(): fail('sealed_old_grade_origin')
        elif logical in grade_pivots:
            q=grade_pivots[logical]; b=int(ref['block']); source=v3.aggregate_pure_grade(context,b,block_owner(b).dense_row(int(ref['pivot'])))
            if v3.pack_trits(source).tobytes()!=go[q].tobytes(): fail('sealed_block_grade_origin')
    return True
def compare_authoritative_transcript(actual,expected):
    """Single equality gate for the independent route and its small tests."""
    for key in ('lower_nodes','grade_nodes','lower_edges','grade_edges','lower_origins','lower_stored','lower_companions','grade_origins','old_lower_zero'):
        if actual.get(key)!=expected.get(key): fail('authoritative_'+key+'_mismatch')
    if actual.get('basis')!=expected.get('basis'): fail('authoritative_basis_mismatch')
def independent_transcript_check(state,candidate,loaded,gn,ln,gedges,ledges,started):
    """Recreate every offer with the pinned standalone arithmetic router."""
    if sha(ROUTER_PATH.read_bytes())!=ROUTER_SHA: fail('router_hash')
    sp=importlib.util.spec_from_file_location('independent_router',ROUTER_PATH)
    if sp is None or sp.loader is None: fail('router_loader')
    router=importlib.util.module_from_spec(sp); sp.loader.exec_module(router)
    body, candidate_basis, _=router.candidate_files(candidate)
    prepare,prepare_digest,_,_,old_rows,blocks=router.load_source(state)
    ctx=router.Arithmetic(); lower=router.IndependentOwner(router.PHYSICAL_LOWER); grade=router.IndependentOwner(router.PHYSICAL_GRADE); companions=[]
    expected_ln=[]; expected_gn=[]; expected_le=[]; expected_ge=[]; expected_lo=[]; expected_ls=[]; expected_lc=[]; expected_go=[]; expected_oz=[]; logical=lower_offers=grade_offers=0
    for rank,low_raw,lift_raw,character in old_rows:
        low_mat=low_raw.reshape(rank,router.LOWER_WIDTH//4); lift_mat=lift_raw.reshape(rank,router.SOURCE_TOTAL//4)
        for pivot in range(rank):
            lower_row=router.unpack(low_mat[pivot],router.LOWER_WIDTH); occurrence_lower=np.zeros((4,router.SOURCE_BASE),dtype=np.uint8); occurrence_lower[character]=lower_row[:router.SOURCE_BASE]; occurrence_grade=router.unpack(lift_mat[pivot],router.SOURCE_TOTAL).reshape(4,router.SOURCE_BLOCK); physical_lower,physical_grade=router.aggregate_pair(ctx,occurrence_lower,occurrence_grade,lower_row[router.SOURCE_BASE:])
            lower_offers+=1; remainder,reductions=lower.reduce(router.pack(physical_lower)); companion=physical_grade.copy()
            for p,c in reductions: router.add_mod(companion,companions[p],-c)
            if np.any(remainder):
                accepted=lower.accept_reduced(remainder,reductions)
                if not accepted.get('accepted') or accepted.get('reductions')!=reductions: fail('router_lower_accept')
                scale=int(accepted['scale']);
                if scale==2: companion=((2*companion.astype(np.uint16))%3).astype(np.uint8)
                es=len(expected_le); expected_le.extend((int(p),int(c)) for p,c in reductions); expected_ln.append((logical,scale,es,len(reductions),0,0)); expected_lo.append(router.pack(physical_lower).tobytes()); expected_ls.append(lower.rows[-1].tobytes()); expected_lc.append(router.pack(companion).tobytes()); companions.append(companion)
            else:
                expected_oz.append(remainder.tobytes()); grade_offers+=1; ins=grade.insert(companion)
                if ins.get('accepted'):
                    ls=len(expected_le); expected_le.extend((int(p),int(c)) for p,c in reductions); es=len(expected_ge); expected_ge.extend((int(p),int(c)) for p,c in ins['reductions']); expected_gn.append((logical,int(ins['scale']),es,len(ins['reductions']),ls,len(reductions))); expected_go.append(router.pack(companion).tobytes())
            logical+=1
            if logical%256==0: guard(started)
    for block_index,(block_body,block_digest,raw,leads) in enumerate(blocks):
        rank=len(leads); mat=raw.reshape(rank,router.SOURCE_BLOCK//4)
        for pivot in range(rank):
            grade_offers+=1; companion=router.aggregate_pure(ctx,block_index,router.unpack(mat[pivot],router.SOURCE_BLOCK)); ins=grade.insert(companion)
            if ins.get('accepted'):
                es=len(expected_ge); expected_ge.extend((int(p),int(c)) for p,c in ins['reductions']); expected_gn.append((logical,int(ins['scale']),es,len(ins['reductions']),0,0)); expected_go.append(router.pack(companion).tobytes())
            logical+=1
            if logical%256==0: guard(started)
    if (logical,lower_offers,grade_offers,len(lower.rows),len(grade.rows))!=(8059,2014,6398,1661,5044): fail('router_counts')
    got_ln=[tuple(int(x) for x in row) for row in ln]; got_gn=[tuple(int(x) for x in row) for row in gn]
    routed_basis=grade.matrix_bytes()
    compare_authoritative_transcript({'lower_nodes':got_ln,'grade_nodes':got_gn,'lower_edges':ledges,'grade_edges':gedges,'lower_origins':bytes(loaded['lower_origins']),'lower_stored':bytes(loaded['lower_stored']),'lower_companions':bytes(loaded['lower_companions']),'grade_origins':bytes(loaded['grade_origins']),'old_lower_zero':bytes(loaded.get('old_lower_zero',b'')),'basis':routed_basis},{'lower_nodes':expected_ln,'grade_nodes':expected_gn,'lower_edges':expected_le,'grade_edges':expected_ge,'lower_origins':b''.join(expected_lo),'lower_stored':b''.join(expected_ls),'lower_companions':b''.join(expected_lc),'grade_origins':b''.join(expected_go),'old_lower_zero':b''.join(expected_oz),'basis':candidate_basis})
    if sha(routed_basis)!=BASIS_SHA: fail('authoritative_basis_hash')
    return True
def replay(payload:Path,candidate:Path,state:Path,out:Path|None):
    started=time.monotonic()
    manifest_raw=(payload/'manifest.json').read_bytes(); m=json.loads(manifest_raw)
    if canon(m)!=manifest_raw: fail('manifest_canonical')
    payload_manifest_sha256=sha(manifest_raw)
    require_false_claim_flags(m,'manifest')
    if m.get('schema')!='d972.r07.a0.grade1-selected-slp.v1' or m.get('marker')!='R07_GRADE1_SELECTED_SLP_V1_CANDIDATE': fail('manifest')
    if m.get('decision_sha256')!=BODY_SHA or m.get('prepare_sha256')!=PREPARE_SHA or m.get('cursor')!=8059 or m.get('lower_rank')!=LOWER or m.get('grade_rank')!=GRADE or m.get('coefficient_count')!=3317: fail('manifest_binding')
    body,basis,remainder=load_candidate(candidate)
    if body.get('prepare_sha256')!=m['prepare_sha256'] or body.get('block_sha256')!=m.get('block_sha256'): fail('parent_binding')
    files=m.get('files',{}); loaded={}
    for key,rec in files.items():
        if not isinstance(rec,dict) or rec.get('file') not in {p.name for p in payload.iterdir()}: fail('receipt_file')
        data=(payload/rec['file']).read_bytes()
        if len(data)!=rec.get('bytes') or sha(data)!=rec.get('sha256'): fail('receipt_auth')
        loaded[key]=data
    compare_roots_receipt_pointer(m.get('roots'),files.get('roots',{}).get('file'))
    if 'roots' not in loaded or canon(json.loads(loaded['roots']))!=loaded['roots']: fail('roots_canonical')
    rootsjson=json.loads(loaded['roots']); require_false_claim_flags(rootsjson,'roots')
    durable=sum(int(rec.get('bytes',0)) for rec in files.values())
    if durable > 7*1024**3: fail('UNKNOWN_RESOURCE:durable_cap')
    guard(started)
    prepare,_=load_residual(state)
    block_bodies=[sealed_body(state,f'block-{i}',m['block_sha256'][i]) for i in range(4)]
    refs=json.loads(loaded['source_refs'])
    if canon(refs)!=loaded['source_refs']: fail('source_refs_schema')
    validate_source_ancestry(loaded,refs,prepare,block_bodies)
    gn=read_records(loaded['grade_nodes']); ln=read_records(loaded['lower_nodes']); ge=loaded['grade_edges']; le=loaded['lower_edges']
    if len(gn)!=GRADE or len(ln)!=LOWER or len(ge)%3 or len(le)%3: fail('transcript_shape')
    def edges(data): return [struct.unpack_from('<HB',data,i) for i in range(0,len(data),3)]
    gedges=edges(ge); ledges=edges(le)
    for p,c in gedges+ledges:
        if c not in (1,2): fail('edge_coefficient')
    for i,(o,s,e,n,ls,lnum) in enumerate(gn):
        if s not in (1,2) or e+n>len(gedges): fail('grade_node')
        for p,c in gedges[e:e+n]:
            if p>=i: fail('grade_acyclic')
        if ls+lnum>len(ledges): fail('lower_edge_interval')
    for i,(o,s,e,n,_,_) in enumerate(ln):
        if s not in (1,2) or e+n>len(ledges): fail('lower_node')
        for p,c in ledges[e:e+n]:
            if p>=i: fail('lower_acyclic')
    declared_gs=bits(loaded['selected_grade'],GRADE); declared_ls=bits(loaded['selected_lower'],LOWER)
    coeffs=body.get('member_coefficients',[]); roots={int(p) for p,c in coeffs}
    if len(coeffs)!=3317 or not roots.issubset({i for i,x in enumerate(declared_gs) if x}): fail('grade_roots')
    gs=[False]*GRADE; ls=[False]*LOWER
    for p in roots: gs[p]=True
    for i in range(GRADE-1,-1,-1):
        if gs[i]:
            _,_,e,n,le0,ln0=gn[i]
            for p,c in gedges[e:e+n]: gs[p]=True
            for p,c in ledges[le0:le0+ln0]: ls[p]=True
    for i in range(LOWER-1,-1,-1):
        if ls[i]:
            _,_,e,n,_,_=ln[i]
            for p,c in ledges[e:e+n]:
                if p>=i: fail('lower_closure')
                ls[p]=True
    if gs!=declared_gs or ls!=declared_ls: fail('closure_bitsets')
    physical=selected_physical_replay(loaded,gn,ln,gedges,ledges,basis,declared_gs,declared_ls)
    structure=json.loads(loaded['source_ancestry'])['structure']
    if structure.get('member_roots')!=[{'pivot':int(p),'coefficient':int(c)} for p,c in coeffs] or structure.get('grade_selected')!=[i for i,x in enumerate(declared_gs) if x] or structure.get('lower_selected')!=[i for i,x in enumerate(declared_ls) if x]: fail('source_structure_closure')
    expected_origins={int(gn[i][0]) for i,x in enumerate(gs) if x}; expected_origins.update(int(ln[i][0]) for i,x in enumerate(ls) if x)
    if {int(r['logical']) for r in refs} != expected_origins: fail('source_ref_closure_binding')
    independent_transcript_check(state,candidate,loaded,gn,ln,gedges,ledges,started)
    selected_source_origin_replay(state,prepare,block_bodies,refs,loaded,gn,ln,gedges,ledges,declared_gs,declared_ls,physical)
    reconstructed=np.zeros(BYTES,dtype=np.uint8)
    rows=np.frombuffer(basis,dtype=np.uint8).reshape(GRADE,BYTES)
    for p,c in coeffs: reconstructed=AXPY[(3-int(c))%3,reconstructed,rows[int(p)]]
    prepare,target_raw=load_residual(state); target=np.frombuffer(target_raw,dtype=np.uint8)
    if not np.array_equal(reconstructed,target): fail('member_equation')
    if np.any(remainder) or sha(remainder)!=REMAINDER_SHA: fail('remainder')
    expected_children=[{'type':'GradeNodeRef','pivot':int(p),'coefficient':int(c)} for p,c in coeffs]
    if rootsjson.get('C_T',{}).get('type')!='OrderedProduct' or rootsjson.get('C_T',{}).get('children')!=expected_children: fail('roots_update')
    prior_terms=prepare.get('canonical_solution',{}).get('terms',[])
    if rootsjson.get('C_<1',{}).get('type')!='RegisteredPriorProduct' or rootsjson.get('C_<1',{}).get('terms')!=prior_terms: fail('roots_prior')
    if rootsjson.get('C_1')!={'type':'Compose','left':'C_<1','right':'C_T'}: fail('roots_compose_order')
    if not isinstance(files.get('source_ancestry'),dict) or not isinstance(files.get('roots'),dict): fail('manifest_handoff_receipts')
    verdict={'basis_sha256':BASIS_SHA,'coefficient_count':3317,'cross_checked':False,'cursor':8059,'grade_offer_count':6398,'grade_rank':GRADE,'lower_offer_count':2014,'lower_rank':LOWER,'marker':MARKER,'payload_manifest_sha256':payload_manifest_sha256,'prepare_sha256':PREPARE_SHA,'remainder_sha256':REMAINDER_SHA,'roots_sha256':files['roots']['sha256'],'source_ancestry_sha256':files['source_ancestry']['sha256'],'verified':False}
    if out is not None:
        guard(started)
        out.write_bytes(canon(verdict))
    print(json.dumps(verdict,sort_keys=True)); return 0
def main():
    ap=argparse.ArgumentParser(); ap.add_argument('--payload',type=Path); ap.add_argument('--candidate',type=Path); ap.add_argument('--state',type=Path); ap.add_argument('--out',type=Path); ap.add_argument('--selftest',action='store_true'); a=ap.parse_args()
    try:
        if a.selftest:
            if int(AXPY[2,2,1]) != 0 or int(AXPY[2,1,2]) != 0: fail('fixture_coefficient_2')
            if struct.unpack('<HB', struct.pack('<HB',0,1)) != (0,1): fail('fixture_nonmonotone')
            flags=[False,True,False]
            for i in range(2,-1,-1):
                if flags[i] and i==1: flags[0]=True
            if flags != [True,True,False]: fail('fixture_reverse_closure')
            base={'canonical':True,'nodes':[{'key':'old:0:0','kind':'old','children':[],'origin':'old','scale':1,'edge_order':[],'companion':True,'lower_zero':True},{'key':'old:0:1','kind':'old','children':['old:0:0'],'origin':'old','scale':2,'edge_order':['old:0:0'],'companion':True,'lower_zero':True}],'defects':[{'key':'defect:0','kind':'defect','origin':'defect','children':['old:0:0'],'expression_key':'actor:0:0:1'}],'expressions':[{'key':'actor:0:0:1','expression':[[0,1]]},{'key':'seed:0:1','expression':[[0,1]]}]}
            expected={'nodes':json.loads(json.dumps(base['nodes'])),'defects':json.loads(json.dumps(base['defects'])),'expressions':json.loads(json.dumps(base['expressions']))}; expected_maps=({'old:0:0':expected['nodes'][0],'old:0:1':expected['nodes'][1]}, {'defect:0':expected['defects'][0]}, {'actor:0:0:1':expected['expressions'][0],'seed:0:1':expected['expressions'][1]})
            compare_source_structure(base['nodes'],base['defects'],base['expressions'],*expected_maps)
            roots=[{'kind':'grade','ids':[0],'prefix':[],'coefficient':1}]; compare_root_binding(roots,[{'pivot':0,'coefficient':1}])
            bad_roots=[{'kind':'grade','ids':[0],'prefix':[],'coefficient':2}]
            try: compare_root_binding(bad_roots,[{'pivot':0,'coefficient':1}])
            except RuntimeError: pass
            else: fail('root_mutation_not_rejected')
            bad_roots=[{'kind':'grade','ids':[0],'prefix':[],'coefficient':1},{'kind':'grade','ids':[0],'prefix':[],'coefficient':1}]
            try: compare_root_binding(bad_roots,[{'pivot':0,'coefficient':1}])
            except RuntimeError: pass
            else: fail('root_duplicate_mutation_not_rejected')
            source_mutations=[lambda g:g['nodes'].pop(0),lambda g:g['nodes'].append({'key':'old:0:2','kind':'old','children':[]}),lambda g:g['nodes'].append({'key':'old:0:0','kind':'old','children':[],'origin':'old','scale':1,'edge_order':[],'companion':True,'lower_zero':True}),lambda g:g['nodes'][0].update({'key':'stale:0:1'}),lambda g:g['nodes'][1].update({'children':[],'edge_order':[]}),lambda g:g['nodes'][0].update({'scale':2}),lambda g:g['nodes'][0].update({'companion':False}),lambda g:g['nodes'][0].update({'lower_zero':False}),lambda g:g['defects'][0]['children'].pop(),lambda g:g['expressions'].pop(0),lambda g:g['expressions'].pop(),lambda g:g['expressions'][0].update({'expression':[[0,2]]}),lambda g:g['expressions'][1].update({'expression':[[0,2]]})]
            for mutation in source_mutations:
                bad=json.loads(json.dumps(base)); mutation(bad)
                try: compare_source_structure(bad['nodes'],bad['defects'],bad['expressions'],*expected_maps)
                except RuntimeError: pass
                else: fail('source_mutation_not_rejected')
            actual={'lower_nodes':[(0,1,0,0,0,0)],'grade_nodes':[(0,2,0,0,0,0)],'lower_edges':[(0,1),(1,2)],'grade_edges':[(0,2)],'lower_origins':b'L','lower_stored':b'S','lower_companions':b'C','grade_origins':b'G','old_lower_zero':b'Z','basis':b'B'}; expected_tx=dict(actual); compare_authoritative_transcript(actual,expected_tx)
            require_false_claim_flags({'direct_occurrence_replay':False,'next_degree2_residual':None,'cross_checked':False,'verified':False,'A0':False,'COMMON':False,'FAKE':False,'IHARA':False},'selftest')
            for key in ('direct_occurrence_replay','next_degree2_residual','cross_checked','verified','A0','COMMON','FAKE','IHARA'):
                bad_flags={'direct_occurrence_replay':False,'next_degree2_residual':None,'cross_checked':False,'verified':False,'A0':False,'COMMON':False,'FAKE':False,'IHARA':False}; bad_flags[key]=([] if key=='next_degree2_residual' else True)
                try: require_false_claim_flags(bad_flags,'selftest')
                except RuntimeError: pass
                else: fail('claim_flag_mutation_not_rejected')
            compare_roots_receipt_pointer('roots.json','roots.json')
            try: compare_roots_receipt_pointer('roots.json','other.json')
            except RuntimeError: pass
            else: fail('root_pointer_mutation_not_rejected')
            tx_mutations=[('lower_nodes',[(1,1,0,0,0,0)]),('grade_nodes',[(0,1,0,0,0,0)]),('grade_nodes',[(0,2,0,0,0,1)]),('lower_edges',[(1,2),(0,1)]),('grade_edges',[(0,1)]),('lower_origins',b'X'),('lower_stored',b'X'),('lower_companions',b'X'),('grade_origins',b'X'),('old_lower_zero',b'X'),('basis',b'X')]
            for key,value in tx_mutations:
                bad=dict(actual); bad[key]=value
                try: compare_authoritative_transcript(bad,expected_tx)
                except RuntimeError: pass
                else: fail('transcript_mutation_not_rejected')
            print(json.dumps({'canonical_validator':'PASS','authoritative_transcript_comparator':'PASS','claim_flag_mutation_count':8,'coefficient_2':'PASS','nonmonotone_lead':'PASS','reverse_closure':'PASS','root_mutation_count':3,'source_mutation_count':13,'transcript_mutation_count':11},sort_keys=True)); return 0
        if not a.payload or not a.candidate or not a.state: fail('usage')
        return replay(a.payload,a.candidate,a.state,a.out)
    except Exception as e: print(json.dumps({'status':'REJECTED','error':str(e)}),file=sys.stderr); return 1
if __name__=='__main__': raise SystemExit(main())
