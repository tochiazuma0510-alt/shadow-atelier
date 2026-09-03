#!/usr/bin/env python3
"""Phase-separated, componentwise semantic replay for the lazy P1 state."""
from __future__ import annotations
import argparse, hashlib, importlib.util, io, json, math, os, re, stat, sys, tempfile, time
from collections import deque
from pathlib import Path
import numpy as np

ROOT=Path(__file__).resolve().parents[1]
V4=ROOT/'search/d972_r07_a0_first_rung_grade1_v4.py'
V4_SHA='1fb4b29691f448782e7f7f2e2282e7067282bc619fb34b7214089c5a73e24dc4'
STRUCTURAL=ROOT/'search/d972_r07_grade2_specific_owner_prejoin_v1.py'
STRUCTURAL_SHA='38fcbe3757d1b14fd19f4f557f763c1f5f6a2e8da47e0e061707cf28c5064d73'
PREPARE_DIGEST='1f191d88a0453360021ec57d253a7d16c9a66ac059ddaaadb6db3e2b9293c865'
SOURCE_RUN='33677346616'; SOURCE_ATTEMPT='1'; SOURCE_HEAD='22c6dddb43d107c05e65f53ad898823ae8ebe276'
SERVICE={
 'prepare':(9865061266,'task554-grade1-v3-prepare-33677346616-1',204360988,'sha256:da8bfec6a03cac65de40ba8c4f79cde687fd2629edb3c3965fd972ecf96cc2f4'),
 'block0':(9865238399,'task554-grade1-v3-state-block-0-33677346616-1',81729645,'sha256:2a8e63a4270bf4052c7fd8763d7828fc17dd6b94c88854bacde1e94082cd5838'),
 'block1':(9865242284,'task554-grade1-v3-state-block-1-33677346616-1',82259824,'sha256:849321b79f0e3ea3c9a3f9c9dad43de2b3aaa571163456abc702476e322714fb'),
 'block2':(9865193269,'task554-grade1-v3-state-block-2-33677346616-1',82200189,'sha256:d2cdf8245d58a384bebfd516135e07930fe26c21c2c1cab130dfa6c3c7f2854d'),
 'block3':(9865239848,'task554-grade1-v3-state-block-3-33677346616-1',82266526,'sha256:87547101ede2fb48619a069de958c08cbb3cb0ee6c0990090234005aacd05b92')}
PARENTS={'block0':'9ebcc7ad1141c20aeaff82eb4a83a9489dc492b30220547f23526b4fcdd8dc74','block1':'d783bbe6c92c15a241eb78d0b25bca5e7c00f60799ce82f6df8b1d3ee7a202f6','block2':'a6dcc904fc3e9daae008f72de7e83ffadcd39055d557621b9cdf06baea0e83ac','block3':'642a4ec0ad6ad4ea659e84330e34006c767ca029203446cb64a17c151fefdb01'}
BASIS=('cc7e38114afc58e3aba10fa340a6ebd4f9a7a4752d5bb5fb9408ea8d84021e39','0223f72b7d2cb8a72f2ff99b8812fea977ed761c8505dab52ad3fba284b93461','602f23081aa609973860eac24d2f65104a9530c8ddf356d60a9d0378921b99f6','4ed4de15c00290f60e5fd2d57dd94db3103be92c602d92481f2835d9d96db0b9')
CHARACTERS=((0,0),(0,1),(1,0),(1,1)); ACTORS=(1,-1,2,-2)
PURE_WORDS_SHA='c2cd9825d30d95baead65aabbf16e88c8c3e277ef7ee9f1c28a38067f12177b4'
EQUALITY_RECORDS=(
 {'character_index':0,'record_sha256':'2a1f0b96effc5bb808d70303f63f78cbc4ef069d80290e5d2f24b072948fcee2','lower_sha256':'46beeda1dfca7a228eafc9fbf030eb3ccd87c5009c380bae39efa4d17dda7837','lifted_sha256':'08632b4f3c0a8b0163926d48b406a58417038e427c902da56391c57963b4ab2b'},
 {'character_index':1,'record_sha256':'2eb0b06da23e6bb45066cb9db0d0bf8c1d6676e6f85067c0eb9da48afa1149fa','lower_sha256':'8a37de95859793ef3c8321d18de09590c28ec5adbc9025e70f819426a8d89333','lifted_sha256':'14ea8ee3833f11250d18beac102b3e8b8d759ca13e0f8230069ece5f395cf364'},
 {'character_index':2,'record_sha256':'10725c2587ce2c9f8b19df2d62be48dd01a16349f60ad9c604b9fb278052a7df','lower_sha256':'ee6ee8c731be47024b9f6656a31100139ddc4ca685c568427d8fe90b172a60b4','lifted_sha256':'0609799f1bf4ba0fd534592c71ed22bee9c69b558930a4eddd745adf386076c4'},
 {'character_index':3,'record_sha256':'547720cf7162f84957a3f2c5bb7af42fe618641f3a89796814a577bb9ae57b7e','lower_sha256':'3b9be2ac16be5a4394c164f759a6e4414b65c597ee77d42830e33aeaa5fb0b48','lifted_sha256':'7a3f436f4f2e324f0784f40efb975c31a24d845c350b0819f61b727aead3bec5'},)
EQUALITY_SHA='99da0c4a42a0c747cde28cd91797d7c655d797c27f8f78a7423142bf56bc5dbf'
DAG_SHA=('b7dc7ca9d551e0e788ff48576c05fed30c95a1f54a60991415926f448c6fb115','5a35f0949436ef2998638f8ad0ab57d0feec2f44c5054c711d35d71d8edc3258','221c47b73a6ead9b7fe03640ca7e99fd2df68bf7a65328e7909933d04d45454b','2a2be062e35111faaf87bd303be80774dea76ec659bab0b59fe4678ad0d4e6e9')
CLAIMS={'A0':False,'COMMON':False,'COMPATIBLE_LIFT':False,'FAKE':False,'FULL_Q0':False,'IHARA':False,'ORDER_54432':False,'verified':False}

def sha(data): return hashlib.sha256(data).hexdigest()
def canonical(value): return (json.dumps(value,sort_keys=True,separators=(',',':'),ensure_ascii=True)+'\n').encode('ascii')
def fail(reason): raise RuntimeError(reason)
def require(ok,reason):
    if not ok: fail(reason)
def plain_int(x): return isinstance(x,int) and not isinstance(x,bool)
def load_module(path,expected,name):
    require(sha(path.read_bytes())==expected,'source_pin:'+path.name)
    spec=importlib.util.spec_from_file_location(name,path); require(spec is not None and spec.loader is not None,'module_loader')
    mod=importlib.util.module_from_spec(spec); marker=object(); previous=sys.modules.get(name,marker); sys.modules[name]=mod
    try: spec.loader.exec_module(mod)
    except BaseException:
        if previous is marker: sys.modules.pop(name,None)
        else: sys.modules[name]=previous
        raise
    return mod
def load_v4(): return load_module(V4,V4_SHA,'p1_v4')
def load_structural(): return load_module(STRUCTURAL,STRUCTURAL_SHA,'p1_structural')
def exact_root(root):
    info=root.lstat(); require(stat.S_ISDIR(info.st_mode) and not stat.S_ISLNK(info.st_mode) and not (getattr(info,'st_file_attributes',0)&0x400),'root_directory')
    names=[]
    for item in root.iterdir():
        st=item.lstat(); require(stat.S_ISREG(st.st_mode) and not stat.S_ISLNK(st.st_mode) and not (getattr(st,'st_file_attributes',0)&0x400),'unsafe_root_entry'); names.append(item.name)
    require(len(set(x.casefold() for x in names))==len(names),'root_case_collision')
    return names
def exact_roster(names,expected): require(set(names)==set(expected) and len(names)==len(expected),'root_roster')
def read_canonical(path):
    raw=path.read_bytes()
    try: value=json.loads(raw)
    except (ValueError,TypeError): fail('json')
    require(raw==canonical(value),'noncanonical_json'); return value,raw
def read_sealed(root,stem,digest,parent=None):
    hr,hr_raw=read_canonical(root/f'{stem}.HEAD'); require(hr=={'body_sha256':digest,'parent_sha256':parent,'schema':'d972.r07.a0.first-rung-grade1.v3.state.head','stem':stem},'sealed_head')
    body,body_raw=read_canonical(root/f'{stem}.{digest}.json'); require(sha(body_raw)==digest,'sealed_body_hash'); return body,body_raw
def exact_packet_stream(root,receipt,rows,width):
    require(isinstance(receipt,dict),'packet_receipt_shape'); path=root/receipt['file']; require(path.name==receipt['file'],'packet_name')
    expected=rows*(width//4); require(receipt.get('bytes')==expected and receipt.get('width')==width and receipt.get('rows')==rows and isinstance(receipt.get('sha256'),str) and re.fullmatch(r'[0-9a-f]{64}',receipt['sha256']),'packet_dimensions')
    before=path.stat(); h=hashlib.sha256(); count=0
    stream=path.open('rb')
    try:
        while True:
            chunk=stream.read(1<<20)
            if not chunk: break
            require(max(chunk,default=0)<=80,'packet_byte'); h.update(chunk); count+=len(chunk)
    finally: stream.close()
    after=path.stat(); require(count==expected and h.hexdigest()==receipt['sha256']==receipt.get('sha256'),'packet_digest')
    require((before.st_size,before.st_mtime_ns,before.st_ino)==(after.st_size,after.st_mtime_ns,after.st_ino),'packet_changed')
    return path
def seek_packet_range(stream,begin,end,row_bytes):
    require(plain_int(begin) and plain_int(end) and 0<=begin<=end,'packet_range')
    require(plain_int(row_bytes) and row_bytes>0,'packet_row_bytes')
    stream.seek(begin*row_bytes); require(stream.tell()==begin*row_bytes,'packet_seek')
    return end*row_bytes
def finish_packet_range(stream,end,row_bytes):
    require(stream.tell()==end*row_bytes,'packet_position')
def consume_packet_range(streams,begin,end,row_bytes,consumer):
    for stream in streams: seek_packet_range(stream,begin,end,row_bytes)
    for absolute in range(begin,end):
        rows=[]
        for stream in streams:
            raw=stream.read(row_bytes); require(len(raw)==row_bytes,'packet_range_eof'); rows.append(raw)
        consumer(absolute,rows)
    for stream in streams: finish_packet_range(stream,end,row_bytes)
def complete_actor_row(row):
    require(isinstance(row,list) and len(row)==4 and all(value is not None for value in row),'actor_row_complete')
    return row
def assert_projector_identity(v4,context):
    expected={ (0,0):(), (0,1):(-2,)*9, (1,0):(-2,-2,1,1,2,1,2,1,1), (1,1):(-2,-2,-2,-1,-2,-1,-1,-1,-2,-1)}
    require(v4.PURE_Q1_WORDS==expected,'pure_word_pin')
    for label in CHARACTERS:
        value=context.pure_source_affine[label]; require(isinstance(value,(tuple,list)) and len(value)>=3 and value[0]==v4.floor.ID9,'pure_q1_endpoint'); require(value[1]==label[0] and value[2]==label[1],'pure_q1_parity')
    table=[sum(v4.cv(label,a,b) for label in CHARACTERS)%3 for a,b in CHARACTERS]
    require(table==[1,0,0,0],'sum_projectors')
    return {'sum_chi_P_chi_mod3':1,'seed_reconstruction_count':44,'cv_sum_table':table,'cv_sum_table_sha256':sha(canonical(table)),'pure_words_sha256':sha(canonical([[list(x),list(expected[x])] for x in CHARACTERS]))}
def compare_bytes(actual,expected,reason): require(actual==expected,reason)
def compare_expression(actual,expected,reason): require(actual==expected,reason)
def compare_node(actual,expected,reason): require(actual==expected,reason)
def compare_actor_transition(actual,expected,reason): require(actual==expected,reason)
def shared_aux_check(lower,aux): require(lower[-len(aux):].tobytes()==aux.tobytes(),'shared_aux')
def validate_prior_expression(expression,pivot):
    require(isinstance(expression,list),'prior_expression_shape')
    for pair in expression:
        require(isinstance(pair,list) and len(pair)==2 and plain_int(pair[0]) and plain_int(pair[1]) and 0<=pair[0]<pivot and pair[1] in (1,2),'prior_expression')
def authenticated_prepare(v4,root,packet_indices=range(4)):
    names=exact_root(root)
    body,raw=read_sealed(root,'prepare',PREPARE_DIGEST,None)
    receipt=v4.load_pinned_inputs()[1]
    v4.validate_prepare_state(root,body,receipt,fixture=False,authenticate_residual=True,authenticate_old=True,authenticate_packets=packet_indices)
    expected={'prepare.HEAD',f'prepare.{PREPARE_DIGEST}.json'}
    for row in body['old_blocks']: expected|={row['lower_basis_blob']['file'],row['lifted_grade_blob']['file']}
    expected|={row['blob']['file'] for row in body['packets']}; expected|={body['residual_blob']['file']}; exact_roster(names,expected)
    return body,raw,receipt
def replay_prepare(root):
    started=time.monotonic(); v4=load_v4(); body,raw,receipt=authenticated_prepare(v4,root)
    words=json.loads((ROOT/'scratchpad/a0_paper_words_v1.json').read_text(encoding='utf-8')); context=v4.Context(words); projector=assert_projector_identity(v4,context)
    base=[v4.evaluate_occurrence_pair(tuple(map(int,w)),context) for w in words['relators']]; require(len(base)==44,'seed_count')
    seconds=float(os.environ.get('TASK709_SECONDS','21600')); rss=int(os.environ.get('TASK709_MAX_RSS',str(8*1024**3)))
    old_rank=0; actor_count=0; seed_count=0; dag_count=0; equality=[]
    packet_paths=[exact_packet_stream(root,body['packets'][p]['blob'],len(body['defect_origins']),v4.SOURCE_BLOCK_WIDTH) for p in range(4)]
    streams=[path.open('rb') for path in packet_paths]; cursor=0
    try:
      for ci,label in enumerate(CHARACTERS):
        projected=[v4.projected_seed_pair(context,base[s],label) for s in range(44)]
        seeds=[]; grades=[]
        for pair in projected:
            row=np.zeros(v4.LOWER_ECHELON_WIDTH,dtype=np.uint8); row[:v4.SOURCE_BASE_WIDTH]=pair[0][ci]; row[v4.SOURCE_BASE_WIDTH:]=pair[2]; shared_aux_check(row,pair[2]); seeds.append(row); grades.append(pair[1].reshape(v4.SOURCE_TOTAL_WIDTH))
        owner,record=v4.close_lower_block(context,label,seeds,started,seconds,rss); expected=body['old_blocks'][ci]
        compare_node(record,expected['record'],'old_record_replay'); compare_bytes(owner.matrix_bytes(),v4.read_blob(root,expected['lower_basis_blob']),'old_lower_bytes')
        lower_bytes=owner.matrix_bytes(); lifted_expected=v4.read_blob(root,expected['lifted_grade_blob']); lifts=v4.evaluate_old_lifts(context,label,owner,record,grades,started,seconds,rss); lifted_bytes=v4.packed_matrix_bytes(lifts); compare_bytes(lifted_bytes,lifted_expected,'old_lift_bytes'); equality.append({'character_index':ci,'record_sha256':sha(canonical(record)),'lower_sha256':sha(lower_bytes),'lifted_sha256':sha(lifted_bytes)})
        origin_range=expected['defect_origin_range']; require(isinstance(origin_range,list) and len(origin_range)==2,'prepare_origin_range_shape'); begin,end=origin_range
        span=44+4*len(owner.rows); require(end-begin==span and begin==cursor,'prepare_origin_range_binding'); cursor=end
        def consume(absolute,rows):
            nonlocal seed_count,actor_count
            local=absolute-begin
            if local<44:
                work=projected[local][1].reshape(v4.SOURCE_TOTAL_WIDTH).copy()
                for pivot,coefficient in record['seed_reductions'][local]: v4._add_mod3(work,lifts[int(pivot)],-int(coefficient))
                for p,raw_row in enumerate(rows): compare_bytes(v4.pack_trits(work.reshape(4,v4.SOURCE_BLOCK_WIDTH)[p]).tobytes(),raw_row,'seed_packet_bytes')
                seed_count+=1
            else:
                actor_index=local-44; pivot,ai=divmod(actor_index,4); lower=owner.dense_row(pivot); work=v4.exact_actor_on_old_lift(context,lower,lifts[pivot],label,ACTORS[ai])
                for earlier,coefficient in record['actor_transitions'][pivot][ai]: v4._add_mod3(work,lifts[int(earlier)],-int(coefficient))
                for p,raw_row in enumerate(rows): compare_bytes(v4.pack_trits(work.reshape(4,v4.SOURCE_BLOCK_WIDTH)[p]).tobytes(),raw_row,'actor_packet_bytes')
                actor_count+=1
        consume_packet_range(streams,begin,end,v4.SOURCE_BLOCK_WIDTH//4,consume)
        old_rank+=len(owner.rows); dag_count+=len(record['dag_nodes'])
      for stream in streams: require(not stream.read(1),'prepare_packet_trailing')
    finally:
        for stream in streams: stream.close()
    require(cursor==len(body['defect_origins']),'prepare_origin_cursor')
    require((old_rank,dag_count,seed_count,actor_count)==(2014,2014,176,8056),'prepare_counts')
    validate_equality_receipts(equality); require(sha(canonical(equality))==EQUALITY_SHA,'prepare_equality_digest')
    peak=v4.rss_bytes() if hasattr(v4,'rss_bytes') else None
    return {'schema':'d972.r07.p1.componentwise.prepare.v1','phase':'prepare','producer_sha256':sha(Path(__file__).read_bytes()),'source_run':SOURCE_RUN,'source_attempt':SOURCE_ATTEMPT,'source_head':SOURCE_HEAD,'prepare_body_sha256':PREPARE_DIGEST,'input_manifest_sha256':sha(canonical(receipt)),'counts':{'old_ranks':2014,'old_dag_nodes':2014,'old_seed_lower':176,'old_actor_lower':8056,'direct_packet_halves':32928},'equality_receipts':equality,'equality_receipts_sha256':EQUALITY_SHA,'projector_identity':projector,'downstream_claim_flags':dict(CLAIMS),'resident_global_matrix':False,'independent_checker':False,'precision2':False,'A0':False,'COMMON':False,'COMPATIBLE_LIFT':False,'FAKE':False,'IHARA':False,'verified':False,'elapsed_seconds':time.monotonic()-started,'peak_rss_bytes':peak}
def validate_block_request(index,parent=PREPARE_DIGEST):
    require(plain_int(index) and index in range(4),'block_index'); require(parent==PREPARE_DIGEST,'block_ancestry')
def block_envelope(root,index,prepare,v4,structural):
    validate_block_request(index); safe_root,body,body_bytes=structural.validate_block_envelope(root,index,prepare); structural.validate_block_semantics(body,prepare,index,(1509,1512,1512,1512)[index]); require(body['basis_blob']['sha256']==BASIS[index],'block_basis_pin'); return safe_root,body,body_bytes
def replay_block_kernel(v4,context,label,owner,packet_rows,body,width=18144):
    row_bytes=width//4; queue=deque(); nodes=[]; origins=[]; transitions=[]
    for origin,raw_row in enumerate(packet_rows):
        require(len(raw_row)==row_bytes,'packet_eof'); inserted=owner.insert(v4.unpack_trits(np.frombuffer(raw_row,dtype=np.uint8),width)); origins.append(v4.expression_from_insert(inserted)); compare_expression(origins[-1],body['origin_reductions'][origin],'packet_expression')
        if inserted['accepted']:
            pivot=int(inserted['pivot']); node={'pivot':pivot,'lead':int(inserted['lead']),'scale':int(inserted['scale']),'origin':{'kind':'defect','origin':origin},'reductions':inserted['reductions']}; nodes.append(node); compare_node(node,body['dag_nodes'][pivot],'packet_dag_node'); transitions.append([None]*4); queue.append(pivot)
    require(len(origins)==8232,'packet_row_count')
    while queue:
        pivot=queue.popleft(); parent=owner.dense_row(pivot); row=[None]*4
        for ai,letter in enumerate(ACTORS):
            inserted=owner.insert(v4.associated_grade_actor(context,parent,label,letter)); expression=v4.expression_from_insert(inserted); row[ai]=expression; compare_actor_transition(expression,body['actor_transitions'][pivot][ai],'actor_transition')
            if inserted['accepted']:
                child=int(inserted['pivot']); node={'pivot':child,'lead':int(inserted['lead']),'scale':int(inserted['scale']),'origin':{'kind':'actor','parent':pivot,'letter':letter},'reductions':inserted['reductions']}; nodes.append(node); compare_node(node,body['dag_nodes'][child],'actor_dag_node'); transitions.append([None]*4); queue.append(child)
        transitions[pivot]=complete_actor_row(row)
    return origins,nodes,transitions
def replay_block(prep_root,root,index):
    started=time.monotonic(); v4=load_v4(); structural=load_structural(); prepare,_,_=authenticated_prepare(v4,prep_root,(index,)); safe_root,body,body_bytes=block_envelope(root,index,prepare,v4,structural)
    label=CHARACTERS[index]; packet=prepare['packets'][index]; packet_path=exact_packet_stream(prep_root,packet['blob'],8232,v4.SOURCE_BLOCK_WIDTH); owner=v4.PackedEchelon(v4.SOURCE_BLOCK_WIDTH); context=v4.context_for_state(prepare)
    with packet_path.open('rb') as stream:
        def packet_rows():
            while True:
                raw_row=stream.read(v4.SOURCE_BLOCK_WIDTH//4)
                if not raw_row: return
                yield raw_row
        origins,nodes,transitions=replay_block_kernel(v4,context,label,owner,packet_rows(),body,v4.SOURCE_BLOCK_WIDTH); require(not stream.read(1),'packet_trailing')
    for node in nodes: validate_prior_expression(node['reductions'],node['pivot'])
    require(len(nodes)==len(body['dag_nodes']) and len(owner.rows)==(1509,1512,1512,1512)[index],'block_rank'); require(origins==body['origin_reductions'] and transitions==body['actor_transitions'],'block_expression_replay'); require(sha(canonical(nodes))==body['dag_sha256'],'block_dag_digest')
    require(body['dag_sha256']==DAG_SHA[index],'block_dag_pin')
    basis=body['basis_blob']; compare_bytes(owner.matrix_bytes(),v4.read_blob(safe_root,basis),'block_basis_bytes')
    n=len(owner.rows); peak=v4.rss_bytes() if hasattr(v4,'rss_bytes') else None; return {'schema':'d972.r07.p1.componentwise.block.v1','phase':'block','producer_sha256':sha(Path(__file__).read_bytes()),'source_run':SOURCE_RUN,'source_attempt':SOURCE_ATTEMPT,'source_head':SOURCE_HEAD,'prepare_body_sha256':PREPARE_DIGEST,'block_index':index,'block_body_sha256':PARENTS[f'block{index}'],'basis_sha256':BASIS[index],'counts':{'packet_basis_halves':8232,'new_actor_identities':4*n,'new_dag_identities':n,'compound_obligations':8232+4*n},'rank':n,'attempts':8232+4*n,'dag_sha256':body['dag_sha256'],'downstream_claim_flags':dict(CLAIMS),'resident_global_matrix':False,'independent_checker':False,'precision2':False,'A0':False,'COMMON':False,'COMPATIBLE_LIFT':False,'FAKE':False,'IHARA':False,'verified':False,'elapsed_seconds':time.monotonic()-started,'peak_rss_bytes':peak}
FALSE_FLAGS=('resident_global_matrix','independent_checker','precision2','A0','COMMON','COMPATIBLE_LIFT','FAKE','IHARA','verified')
def digest_string(value,reason):
    require(isinstance(value,str) and re.fullmatch(r'[0-9a-f]{64}',value) is not None,reason)
def exact_false_flags(value,reason):
    require(isinstance(value,dict) and set(value)==set(CLAIMS),reason+'_keys')
    for key in CLAIMS: require(value[key] is False,reason+'_'+key)
def exact_telemetry(value):
    elapsed=value.get('elapsed_seconds'); peak=value.get('peak_rss_bytes')
    require((isinstance(elapsed,(int,float)) and not isinstance(elapsed,bool) and math.isfinite(float(elapsed)) and elapsed>=0),'receipt_elapsed')
    require(peak is None or (plain_int(peak) and peak>=0),'receipt_peak')
def validate_equality_receipts(value):
    require(isinstance(value,list) and len(value)==4,'equality_records')
    for index,record in enumerate(value):
        require(isinstance(record,dict) and set(record)=={'character_index','record_sha256','lower_sha256','lifted_sha256'},'equality_record_keys')
        require(plain_int(record['character_index']) and record['character_index']==index,'equality_record_index')
        for key in ('record_sha256','lower_sha256','lifted_sha256'): digest_string(record[key],'equality_'+key)
        require(record==EQUALITY_RECORDS[index],'equality_record_pin')
def validate_projector(value):
    require(isinstance(value,dict) and set(value)=={'sum_chi_P_chi_mod3','seed_reconstruction_count','cv_sum_table','cv_sum_table_sha256','pure_words_sha256'},'projector_keys')
    require(plain_int(value['sum_chi_P_chi_mod3']) and value['sum_chi_P_chi_mod3']==1,'projector_sum')
    require(plain_int(value['seed_reconstruction_count']) and value['seed_reconstruction_count']==44,'projector_seed_count')
    require(value['cv_sum_table']==[1,0,0,0],'projector_table')
    require(value['cv_sum_table_sha256']==sha(canonical([1,0,0,0])),'projector_table_digest')
    require(value['pure_words_sha256']==PURE_WORDS_SHA,'projector_words_digest')
def validate_prepare_receipt(value,producer):
    require(value.get('schema')=='d972.r07.p1.componentwise.prepare.v1' and value.get('phase')=='prepare','prepare_receipt_phase')
    require(value.get('producer_sha256')==producer,'prepare_receipt_producer')
    require(value.get('source_run')==SOURCE_RUN and isinstance(value.get('source_run'),str),'prepare_source_run')
    require(value.get('source_attempt')==SOURCE_ATTEMPT and isinstance(value.get('source_attempt'),str),'prepare_source_attempt')
    require(value.get('source_head')==SOURCE_HEAD and isinstance(value.get('source_head'),str),'prepare_source_head')
    require(value.get('prepare_body_sha256')==PREPARE_DIGEST,'prepare_body_digest'); digest_string(value.get('input_manifest_sha256'),'prepare_manifest')
    counts=value.get('counts'); require(isinstance(counts,dict) and set(counts)=={'old_ranks','old_dag_nodes','old_seed_lower','old_actor_lower','direct_packet_halves'},'prepare_counts_keys')
    expected={'old_ranks':2014,'old_dag_nodes':2014,'old_seed_lower':176,'old_actor_lower':8056,'direct_packet_halves':32928}
    for key,want in expected.items(): require(plain_int(counts[key]) and counts[key]==want,'prepare_count_'+key)
    validate_equality_receipts(value.get('equality_receipts')); require(sha(canonical(value['equality_receipts']))==EQUALITY_SHA,'equality_digest_value'); require(value.get('equality_receipts_sha256')==EQUALITY_SHA,'equality_digest_pin')
    validate_projector(value.get('projector_identity')); exact_false_flags(value.get('downstream_claim_flags'),'prepare_flags')
    for key in FALSE_FLAGS: require(value.get(key) is False,'prepare_flag_'+key)
    exact_telemetry(value)
def validate_block_receipt(value,index,producer):
    require(value.get('schema')=='d972.r07.p1.componentwise.block.v1' and value.get('phase')=='block','block_receipt_phase')
    require(value.get('producer_sha256')==producer,'block_receipt_producer')
    require(value.get('source_run')==SOURCE_RUN and isinstance(value.get('source_run'),str),'block_source_run')
    require(value.get('source_attempt')==SOURCE_ATTEMPT and isinstance(value.get('source_attempt'),str),'block_source_attempt')
    require(value.get('source_head')==SOURCE_HEAD and isinstance(value.get('source_head'),str),'block_source_head')
    require(value.get('prepare_body_sha256')==PREPARE_DIGEST,'block_prepare_digest'); require(value.get('block_index')==index and plain_int(value.get('block_index')),'block_index_value')
    require(value.get('block_body_sha256')==PARENTS[f'block{index}'],'block_parent_digest'); require(value.get('basis_sha256')==BASIS[index],'block_basis_digest')
    rank=value.get('rank'); expected_rank=(1509,1512,1512,1512)[index]; require(plain_int(rank) and rank==expected_rank,'block_rank_value'); require(plain_int(value.get('attempts')) and value['attempts']==8232+4*rank,'block_attempts')
    require(value.get('dag_sha256')==DAG_SHA[index],'block_dag_digest')
    counts=value.get('counts'); require(isinstance(counts,dict) and set(counts)=={'packet_basis_halves','new_actor_identities','new_dag_identities','compound_obligations'},'block_counts_keys')
    expected_counts={'packet_basis_halves':8232,'new_actor_identities':4*rank,'new_dag_identities':rank,'compound_obligations':8232+4*rank}
    for key,want in expected_counts.items(): require(plain_int(counts[key]) and counts[key]==want,'block_count_'+key)
    exact_false_flags(value.get('downstream_claim_flags'),'block_flags')
    for key in FALSE_FLAGS: require(value.get(key) is False,'block_flag_'+key)
    exact_telemetry(value)
def exact_receipt(path,allowed):
    value,raw=read_canonical(path); require(isinstance(value,dict) and set(value)==allowed,'receipt_keys'); require(value.get('producer_sha256')==sha(Path(__file__).read_bytes()),'receipt_producer'); return value
def validate_join_indices(indices): require(isinstance(indices,list) and len(indices)==4 and all(plain_int(x) for x in indices) and indices==[0,1,2,3],'join_indices')
def validate_join_receipts(prepare,blocks):
    producer=sha(Path(__file__).read_bytes()); validate_prepare_receipt(prepare,producer)
    require(len(blocks)==4,'join_block_count')
    for index,value in enumerate(blocks): validate_block_receipt(value,index,producer)
    validate_join_indices([x['block_index'] for x in blocks]); require(all(x['prepare_body_sha256']==prepare['prepare_body_sha256'] for x in blocks),'join_parent'); require(all(x['source_run']==prepare['source_run'] and x['source_attempt']==prepare['source_attempt'] and x['source_head']==prepare['source_head'] for x in blocks),'join_source_ancestry'); require(all(x['block_body_sha256']==PARENTS[f"block{x['block_index']}"] and x['basis_sha256']==BASIS[x['block_index']] for x in blocks),'join_artifact_ancestry'); require(all(x['downstream_claim_flags']==CLAIMS for x in blocks) and prepare['downstream_claim_flags']==CLAIMS,'join_claims')
    require(prepare['projector_identity']['cv_sum_table']==[1,0,0,0] and prepare['projector_identity']['cv_sum_table_sha256']==sha(canonical([1,0,0,0])),'join_projector_identity')
    require(prepare['counts']=={'old_ranks':2014,'old_dag_nodes':2014,'old_seed_lower':176,'old_actor_lower':8056,'direct_packet_halves':32928},'join_prepare_counts'); require(sum(x['rank'] for x in blocks)==6045 and sum(x['counts']['new_dag_identities'] for x in blocks)==6045,'join_block_counts'); require(sum(x['counts']['packet_basis_halves'] for x in blocks)==32928 and sum(x['counts']['new_actor_identities'] for x in blocks)==24180 and sum(x['counts']['compound_obligations'] for x in blocks)==57108 and 8232+32928+24180==65340,'join_obligation_counts')
def join(paths):
    require(len(paths)==5,'join_count'); prepare=exact_receipt(paths[0],{'schema','phase','producer_sha256','source_run','source_attempt','source_head','prepare_body_sha256','input_manifest_sha256','counts','equality_receipts','equality_receipts_sha256','projector_identity','downstream_claim_flags','resident_global_matrix','independent_checker','precision2','A0','COMMON','COMPATIBLE_LIFT','FAKE','IHARA','verified','elapsed_seconds','peak_rss_bytes'}); blocks=[exact_receipt(p,{'schema','phase','producer_sha256','source_run','source_attempt','source_head','prepare_body_sha256','block_index','block_body_sha256','basis_sha256','counts','rank','attempts','dag_sha256','downstream_claim_flags','resident_global_matrix','independent_checker','precision2','A0','COMMON','COMPATIBLE_LIFT','FAKE','IHARA','verified','elapsed_seconds','peak_rss_bytes'}) for p in paths[1:]]
    validate_join_receipts(prepare,blocks); v4=load_v4(); receipt=v4.load_pinned_inputs()[1]; require(prepare['input_manifest_sha256']==sha(canonical(receipt)),'join_manifest_digest'); projector=assert_projector_identity(v4,v4.Context(json.loads((ROOT/'scratchpad/a0_paper_words_v1.json').read_text(encoding='utf-8')))); require(prepare['projector_identity']==projector,'join_projector_receipt')
    return {'schema':'d972.r07.p1.componentwise.v1','terminal':'TASK554_P1_COMPONENTWISE_SEMANTICS_REPLAYED','global_relations':32280,'old_ranks':2014,'new_ranks':6045,'dag_nodes':8059,'old_local_relations':8232,'direct_packet_halves':32928,'packet_basis_halves':32928,'new_actor_identities':24180,'compound_obligations':65340,'resident_global_matrix':False,'independent_checker':False,'precision2':False,'A0':False,'COMMON':False,'COMPATIBLE_LIFT':False,'FAKE':False,'IHARA':False,'verified':False,'producer_sha256':prepare['producer_sha256']}
def expect_reject(call):
    try: call()
    except RuntimeError: return 1
    fail('fixture_accept')
def _fixture_receipts():
    producer=sha(Path(__file__).read_bytes()); equality=[dict(record) for record in EQUALITY_RECORDS]
    projector={'sum_chi_P_chi_mod3':1,'seed_reconstruction_count':44,'cv_sum_table':[1,0,0,0],'cv_sum_table_sha256':sha(canonical([1,0,0,0])),'pure_words_sha256':PURE_WORDS_SHA}
    flags=dict(CLAIMS); prepare={'schema':'d972.r07.p1.componentwise.prepare.v1','phase':'prepare','producer_sha256':producer,'source_run':SOURCE_RUN,'source_attempt':SOURCE_ATTEMPT,'source_head':SOURCE_HEAD,'prepare_body_sha256':PREPARE_DIGEST,'input_manifest_sha256':'b'*64,'counts':{'old_ranks':2014,'old_dag_nodes':2014,'old_seed_lower':176,'old_actor_lower':8056,'direct_packet_halves':32928},'equality_receipts':equality,'equality_receipts_sha256':EQUALITY_SHA,'projector_identity':projector,'downstream_claim_flags':flags,'resident_global_matrix':False,'independent_checker':False,'precision2':False,'A0':False,'COMMON':False,'COMPATIBLE_LIFT':False,'FAKE':False,'IHARA':False,'verified':False,'elapsed_seconds':0.0,'peak_rss_bytes':0}
    ranks=(1509,1512,1512,1512); blocks=[]
    for i,rank in enumerate(ranks): blocks.append({'schema':'d972.r07.p1.componentwise.block.v1','phase':'block','producer_sha256':producer,'source_run':SOURCE_RUN,'source_attempt':SOURCE_ATTEMPT,'source_head':SOURCE_HEAD,'prepare_body_sha256':PREPARE_DIGEST,'block_index':i,'block_body_sha256':PARENTS[f'block{i}'],'basis_sha256':BASIS[i],'counts':{'packet_basis_halves':8232,'new_actor_identities':4*rank,'new_dag_identities':rank,'compound_obligations':8232+4*rank},'rank':rank,'attempts':8232+4*rank,'dag_sha256':DAG_SHA[i],'downstream_claim_flags':dict(flags),'resident_global_matrix':False,'independent_checker':False,'precision2':False,'A0':False,'COMMON':False,'COMPATIBLE_LIFT':False,'FAKE':False,'IHARA':False,'verified':False,'elapsed_seconds':0.0,'peak_rss_bytes':0})
    return prepare,blocks
def _fixture_projector():
    expected={(0,0):(),(0,1):(-2,)*9,(1,0):(-2,-2,1,1,2,1,2,1,1),(1,1):(-2,-2,-2,-1,-2,-1,-1,-1,-2,-1)}
    marker=object()
    class Floor: ID9=marker
    class V4:
        PURE_Q1_WORDS=expected; floor=Floor()
        @staticmethod
        def cv(label,a,b): return 1 if ((label[0]*a+label[1]*b)&1)==0 else 2
    class Context: pure_source_affine={label:(marker,label[0],label[1]) for label in CHARACTERS}
    return V4,Context
def validate_cli(args):
    phases=(args.selftest,args.prepare_replay is not None,args.block_replay is not None,args.join_receipts is not None)
    require(sum(1 for selected in phases if selected)==1,'phase_selection')
    require((args.index is not None)==(args.block_replay is not None),'index_phase')
def selftest():
    accepted=0; rejected=0; reached=[]
    expected=[[1,2],[3,1]]; compare_bytes(expected,expected,'fixture_packet'); accepted+=1
    rejected+=expect_reject(lambda: compare_bytes(b'raw',b'grade','fixture_packet_sign_raw'))
    rejected+=expect_reject(lambda: compare_bytes(bytes([0]),bytes([1]),'fixture_packet_byte'))
    rejected+=expect_reject(lambda: compare_expression([[0,1]],[[0,2]],'fixture_expression_coefficient'))
    rejected+=expect_reject(lambda: validate_prior_expression([[1,1]],1))
    rejected+=expect_reject(lambda: compare_actor_transition([[0,1]],[[1,1]],'fixture_actor_transition'))
    a=np.zeros(4,dtype=np.uint8); b=np.ones(2,dtype=np.uint8); rejected+=expect_reject(lambda: shared_aux_check(a,b))
    rejected+=expect_reject(lambda: validate_block_request(4))
    rejected+=expect_reject(lambda: validate_block_request(0,'wrong-parent'))
    rejected+=expect_reject(lambda: validate_join_indices([0,1,1,3]))
    rejected+=expect_reject(lambda: validate_join_indices([0,1,2]))
    rejected+=expect_reject(lambda: require(plain_int(False),'fixture_bool_as_int'))
    with tempfile.TemporaryDirectory() as td:
        toy=Path(td); (toy/'toy.bin').write_bytes(b'fixture'); exact_root(toy); reached.append('exact_root')
        rejected+=expect_reject(lambda: exact_root(toy/'toy.bin'))
        packet=io.BytesIO(bytes(range(4))); seen=[]; consume_packet_range([packet],0,2,1,lambda absolute,rows: seen.append((absolute,rows[0]))); consume_packet_range([packet],2,4,1,lambda absolute,rows: seen.append((absolute,rows[0]))); require(seen==[(0,b'\x00'),(1,b'\x01'),(2,b'\x02'),(3,b'\x03')],'fixture_packet_range'); require(not packet.read(1),'fixture_packet_eof'); reached.append('prepare_packet_range')
        rejected+=expect_reject(lambda: finish_packet_range(io.BytesIO(bytes(20)),5,2))
        body={'basis_blob':{'sha256':BASIS[0]}}
        class StructuralFixture:
            @staticmethod
            def validate_block_envelope(root,index,prepare): return root,body,17
            @staticmethod
            def validate_block_semantics(body,prepare,index,rank): return None
        safe,_,body_bytes=block_envelope(toy,0,{},None,StructuralFixture); require(safe==toy and body_bytes==17,'fixture_block_envelope'); reached.append('block_envelope')
    slots=[None]*4
    for index in range(4): slots[index]=[]
    complete_actor_row(slots); reached.append('actor_row')
    rejected+=expect_reject(lambda: complete_actor_row([[],None,[],[]]))
    class KernelOwner:
        def __init__(self): self.calls=0; self.rows=[np.zeros(1,dtype=np.uint8)]
        def insert(self,value):
            self.calls+=1
            if self.calls==1: return {'accepted':True,'pivot':0,'lead':0,'scale':1,'reductions':[]}
            return {'accepted':False,'reductions':[]}
        def dense_row(self,pivot): return np.zeros(1,dtype=np.uint8)
    class KernelV4:
        SOURCE_BLOCK_WIDTH=4
        @staticmethod
        def unpack_trits(value,width): return value
        @staticmethod
        def expression_from_insert(inserted): return inserted['reductions']
        @staticmethod
        def associated_grade_actor(context,row,label,letter): return np.zeros(1,dtype=np.uint8)
    kernel_body={'origin_reductions':[[] for _ in range(8232)],'actor_transitions':[[[],[],[],[]]],'dag_nodes':[{'pivot':0,'lead':0,'scale':1,'origin':{'kind':'defect','origin':0},'reductions':[]}]}
    kernel_owner=KernelOwner(); kernel_result=replay_block_kernel(KernelV4(),None,(0,0),kernel_owner,[b'\x00']*8232,kernel_body,4); require(len(kernel_result[0])==8232 and len(kernel_result[1])==1 and kernel_result[2]==[[[],[],[],[]]],'fixture_block_kernel'); reached.append('block_replay_kernel')
    projector_v4,projector_context=_fixture_projector(); projector=assert_projector_identity(projector_v4,projector_context); validate_projector(projector); reached.append('projector_identity')
    class BadProjector:
        PURE_Q1_WORDS=projector_v4.PURE_Q1_WORDS; floor=projector_v4.floor
        @staticmethod
        def cv(label,a,b): return 1
    rejected+=expect_reject(lambda: assert_projector_identity(BadProjector(),projector_context))
    class BadContext:
        pure_source_affine=dict(projector_context.pure_source_affine)
    BadContext.pure_source_affine[(0,1)]=(projector_v4.floor.ID9,0,0)
    rejected+=expect_reject(lambda: assert_projector_identity(projector_v4,BadContext()))
    prepare,blocks=_fixture_receipts(); validate_join_receipts(prepare,blocks); accepted+=1; reached.append('join_receipt_validator')
    altered=json.loads(json.dumps(prepare)); altered['counts']['old_seed_lower']=175; rejected+=expect_reject(lambda: validate_join_receipts(altered,blocks))
    altered=json.loads(json.dumps(prepare)); altered['equality_receipts'][0]['character_index']=True; rejected+=expect_reject(lambda: validate_join_receipts(altered,blocks))
    altered=json.loads(json.dumps(prepare)); altered['projector_identity']['cv_sum_table']=[1,1,0,0]; rejected+=expect_reject(lambda: validate_join_receipts(altered,blocks))
    altered=json.loads(json.dumps(blocks)); altered[1]['rank']=False; rejected+=expect_reject(lambda: validate_join_receipts(prepare,altered))
    altered=json.loads(json.dumps(blocks)); altered[2]['downstream_claim_flags']['A0']=True; rejected+=expect_reject(lambda: validate_join_receipts(prepare,altered))
    altered=json.loads(json.dumps(prepare)); altered['elapsed_seconds']=False; rejected+=expect_reject(lambda: validate_join_receipts(altered,blocks))
    altered=json.loads(json.dumps(prepare)); altered['source_head']='0'*40; rejected+=expect_reject(lambda: validate_join_receipts(altered,blocks))
    altered=json.loads(json.dumps(blocks)); altered[3]['attempts']=True; rejected+=expect_reject(lambda: validate_join_receipts(prepare,altered))
    altered=json.loads(json.dumps(blocks)); altered[0]['dag_sha256']='f'*64; rejected+=expect_reject(lambda: validate_join_receipts(prepare,altered))
    altered=json.loads(json.dumps(prepare)); altered['equality_receipts'][0]['lower_sha256']='f'*64; altered['equality_receipts_sha256']=sha(canonical(altered['equality_receipts'])); rejected+=expect_reject(lambda: validate_join_receipts(altered,blocks))
    altered=json.loads(json.dumps(prepare)); altered['equality_receipts_sha256']='f'*64; rejected+=expect_reject(lambda: validate_join_receipts(altered,blocks))
    def cli(selftest=False,prepare=None,block=None,join_paths=None,index=None): return argparse.Namespace(selftest=selftest,prepare_replay=prepare,block_replay=block,join_receipts=join_paths,index=index)
    validate_cli(cli(selftest=True)); rejected+=expect_reject(lambda: validate_cli(cli(selftest=True,index=0))); rejected+=expect_reject(lambda: validate_cli(cli(prepare=Path('fixture'),index=0))); rejected+=expect_reject(lambda: validate_cli(cli(join_paths=[Path(str(i)) for i in range(5)],index=0))); rejected+=expect_reject(lambda: validate_cli(cli(block=[Path('a'),Path('b')]))); rejected+=expect_reject(lambda: validate_cli(cli())); rejected+=expect_reject(lambda: validate_cli(cli(prepare=Path('fixture'),join_paths=[Path(str(i)) for i in range(5)]))); reached.append('cli_validator')
    with tempfile.TemporaryDirectory() as td:
        noncanonical=Path(td)/'noncanonical.json'; noncanonical.write_bytes(b'{"x": 0}')
        rejected+=expect_reject(lambda: read_canonical(noncanonical))
    print(json.dumps({'status':'PASS','fixture_accept':accepted,'rejections':rejected,'live_entry_points':reached,'valid_hex_dag_mutation':'REJECT','coordinated_equality_mutation':'REJECT','noncanonical_equality_aggregate':'REJECT','forbidden_index_combinations':'REJECT','packet_sign_raw_grade':'REJECT','packet_byte_mutation':'REJECT','expression_coefficient':'REJECT','dag_forward_edge':'REJECT','actor_transition':'REJECT','shared_aux_omission':'REJECT','wrong_block_index':'REJECT','wrong_ancestry':'REJECT','duplicate_join':'REJECT','missing_join':'REJECT','bool_as_int':'REJECT','noncanonical_receipt':'REJECT','actual_replay':'DEFERRED_TO_GHA','verified':False},sort_keys=True))
def main():
    p=argparse.ArgumentParser(); p.add_argument('--selftest',action='store_true'); p.add_argument('--prepare-replay',type=Path); p.add_argument('--block-replay',nargs=2,metavar=('PREP_ROOT','BLOCK_ROOT'),type=Path); p.add_argument('--index',type=int); p.add_argument('--join-receipts',nargs=5,type=Path); a=p.parse_args()
    try:
        validate_cli(a)
        if a.selftest: selftest(); return 0
        if a.prepare_replay and not a.block_replay and not a.join_receipts: print(json.dumps(replay_prepare(a.prepare_replay),sort_keys=True,separators=(',',':'))); return 0
        if a.block_replay and a.index is not None and not a.prepare_replay and not a.join_receipts: print(json.dumps(replay_block(a.block_replay[0],a.block_replay[1],a.index),sort_keys=True,separators=(',',':'))); return 0
        if a.join_receipts and not a.prepare_replay and not a.block_replay: print(json.dumps(join(a.join_receipts),sort_keys=True,separators=(',',':'))); return 0
        fail('usage')
    except Exception as exc: print(json.dumps({'status':'NOT_READY','error':str(exc)},sort_keys=True),file=sys.stderr); return 1
if __name__=='__main__': raise SystemExit(main())
