#!/usr/bin/env python3
"""Result-independent Task647 pre-join gate; heavy owner remains fail-closed."""
import argparse, hashlib, json, os, re, stat, sys, tempfile, time
from pathlib import Path
INPUT_PINS={'scratchpad/a0_paper_words_v1.json': '90ba603368307e16b27b2bad9d84847c7bedc501fab811b8919d96e3c8936893',
 'scratchpad/fuda1_a0_rmax_data.g': '625b4d11ca882c9419d9e0d78510bf323a117673722b8dd9ec7d7e85554267ba',
 'search/certs/d972_r07_a0_c2fourier_joint_floor_v1.json': 'e55b7dfa5a0876054b05259f115266c0b2651431f1f2670efe85e9b34c94222b',
 'search/d972_r07_a0_c2fourier_joint_floor_v1.py': '6201ae0b5c1d648529ac648a574c5096b8088fe341423724556860d9d3f23fba',
 'sol/proof_r07_a0_affine_truncated_two_rung_engine_v443.md': '80970217b415d7b764e399b5ce5892075b1f82f7f87f0c6199e9f6b0e404f24c',
 'sol/proof_r07_a0_explicit_g9_two_rung_twisting_v442.md': 'afa91b6137f8321522cf97fa11502213bde45c7c4c325b3b2ad28e8f6e844de4',
 'sol/proof_r07_a0_relative_fibre_echelon_lift_v441.md': '5cb52ffd02d2cd5c89e08080931065123a7208f7d5a2878acddb5d9ac2958fbb',
 'sol/proof_r07_filtered_transition_defect_closure_v444.md': '705afdc595f21f64356b70469a8444708b8a8c8e6306c218e942863a560ef645',
 'sol/proof_r07_first_rung_character_blocks_coupled_monomials_v446.md': '389ceee1250b892ec4845753af23f4455e619e2d72782931645d8b8176764756',
 'sol/proof_r07_first_rung_character_projector_word_repair_v447.md': '3e4bb3e498beb2c44cf3e1f0786ad83c7691312674967877b766e3e61bb496c2',
 'sol/proof_r07_first_rung_six_grade_index_repair_v449.md': '0237572f8ee949cdac8129cb9a9dae8c833b00baee2647c0deed194449577ff9',
 'sol/sol_reply_544_audit_r07_a0_relative_fibre_echelon_v1.md': '7875fa2641355c8d6d09248b23c9fa9c766f48db751d34b90826ab609b457eb3',
 'sol/sol_reply_547_audit_r07_a0_psl504_canonical_payload_v1.md': '84029c2f64ac8a20f83d9680e2b105f6994db140c4062d8e5c8f99228f7ab32f',
 'sol/sol_reply_548_audit_r07_a0_explicit_g9_two_rung_twisting_v1.md': 'bd1b0239e0410f2ab63abd30e7ff9a422528d141138cfeafc8ca3960da1cd834',
 'sol/sol_reply_549_audit_r07_a0_order2016_literal_member_v1.md': 'a088d27203e2064ac8240b813fd15e905ec82633b93b829e89b4a073f111256c',
 'sol/sol_reply_550_audit_r07_a0_affine_engine_transition_defects_v1.md': '329aa9b8c8b87e5672938cb70ab99dbf365b59a0e63468a3df58420ee26e4616',
 'sol/sol_reply_553_audit_r07_a0_character_blocks_coupled_monomials_v1.md': '9e06ae4022e6267846561b13fed2f64a73909ba0d3b68436173763cf6bdba1df',
 'sol/sol_reply_555_audit_r07_a0_six_grade_schedule_v1.md': '8dcdfbb4825c65bff9698311b735e830c27d39f98405bcfb01af3411d97a2e45'}
SERVICE={'run':'33677346616','attempt':'1','head':'22c6dddb43d107c05e65f53ad898823ae8ebe276','prepare':(9865061266,'task554-grade1-v3-prepare-33677346616-1',204360988,'sha256:da8bfec6a03cac65de40ba8c4f79cde687fd2629edb3c3965fd972ecf96cc2f4'),'block0':(9865238399,'task554-grade1-v3-state-block-0-33677346616-1',81729645,'sha256:2a8e63a4270bf4052c7fd8763d7828fc17dd6b94c88854bacde1e94082cd5838'),'block1':(9865242284,'task554-grade1-v3-state-block-1-33677346616-1',82259824,'sha256:849321b79f0e3ea3c9a3f9c9dad43de2b3aaa571163456abc702476e322714fb'),'block2':(9865193269,'task554-grade1-v3-state-block-2-33677346616-1',82200189,'sha256:d2cdf8245d58a384bebfd516135e07930fe26c21c2c1cab130dfa6c3c7f2854d'),'block3':(9865239848,'task554-grade1-v3-state-block-3-33677346616-1',82266526,'sha256:87547101ede2fb48619a069de958c08cbb3cb0ee6c0990090234005aacd05b92')}
PARENTS={'prepare':('9865061266','1f191d88a0453360021ec57d253a7d16c9a66ac059ddaaadb6db3e2b9293c865'),'block0':('9865238399','9ebcc7ad1141c20aeaff82eb4a83a9489dc492b30220547f23526b4fcdd8dc74'),'block1':('9865242284','d783bbe6c92c15a241eb78d0b25bca5e7c00f60799ce82f6df8b1d3ee7a202f6'),'block2':('9865193269','a6dcc904fc3e9daae008f72de7e83ffadcd39055d557621b9cdf06baea0e83ac'),'block3':('9865239848','642a4ec0ad6ad4ea659e84330e34006c767ca029203446cb64a17c151fefdb01')}
BLOCK_BASIS_SHA=('cc7e38114afc58e3aba10fa340a6ebd4f9a7a4752d5bb5fb9408ea8d84021e39','0223f72b7d2cb8a72f2ff99b8812fea977ed761c8505dab52ad3fba284b93461','602f23081aa609973860eac24d2f65104a9530c8ddf356d60a9d0378921b99f6','4ed4de15c00290f60e5fd2d57dd94db3103be92c602d92481f2835d9d96db0b9')
ORDERS={'characters':[[0,0],[0,1],[1,0],[1,1]],'actors':[1,-1,2,-2],'monomials':['u1^2','u1u2','u1u3','u2^2','u2u3','u3^2'],'origins':32280,'basis':8059,'lower':32260,'top':48384}
EMPTY_JOIN={'run':None,'attempt':None,'head':None,'job':None,'artifact_id':None,'artifact_bytes':None,'artifact_digest':None,'manifest_sha256':None,'checker_sha256':None,'rho2_packed_sha256':None,'rho2_dense_sha256':None}
def join_gate(j):
    if j!=EMPTY_JOIN: raise RuntimeError('result_dependent_join_not_frozen')
    raise RuntimeError('NOT_READY:Task640_step8_join')
def checkpoint_gate(c):
    required={'schema','generation','previous_checkpoint_sha256','phase','cursor','terminal'}
    if set(c)!=required or c['terminal'] not in (None,'UNKNOWN_RESOURCE'): raise RuntimeError('checkpoint_contract')
def structural_row(row,lead,scale,prior,index):
    if not row or any(x not in (0,1,2) for x in row) or not any(row): raise RuntimeError('row_field')
    actual=next(i for i,x in enumerate(row) if x)
    if lead!=actual or row[lead]!=1 or scale not in (1,2) or any(p<0 or p>=index for p in prior): raise RuntimeError('row_structure')
class Presentation1:
    OFFSETS=(0,505,1008,1511,2014,3523,5035,6547,8059)
    def __init__(self,rows): self._rows=tuple(rows)
    def basis(self,i): return self._rows[i]
    @property
    def pending_semantic_replays(self): return {'seeds':44,'actors':32236}
def selftest():
    checkpoint_gate({'schema':'r07.grade2.prejoin.v1','generation':0,'previous_checkpoint_sha256':None,'phase':'AUTH_INPUTS','cursor':0,'terminal':None})
    try: join_gate(dict(EMPTY_JOIN))
    except RuntimeError as e: assert str(e).startswith('NOT_READY:')
    structural_row([0,1,2],1,2,[],0); rejected=0
    for args in (([0,0],0,1,[],0),([2],0,1,[],0),([1],0,3,[],0),([1],0,1,[1],1)):
        try:structural_row(*args)
        except RuntimeError:rejected+=1
    receipt=local_input_receipt(); good={'input_manifest':receipt,'input_manifest_sha256':sha(canonical(receipt)),'dimensions':fixed_dimensions(),'paired_lower_presentation_complete':True}; validate_input_binding(good,receipt)
    mutations=[]
    bad=dict(receipt); bad.pop(next(iter(bad))); mutations.append({**good,'input_manifest':bad})
    keys=list(receipt); bad=dict(receipt); bad[keys[0]],bad[keys[1]]=bad[keys[1]],bad[keys[0]]; mutations.append({**good,'input_manifest':bad})
    mutations.append({**good,'input_manifest':{**receipt,'extra':{'bytes':0,'sha256':'0'*64}}}); mutations.append({**good,'dimensions':{**fixed_dimensions(),'characters':5}}); mutations.append({**good,'input_manifest_sha256':'0'*64}); mutations.append({**good,'paired_lower_presentation_complete':False})
    live=0
    for bad in mutations:
        try: validate_input_binding(bad,receipt)
        except RuntimeError: live+=1
        else: raise RuntimeError('fixture_input_binding')
    blob_live=blob_fixture(); roster_live=roster_fixture(); expression_live=expression_fixture(); file_live,file_skipped=file_safety_fixture(); envelope_live=envelope_fixture(); row_scan_live=old_row_scan_fixture(); block_live=block_fixture()
    matrix={'input_binding':live,'typed_blob':blob_live,'roster_origin_packet':roster_live,'expression_dag_record':expression_live,'file_safety':file_live,'head_body_envelope':envelope_live}
    print(json.dumps({'status':'PASS','join':'NOT_READY','parents':5,'structural_mutations':rejected,'input_binding_mutations':live,'blob_mutations':blob_live,'roster_mutations':roster_live,'expression_dag_mutations':expression_live,'file_safety_mutations':file_live,'envelope_mutations':envelope_live,'old_row_scan_fixture':row_scan_live,'block_fixture':block_live,'f668_6_mutation_matrix':matrix,'file_safety_skipped':file_skipped,'blob_race_mutation':'SKIPPED_NONDETERMINISTIC','orders':ORDERS},sort_keys=True))
def sha(data): return hashlib.sha256(data).hexdigest()
def canonical(x): return (json.dumps(x,sort_keys=True,separators=(',',':'),ensure_ascii=True)+'\n').encode('ascii')
def fixed_dimensions(): return {'character_labels':[[0,0],[0,1],[1,0],[1,1]],'characters':4,'monomials':[[1,0,0],[0,1,0],[0,0,1]],'monomials_coupled':True,'physical_grade':24192,'physical_lower_regular':8064,'physical_lower_with_auxiliary':8068,'source_base':6048,'source_per_character':18144,'source_total':72576}
def validate_input_binding(body,receipt):
    if body.get('input_manifest')!=receipt or body.get('input_manifest_sha256')!=sha(canonical(receipt)) or body.get('dimensions')!=fixed_dimensions() or body.get('paired_lower_presentation_complete') is not True: raise RuntimeError('state_input_binding')
def local_input_receipt():
    root=Path(__file__).resolve().parents[1]; out={}
    for rel,digest in INPUT_PINS.items():
        raw=(root/rel).read_bytes()
        if sha(raw)!=digest: raise RuntimeError('frozen_hash:'+rel)
        out[rel]={'bytes':len(raw),'sha256':digest}
    return out
def _plain_int(value): return isinstance(value,int) and not isinstance(value,bool)
def validate_blob_receipt(state_dir,receipt,rows,width):
    required={'file','bytes','sha256','rows','width','encoding'}
    if not isinstance(receipt,dict) or set(receipt)!=required: raise RuntimeError('blob_receipt_shape')
    if not _plain_int(rows) or rows<0 or not _plain_int(width) or width<=0 or width%4: raise RuntimeError('blob_expected_dimensions')
    filename=receipt['file']; expected=rows*(width//4)
    if (not isinstance(filename,str) or Path(filename).name!=filename or
        not re.fullmatch(r'[A-Za-z0-9_.-]+\.[0-9a-f]{64}\.bin',filename) or
        not isinstance(receipt['sha256'],str) or not re.fullmatch(r'[0-9a-f]{64}',receipt['sha256']) or
        not filename.endswith('.'+receipt['sha256']+'.bin') or
        not _plain_int(receipt['rows']) or not _plain_int(receipt['width']) or not _plain_int(receipt['bytes']) or
        receipt['rows']!=rows or receipt['width']!=width or receipt['bytes']!=expected or
        receipt['encoding']!='base3-four-trits-per-byte'): raise RuntimeError('blob_receipt_semantics')
    path=state_dir/filename; validate_regular_member(path); before=path.stat()
    if before.st_size!=expected: raise RuntimeError('blob_size:'+filename)
    h=hashlib.sha256(); count=0
    with path.open('rb') as stream:
        while True:
            chunk=stream.read(1048576)
            if not chunk: break
            if max(chunk,default=0)>80: raise RuntimeError('packed_byte')
            h.update(chunk); count+=len(chunk)
    after=path.stat()
    if count!=expected: raise RuntimeError('blob_eof:'+filename)
    if h.hexdigest()!=receipt['sha256']: raise RuntimeError('blob_sha256:'+filename)
    validate_stable_identity(before,after,filename)
def is_reparse(info): return bool(getattr(info,'st_file_attributes',0)&0x400)
def validate_regular_member(path):
    info=path.lstat()
    if stat.S_ISLNK(info.st_mode) or is_reparse(info) or not stat.S_ISREG(info.st_mode): raise RuntimeError('unsafe_roster_entry:'+path.name)
def scan_safe_root(path):
    info=path.lstat()
    if stat.S_ISLNK(info.st_mode) or is_reparse(info) or not stat.S_ISDIR(info.st_mode): raise RuntimeError('unsafe_prepare_root')
    resolved=path.resolve(); names=[]
    for member in resolved.iterdir(): validate_regular_member(member); names.append(member.name)
    validate_name_set(names)
    return resolved,names
def validate_name_set(names):
    if len({name.casefold() for name in names})!=len(names): raise RuntimeError('case_collision')
def require_exact_roster(names,expected):
    if any(not isinstance(name,str) or Path(name).name!=name for name in expected): raise RuntimeError('unsafe_roster_basename')
    if set(names)!=set(expected) or len(names)!=len(expected): raise RuntimeError('roster')
def validate_stable_identity(before,after,filename):
    if (after.st_size,after.st_mtime_ns,after.st_ino)!=(before.st_size,before.st_mtime_ns,before.st_ino): raise RuntimeError('blob_changed_during_authentication:'+filename)
def file_safety_fixture():
    rejected=0; skipped=[]
    def reject(call):
        nonlocal rejected
        try: call()
        except (RuntimeError,FileNotFoundError): rejected+=1
        else: raise RuntimeError('fixture_file_safety')
    with tempfile.TemporaryDirectory() as td:
        base=Path(td); regular=base/'regular'; regular.mkdir(); (regular/'a').write_bytes(b'a')
        reject(lambda:scan_safe_root(regular/'a'))
        nonregular=base/'nonregular'; nonregular.mkdir(); (nonregular/'child').mkdir(); reject(lambda:scan_safe_root(nonregular))
        reject(lambda:require_exact_roster(['a'],['../a']))
        reject(lambda:require_exact_roster(['a','extra'],['a']))
        reject(lambda:require_exact_roster(['a'],['a','missing']))
        reject(lambda:validate_name_set(['Case','case']))
        before=(regular/'a').stat(); (regular/'a').write_bytes(b'changed'); after=(regular/'a').stat(); reject(lambda:validate_stable_identity(before,after,'a'))
        target=base/'target'; target.mkdir(); (target/'x').write_bytes(b'x')
        root_link=base/'root-link'
        try:
            root_link.symlink_to(target,target_is_directory=True); reject(lambda:scan_safe_root(root_link))
        except OSError: skipped.append('root_link_or_reparse')
        entry_root=base/'entry-root'; entry_root.mkdir(); entry_link=entry_root/'entry-link'
        try:
            entry_link.symlink_to(target/'x'); reject(lambda:scan_safe_root(entry_root))
        except OSError: skipped.append('entry_link_or_reparse')
        if os.name=='nt': skipped.append('distinct_non_symlink_reparse_fixture')
    return rejected,skipped
def authenticate_prepare_blobs(state_dir,b):
    validate_blob_receipt(state_dir,b['residual_blob'],1,24192)
    ranks=(505,503,503,503)
    for old,rank in zip(b['old_blocks'],ranks):
        validate_blob_receipt(state_dir,old['lower_basis_blob'],rank,6056)
        validate_blob_receipt(state_dir,old['lifted_grade_blob'],rank,72576)
    for packet in b['packets']: validate_blob_receipt(state_dir,packet['blob'],8232,18144)
def validate_prepare_roster(b):
    chars=[[0,0],[0,1],[1,0],[1,1]]; blocks=b.get('old_blocks'); packets=b.get('packets'); origins=b.get('defect_origins')
    if not isinstance(blocks,list) or len(blocks)!=4 or not isinstance(packets,list) or len(packets)!=4: raise RuntimeError('prepare_roster_count')
    if not isinstance(origins,list) or len(origins)!=8232: raise RuntimeError('prepare_origin_cardinality')
    digest=sha(canonical(origins))
    if b.get('defect_origin_sha256')!=digest: raise RuntimeError('prepare_origin_digest')
    for i,origin in enumerate(origins):
        if not isinstance(origin,dict) or origin.get('id')!=i: raise RuntimeError('prepare_origin_identity')
    cursor=0
    for i,(old,span) in enumerate(zip(blocks,(2064,2056,2056,2056))):
        if (not isinstance(old,dict) or old.get('character_index')!=i or old.get('character')!=chars[i] or
            not isinstance(old.get('record'),dict) or old['record'].get('character')!=chars[i]): raise RuntimeError('prepare_old_character')
        end=cursor+span
        if old.get('defect_origin_range')!=[cursor,end]: raise RuntimeError('prepare_origin_range')
        cursor=end
    for i,packet in enumerate(packets):
        if (not isinstance(packet,dict) or packet.get('character')!=chars[i] or packet.get('origin_count')!=8232 or
            packet.get('origin_sha256')!=digest): raise RuntimeError('prepare_packet_binding')
def roster_fixture():
    origins=[{'id':i} for i in range(8232)]; digest=sha(canonical(origins)); chars=[[0,0],[0,1],[1,0],[1,1]]; cursor=0; blocks=[]
    for i,span in enumerate((2064,2056,2056,2056)):
        blocks.append({'character_index':i,'character':chars[i],'record':{'character':chars[i]},'defect_origin_range':[cursor,cursor+span]}); cursor+=span
    good={'defect_origins':origins,'defect_origin_sha256':digest,'old_blocks':blocks,'packets':[{'character':chars[i],'origin_count':8232,'origin_sha256':digest} for i in range(4)]}
    validate_prepare_roster(good); mutations=[]
    def clone(): return json.loads(json.dumps(good))
    q=clone(); q['old_blocks'][0],q['old_blocks'][1]=q['old_blocks'][1],q['old_blocks'][0]; mutations.append(q)
    q=clone(); q['old_blocks'][0]['character_index']=1; mutations.append(q)
    q=clone(); q['old_blocks'][0]['character']=[1,1]; mutations.append(q)
    q=clone(); q['old_blocks'][0]['record']['character']=[1,1]; mutations.append(q)
    q=clone(); q['old_blocks'][1]['defect_origin_range']=[2063,4120]; mutations.append(q)
    q=clone(); q['defect_origins'][17]['id']=18; q['defect_origin_sha256']=sha(canonical(q['defect_origins'])); mutations.append(q)
    q=clone(); q['defect_origin_sha256']='0'*64; mutations.append(q)
    q=clone(); q['packets'][0],q['packets'][1]=q['packets'][1],q['packets'][0]; mutations.append(q)
    q=clone(); q['packets'][0]['character']=[1,1]; mutations.append(q)
    q=clone(); q['packets'][0]['origin_count']=8231; mutations.append(q)
    q=clone(); q['packets'][0]['origin_sha256']='0'*64; mutations.append(q)
    rejected=0
    for bad in mutations:
        try: validate_prepare_roster(bad)
        except RuntimeError: rejected+=1
        else: raise RuntimeError('fixture_prepare_roster')
    return rejected
def validate_expression(expression,rank,gate,earlier_than=None):
    if not isinstance(expression,list): raise RuntimeError(gate+':shape')
    bound=rank if earlier_than is None else earlier_than
    for pair in expression:
        if (not isinstance(pair,list) or len(pair)!=2 or not _plain_int(pair[0]) or pair[0]<0 or pair[0]>=bound or
            not _plain_int(pair[1]) or pair[1] not in (1,2)): raise RuntimeError(gate+':entry')
    return len(expression)
def validate_old_records(blocks,ranks):
    if not isinstance(blocks,list) or len(blocks)!=len(ranks): raise RuntimeError('old_record_count')
    counts={'actor_rows':0,'actor_expressions':0,'seed_expressions':0,'dag_nodes':0,'seed_pairs':0,'actor_pairs':0,'dag_pairs':0}
    for old,rank in zip(blocks,ranks):
        record=old.get('record') if isinstance(old,dict) else None
        if (not isinstance(record,dict) or old.get('rank')!=rank or record.get('rank')!=rank or
            record.get('attempts')!=44+4*rank or record.get('actor_order')!=[1,-1,2,-2] or
            record.get('queue_exhausted') is not True or not isinstance(record.get('seed_reductions'),list) or
            len(record['seed_reductions'])!=44 or not isinstance(record.get('actor_transitions'),list) or
            len(record['actor_transitions'])!=rank or any(not isinstance(row,list) or len(row)!=4 for row in record['actor_transitions']) or
            not isinstance(record.get('dag_nodes'),list) or len(record['dag_nodes'])!=rank): raise RuntimeError('old_record_shape')
        for expression in record['seed_reductions']:
            counts['seed_pairs']+=validate_expression(expression,rank,'seed_expression'); counts['seed_expressions']+=1
        for row in record['actor_transitions']:
            counts['actor_rows']+=1
            for expression in row:
                counts['actor_pairs']+=validate_expression(expression,rank,'actor_expression'); counts['actor_expressions']+=1
        leads=set()
        for pivot,node in enumerate(record['dag_nodes']):
            if (not isinstance(node,dict) or not _plain_int(node.get('pivot')) or node['pivot']!=pivot or
                not _plain_int(node.get('lead')) or not 0<=node['lead']<6056 or node['lead'] in leads or
                not _plain_int(node.get('scale')) or node['scale'] not in (1,2)): raise RuntimeError('old_dag_node')
            leads.add(node['lead']); counts['dag_pairs']+=validate_expression(node.get('reductions'),rank,'dag_reduction',pivot); counts['dag_nodes']+=1
    return counts
def expression_fixture():
    rank=2; record={'rank':rank,'attempts':52,'actor_order':[1,-1,2,-2],'queue_exhausted':True,
        'seed_reductions':[[] for _ in range(44)],'actor_transitions':[[[],[],[],[]] for _ in range(rank)],
        'dag_nodes':[{'pivot':0,'lead':3,'scale':1,'reductions':[]},{'pivot':1,'lead':4,'scale':2,'reductions':[[0,1]]}]}
    good=[{'rank':rank,'record':record}]; validate_old_records(good,(rank,)); mutations=[]
    def clone(): return json.loads(json.dumps(good))
    q=clone(); q[0]['record']['seed_reductions'][0]=[[0]]; mutations.append(q)
    for value in (True,-1,2): q=clone(); q[0]['record']['seed_reductions'][0]=[[value,1]]; mutations.append(q)
    for value in (True,0,3): q=clone(); q[0]['record']['seed_reductions'][0]=[[0,value]]; mutations.append(q)
    q=clone(); q[0]['record']['dag_nodes'].pop(); mutations.append(q)
    q=clone(); q[0]['record']['dag_nodes'].append({'pivot':2,'lead':5,'scale':1,'reductions':[]}); mutations.append(q)
    for value in (1,True): q=clone(); q[0]['record']['dag_nodes'][0]['pivot']=value; mutations.append(q)
    for value in (True,-1,6056,4): q=clone(); q[0]['record']['dag_nodes'][0]['lead']=value; mutations.append(q)
    for value in (True,0,3): q=clone(); q[0]['record']['dag_nodes'][0]['scale']=value; mutations.append(q)
    q=clone(); q[0]['record']['dag_nodes'][0]['reductions']=[[1,1]]; mutations.append(q)
    q=clone(); q[0]['record']['dag_nodes'][1]['reductions']=[[1,1]]; mutations.append(q)
    q=clone(); q[0]['rank']=3; mutations.append(q)
    q=clone(); q[0]['record']['rank']=3; mutations.append(q)
    q=clone(); q[0]['record']['attempts']=51; mutations.append(q)
    q=clone(); q[0]['record']['queue_exhausted']=False; mutations.append(q)
    q=clone(); q[0]['record']['actor_order']=[-1,1,2,-2]; mutations.append(q)
    rejected=0
    for bad in mutations:
        try: validate_old_records(bad,(rank,))
        except RuntimeError: rejected+=1
        else: raise RuntimeError('fixture_expression_dag')
    return rejected
def validate_prepare_envelope(head_raw,body_raw,expected_digest=None):
    try: head=json.loads(head_raw); body=json.loads(body_raw)
    except (ValueError,TypeError): raise RuntimeError('envelope_json')
    digest=expected_digest or '1f191d88a0453360021ec57d253a7d16c9a66ac059ddaaadb6db3e2b9293c865'
    expected_head={'body_sha256':digest,'parent_sha256':None,'schema':'d972.r07.a0.first-rung-grade1.v3.state.head','stem':'prepare'}
    if head_raw!=canonical(head) or head!=expected_head: raise RuntimeError('prepare_head_envelope')
    if sha(body_raw)!=digest: raise RuntimeError('prepare_body_hash')
    if body_raw!=canonical(body): raise RuntimeError('prepare_body_canonical')
    if body.get('schema')!='d972.r07.a0.first-rung-grade1.v3.state' or body.get('phase')!='prepare' or body.get('fixture') is not False: raise RuntimeError('prepare_body_envelope')
    return body
def envelope_fixture():
    body={'fixture':False,'phase':'prepare','schema':'d972.r07.a0.first-rung-grade1.v3.state'}; raw=canonical(body); digest=sha(raw)
    head={'body_sha256':digest,'parent_sha256':None,'schema':'d972.r07.a0.first-rung-grade1.v3.state.head','stem':'prepare'}; hr=canonical(head)
    validate_prepare_envelope(hr,raw,digest); tests=[]
    tests.append((hr+b' ',raw,digest))
    for key,value in (('parent_sha256','0'*64),('stem','wrong'),('schema','wrong'),('body_sha256','0'*64)):
        q=dict(head); q[key]=value; tests.append((canonical(q),raw,digest))
    tests.append((hr,raw+b' ',digest))
    noncanonical=json.dumps(body,sort_keys=True).encode(); nd=sha(noncanonical); nh=canonical({**head,'body_sha256':nd}); tests.append((nh,noncanonical,nd))
    for key,value in (('schema','wrong'),('phase','wrong'),('fixture',True)):
        q=dict(body); q[key]=value; qr=canonical(q); qd=sha(qr); qh=canonical({**head,'body_sha256':qd}); tests.append((qh,qr,qd))
    rejected=0
    for bad_head,bad_body,bad_digest in tests:
        try: validate_prepare_envelope(bad_head,bad_body,bad_digest)
        except RuntimeError: rejected+=1
        else: raise RuntimeError('fixture_prepare_envelope')
    return rejected
def peak_rss_bytes():
    if os.name=='nt':
        try:
            import ctypes
            class PMC(ctypes.Structure):
                _fields_=[('cb',ctypes.c_ulong),('PageFaultCount',ctypes.c_ulong),('PeakWorkingSetSize',ctypes.c_size_t),('WorkingSetSize',ctypes.c_size_t),('QuotaPeakPagedPoolUsage',ctypes.c_size_t),('QuotaPagedPoolUsage',ctypes.c_size_t),('QuotaPeakNonPagedPoolUsage',ctypes.c_size_t),('QuotaNonPagedPoolUsage',ctypes.c_size_t),('PagefileUsage',ctypes.c_size_t),('PeakPagefileUsage',ctypes.c_size_t)]
            row=PMC(); row.cb=ctypes.sizeof(row)
            get_process=ctypes.windll.kernel32.GetCurrentProcess; get_process.restype=ctypes.c_void_p
            get_info=ctypes.windll.psapi.GetProcessMemoryInfo; get_info.argtypes=[ctypes.c_void_p,ctypes.POINTER(PMC),ctypes.c_ulong]
            if get_info(get_process(),ctypes.byref(row),row.cb): return int(row.PeakWorkingSetSize)
        except (AttributeError,OSError): pass
    else:
        try:
            import resource
            value=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss
            return int(value if sys.platform=='darwin' else value*1024)
        except (ImportError,OSError): pass
    return None
def packed_first_nonzero(raw,width):
    if len(raw)!=(width+3)//4: raise RuntimeError('packed_row_size')
    if any(value>80 for value in raw): raise RuntimeError('packed_byte')
    for byte_index,value in enumerate(raw):
        work=value
        for slot in range(4):
            coordinate=4*byte_index+slot
            if coordinate>=width: break
            trit=work%3
            if trit: return coordinate,trit
            work//=3
    return None
def analyze_old_row(character,lower_raw,grade_raw,declared,base_width=6048,grade_width=72576):
    local=packed_first_nonzero(lower_raw,base_width+8)
    if local is None: raise RuntimeError('old_lower_zero')
    if local[0]!=declared: raise RuntimeError('old_local_lead_mismatch')
    if local[1]!=1: raise RuntimeError('old_local_lead_nonnormalized')
    candidates=[]
    regular=packed_first_nonzero(lower_raw[:base_width//4],base_width)
    if regular is not None: candidates.append((character*base_width+regular[0],regular[1],'degree_zero'))
    grade=packed_first_nonzero(grade_raw,grade_width)
    if grade is not None: candidates.append((4*base_width+grade[0],grade[1],'degree_one'))
    auxiliary=packed_first_nonzero(lower_raw[base_width//4:],8)
    if auxiliary is not None: candidates.append((4*base_width+grade_width+auxiliary[0],auxiliary[1],'auxiliary'))
    if not candidates: raise RuntimeError('old_logical_zero')
    return min(candidates,key=lambda row:row[0]),local
def scan_old_rows(state_dir,blocks,return_leads=False):
    leads=[]
    for character,(old,rank) in enumerate(zip(blocks,(505,503,503,503))):
        lower_receipt=old['lower_basis_blob']; grade_receipt=old['lifted_grade_blob']; lower_path=state_dir/lower_receipt['file']; grade_path=state_dir/grade_receipt['file']
        validate_regular_member(lower_path); validate_regular_member(grade_path); lower_before=lower_path.stat(); grade_before=grade_path.stat()
        lower_hash=hashlib.sha256(); grade_hash=hashlib.sha256(); lower_count=grade_count=0
        with lower_path.open('rb') as lower_stream,grade_path.open('rb') as grade_stream:
            for pivot,node in enumerate(old['record']['dag_nodes']):
                lower_raw=lower_stream.read(1514); grade_raw=grade_stream.read(18144)
                lower_hash.update(lower_raw); grade_hash.update(grade_raw); lower_count+=len(lower_raw); grade_count+=len(grade_raw)
                lead,local=analyze_old_row(character,lower_raw,grade_raw,node['lead']); leads.append({'row':len(leads),'character':character,'pivot':pivot,'lead':lead[0],'coefficient':lead[1],'kind':lead[2],'local_lead':local[0]})
            if lower_stream.read(1) or grade_stream.read(1): raise RuntimeError('old_blob_trailing')
        if lower_count!=lower_receipt['bytes'] or lower_hash.hexdigest()!=lower_receipt['sha256']: raise RuntimeError('old_scan_lower_receipt')
        if grade_count!=grade_receipt['bytes'] or grade_hash.hexdigest()!=grade_receipt['sha256']: raise RuntimeError('old_scan_grade_receipt')
        validate_stable_identity(lower_before,lower_path.stat(),lower_path.name); validate_stable_identity(grade_before,grade_path.stat(),grade_path.name)
    diagnostic=summarize_old_leads(leads)
    return (diagnostic,leads) if return_leads else diagnostic
def summarize_old_leads(leads):
    by_lead={}
    for row in leads: by_lead.setdefault(row['lead'],[]).append(row['row'])
    collisions=[{'lead':lead,'rows':rows} for lead,rows in sorted(by_lead.items()) if len(rows)>1]
    nonnormal=[row for row in leads if row['coefficient']!=1][:8]
    coefficient_one=[[r['row'],r['lead']] for r in leads if r['coefficient']==1]
    diagnostic={'rows':len(leads),'global_leads_sha256':sha(canonical([[r['lead'],r['coefficient']] for r in leads])),'local_leads_sha256':sha(canonical([r['local_lead'] for r in leads])),'distinct_global_leads':len(by_lead),'duplicate_global_lead_count':len(leads)-len(by_lead),'duplicate_global_leads_sha256':sha(canonical(collisions)),'coefficient_one_global_leads':len(coefficient_one),'coefficient_one_leads_sha256':sha(canonical(coefficient_one)),'collision_examples':collisions[:8],'nonnormalization_examples':nonnormal,'global_echelonicity':len(by_lead)==len(leads) and not nonnormal}
    return diagnostic
def pack_fixture(values):
    out=bytearray()
    for start in range(0,len(values),4):
        chunk=values[start:start+4]+[0]*max(0,4-len(values[start:start+4])); out.append(sum(value*(3**i) for i,value in enumerate(chunk)))
    return bytes(out)
def old_row_scan_fixture():
    zero=[0]*8; lower_zero=[0]*12
    cases=[([1]+[0]*11,zero,0,'degree_zero',1),([0,0,0,0,1]+[0]*7,[0,1]+[0]*6,4,'degree_one',1),([0,0,0,0,1]+[0]*7,zero,4,'auxiliary',1),([0,0,0,0,1]+[0]*7,[2]+[0]*7,4,'degree_one',2)]
    observed=[]
    coefficient_two=0
    for lower,grade,declared,kind,coefficient in cases:
        lead,_=analyze_old_row(0,pack_fixture(lower),pack_fixture(grade),declared,4,8)
        if lead[2]!=kind or lead[1]!=coefficient: raise RuntimeError('fixture_old_row_kind')
        coefficient_two+=lead[1]==2
        observed.append(lead[0])
    rejected=0
    for lower,grade,declared in (([2]+[0]*11,zero,0),(lower_zero,zero,0),([1]+[0]*11,zero,1)):
        try: analyze_old_row(0,pack_fixture(lower),pack_fixture(grade),declared,4,8)
        except RuntimeError: rejected+=1
        else: raise RuntimeError('fixture_old_row_rejection')
    try: packed_first_nonzero(bytes([1,81]),8)
    except RuntimeError: rejected+=1
    else: raise RuntimeError('fixture_late_packed_byte')
    duplicate=summarize_old_leads([{'row':0,'lead':7,'coefficient':1,'local_lead':1},{'row':1,'lead':7,'coefficient':1,'local_lead':2}])
    if duplicate['duplicate_global_lead_count']!=1 or duplicate['collision_examples']!=[{'lead':7,'rows':[0,1]}] or duplicate['duplicate_global_leads_sha256']!='c557517d6dc6bb786415d3467e8f04fba0d8084ef3b64c01ee3b5abf592e6bc6' or duplicate['global_echelonicity'] is not False: raise RuntimeError('fixture_duplicate_global_lead')
    nonnormal_row={'row':0,'lead':5,'coefficient':2,'local_lead':4}; nonnormal=summarize_old_leads([nonnormal_row])
    if nonnormal['coefficient_one_global_leads']!=0 or nonnormal['nonnormalization_examples']!=[nonnormal_row] or nonnormal['global_echelonicity'] is not False: raise RuntimeError('fixture_nonnormal_global_lead')
    return {'kinds':3,'coefficient_two':coefficient_two,'rejections':rejected,'duplicate_global_leads':1,'duplicate_digest':duplicate['duplicate_global_leads_sha256'],'nonnormalization_examples':1}
FALSE_CLAIMS={'A0':False,'COMMON':False,'COMPATIBLE_LIFT':False,'FAKE':False,'FULL_Q0':False,'IHARA':False,'ORDER_54432':False,'verified':False}
def validate_block_semantics(body,prepare,index,rank):
    chars=[[0,0],[0,1],[1,0],[1,1]]; attempts=8232+4*rank
    flags=body.get('downstream_claim_flags')
    if (not isinstance(flags,dict) or set(flags)!=set(FALSE_CLAIMS) or
        any(flags[key] is not False for key in FALSE_CLAIMS)):
        raise RuntimeError('block_semantics')
    if (body.get('schema')!='d972.r07.a0.first-rung-grade1.v3.state' or body.get('phase')!='block' or body.get('fixture') is not False or
        body.get('parent_sha256')!='1f191d88a0453360021ec57d253a7d16c9a66ac059ddaaadb6db3e2b9293c865' or not _plain_int(body.get('character_index')) or body['character_index']!=index or
        not isinstance(body.get('character'),list) or any(not _plain_int(x) for x in body['character']) or body['character']!=chars[index] or body.get('dimensions')!={'monomials_coupled':3,'width':18144} or
        body.get('packet_sha256')!=prepare['packets'][index]['blob']['sha256'] or not _plain_int(body.get('origin_count')) or body['origin_count']!=8232 or not _plain_int(body.get('rank')) or body['rank']!=rank or
        not _plain_int(body.get('attempts')) or body['attempts']!=attempts or body.get('queue_exhausted') is not True or not isinstance(body.get('actor_order'),list) or any(not _plain_int(x) for x in body['actor_order']) or body['actor_order']!=[1,-1,2,-2]): raise RuntimeError('block_semantics')
    origins=body.get('origin_reductions'); transitions=body.get('actor_transitions'); nodes=body.get('dag_nodes'); leads=body.get('pivot_leads')
    if (not isinstance(origins,list) or len(origins)!=8232 or not isinstance(transitions,list) or len(transitions)!=rank or
        any(not isinstance(row,list) or len(row)!=4 for row in transitions) or not isinstance(nodes,list) or len(nodes)!=rank or
        not isinstance(leads,list) or len(leads)!=rank or len(set(leads))!=rank): raise RuntimeError('block_cardinality')
    counts={'origin_expression_lists':8232,'origin_pairs':0,'actor_transition_rows':rank,'actor_expression_lists':4*rank,'actor_pairs':0,'dag_nodes':rank,'dag_pairs':0,'defect_origins':0,'actor_origins':0}
    for expression in origins: counts['origin_pairs']+=validate_expression(expression,rank,'block_origin_expression')
    for row in transitions:
        for expression in row: counts['actor_pairs']+=validate_expression(expression,rank,'block_actor_expression')
    for pivot,node in enumerate(nodes):
        if (not isinstance(node,dict) or not _plain_int(node.get('pivot')) or node['pivot']!=pivot or
            not _plain_int(leads[pivot]) or not _plain_int(node.get('lead')) or node['lead']!=leads[pivot] or
            not 0<=leads[pivot]<18144 or not _plain_int(node.get('scale')) or node['scale'] not in (1,2)): raise RuntimeError('block_dag_node')
        counts['dag_pairs']+=validate_expression(node.get('reductions'),rank,'block_dag_reduction',pivot)
        origin=node.get('origin')
        if not isinstance(origin,dict): raise RuntimeError('block_dag_origin')
        if origin.get('kind')=='defect' and set(origin)=={'kind','origin'} and _plain_int(origin.get('origin')) and 0<=origin['origin']<8232: counts['defect_origins']+=1
        elif origin.get('kind')=='actor' and set(origin)=={'kind','parent','letter'} and _plain_int(origin.get('parent')) and 0<=origin['parent']<pivot and _plain_int(origin.get('letter')) and origin['letter'] in (1,-1,2,-2): counts['actor_origins']+=1
        else: raise RuntimeError('block_dag_origin')
    if body.get('dag_sha256')!=sha(canonical(nodes)): raise RuntimeError('block_dag_digest')
    return counts
def validate_block_envelope(root,index,prepare,expected_digest=None,expected_parent=None):
    root,names=scan_safe_root(root); digest=PARENTS['block'+str(index)][1] if expected_digest is None else expected_digest; parent='1f191d88a0453360021ec57d253a7d16c9a66ac059ddaaadb6db3e2b9293c865' if expected_parent is None else expected_parent; hr=(root/f'block-{index}.HEAD').read_bytes(); br=(root/f'block-{index}.{digest}.json').read_bytes()
    try: head=json.loads(hr); body=json.loads(br)
    except ValueError: raise RuntimeError('block_json')
    expected={'body_sha256':digest,'parent_sha256':parent,'schema':'d972.r07.a0.first-rung-grade1.v3.state.head','stem':'block-'+str(index)}
    if hr!=canonical(head) or head!=expected or sha(br)!=digest or br!=canonical(body): raise RuntimeError('block_envelope')
    receipt=body.get('basis_blob'); require_exact_roster(names,{f'block-{index}.HEAD',f'block-{index}.{digest}.json',receipt.get('file') if isinstance(receipt,dict) else ''})
    return root,body,len(br)
def scan_block_basis(root,body,index,rank):
    receipt=body['basis_blob']
    if receipt.get('sha256')!=BLOCK_BASIS_SHA[index]: raise RuntimeError('block_basis_pin')
    validate_blob_receipt(root,receipt,rank,18144); path=root/receipt['file']; before=path.stat(); h=hashlib.sha256(); count=0; rows=[]
    with path.open('rb') as stream:
        for pivot,declared in enumerate(body['pivot_leads']):
            raw=stream.read(4536); h.update(raw); count+=len(raw); rows.append(analyze_block_row(raw,declared,index,pivot))
        if stream.read(1): raise RuntimeError('block_basis_trailing')
    if count!=receipt['bytes'] or h.hexdigest()!=receipt['sha256']: raise RuntimeError('block_basis_receipt')
    validate_stable_identity(before,path.stat(),path.name)
    return rows,{'rank':rank,'basis_bytes':count,'local_leads_sha256':sha(canonical([r['local_lead'] for r in rows]))}
def analyze_block_row(raw,declared,index,pivot,width=18144):
    lead=packed_first_nonzero(raw,width)
    if lead is None: raise RuntimeError('block_basis_zero')
    if lead[0]!=declared: raise RuntimeError('block_basis_lead')
    if lead[1]!=1: raise RuntimeError('block_basis_nonnormalized')
    return {'row':None,'character':index,'pivot':pivot,'lead':4*6048+width*index+lead[0],'coefficient':1,'local_lead':lead[0]}
def block_fixture():
    prepare={'packets':[{'blob':{'sha256':str(i)*64}} for i in range(4)]}; rank=1
    body={'schema':'d972.r07.a0.first-rung-grade1.v3.state','phase':'block','fixture':False,'parent_sha256':'1f191d88a0453360021ec57d253a7d16c9a66ac059ddaaadb6db3e2b9293c865','character_index':0,'character':[0,0],'dimensions':{'monomials_coupled':3,'width':18144},'packet_sha256':'0'*64,'origin_count':8232,'rank':rank,'attempts':8236,'queue_exhausted':True,'actor_order':[1,-1,2,-2],'downstream_claim_flags':FALSE_CLAIMS,'origin_reductions':[[] for _ in range(8232)],'actor_transitions':[[[],[],[],[]]],'pivot_leads':[0],'dag_nodes':[{'pivot':0,'lead':0,'scale':1,'reductions':[],'origin':{'kind':'defect','origin':0}}]}
    body['dag_sha256']=sha(canonical(body['dag_nodes'])); validate_block_semantics(body,prepare,0,rank); rejected=0
    def reject(q):
        nonlocal rejected
        q['dag_sha256']=sha(canonical(q['dag_nodes']))
        try: validate_block_semantics(q,prepare,0,rank)
        except RuntimeError: rejected+=1
        else: raise RuntimeError('fixture_block_semantics')
    for edit in ('parent','order','expression','forward','origin','node_lead_bool','false_claim_ints'):
        q=json.loads(json.dumps(body))
        if edit=='parent': q['parent_sha256']='0'*64
        elif edit=='order': q['character_index']=1
        elif edit=='expression': q['origin_reductions'][0]=[[True,1]]
        elif edit=='forward': q['dag_nodes'][0]['reductions']=[[0,1]]
        elif edit=='origin': q['dag_nodes'][0]['origin']={'kind':'bad'}
        elif edit=='node_lead_bool': q['dag_nodes'][0]['lead']=False
        else: q['downstream_claim_flags']={key:0 for key in FALSE_CLAIMS}
        reject(q)
    packed_rejected=0
    for raw,declared in ((bytes([1,81]),0),(pack_fixture([1,0,0,0]),1),(pack_fixture([2,0,0,0]),0)):
        try: analyze_block_row(raw,declared,0,0,8 if len(raw)==2 else 4)
        except RuntimeError: packed_rejected+=1
        else: raise RuntimeError('fixture_block_row')
    collision=summarize_old_leads([{'row':0,'lead':10,'coefficient':1,'local_lead':0},{'row':1,'lead':10,'coefficient':1,'local_lead':1}])
    if collision['global_echelonicity'] is not False or collision['duplicate_global_lead_count']!=1: raise RuntimeError('fixture_cross_family_collision')
    with tempfile.TemporaryDirectory() as td:
        root=Path(td); fixture_parent='fixture-parent'; fixture_body={'basis_blob':{'file':'fixture.bin'}}
        fixture_raw=canonical(fixture_body); fixture_digest=sha(fixture_raw)
        fixture_head={'body_sha256':fixture_digest,'parent_sha256':fixture_parent,
                      'schema':'d972.r07.a0.first-rung-grade1.v3.state.head','stem':'block-0'}
        (root/f'block-0.{fixture_digest}.json').write_bytes(fixture_raw)
        (root/'block-0.HEAD').write_bytes(canonical(fixture_head))
        (root/'fixture.bin').write_bytes(b'fixture')
        validate_block_envelope(root,0,{},fixture_digest,fixture_parent)
        bad_head=dict(fixture_head); bad_head['parent_sha256']='wrong-parent'
        (root/'block-0.HEAD').write_bytes(canonical(bad_head))
        try: validate_block_envelope(root,0,{},fixture_digest,fixture_parent)
        except RuntimeError: envelope_rejected=1
        else: raise RuntimeError('fixture_block_envelope')
    return {'semantic_rejections':rejected,'row_rejections':packed_rejected,
            'cross_family_collision':1,'envelope_accept':1,
            'envelope_wrong_parent_rejections':envelope_rejected}
def blob_fixture():
    with tempfile.TemporaryDirectory() as td:
        root=Path(td); data=bytes([0,80]); digest=sha(data); name='tiny.'+digest+'.bin'; (root/name).write_bytes(data)
        good={'file':name,'bytes':2,'sha256':digest,'rows':2,'width':4,'encoding':'base3-four-trits-per-byte'}
        validate_blob_receipt(root,good,2,4); tests=[]
        tests.append(({k:v for k,v in good.items() if k!='encoding'},2,4))
        tests.append(({**good,'rows':True},2,4)); tests.append(({**good,'width':4.0},2,4))
        tests.append(({**good,'encoding':'raw'},2,4)); tests.append(({**good,'file':'../'+name},2,4))
        tests.append((good,1,4)); tests.append((good,2,8))
        (root/('short.'+digest+'.bin')).write_bytes(data[:1]); tests.append(({**good,'file':'short.'+digest+'.bin'},2,4))
        (root/('trail.'+digest+'.bin')).write_bytes(data+b'\0'); tests.append(({**good,'file':'trail.'+digest+'.bin'},2,4))
        wrong='0'*64; (root/('bad.'+wrong+'.bin')).write_bytes(data); tests.append(({**good,'file':'bad.'+wrong+'.bin','sha256':wrong},2,4))
        bad=bytes([0,81]); bd=sha(bad); (root/('byte.'+bd+'.bin')).write_bytes(bad); tests.append(({**good,'file':'byte.'+bd+'.bin','sha256':bd},2,4))
        rejected=0
        for receipt,rows,width in tests:
            try: validate_blob_receipt(root,receipt,rows,width)
            except (RuntimeError,FileNotFoundError): rejected+=1
            else: raise RuntimeError('fixture_blob_receipt')
        return rejected
def ingest_prepare(path,retain=False):
    replay_started=time.perf_counter()
    path,names=scan_safe_root(path)
    hr=(path/'prepare.HEAD').read_bytes()
    digest='1f191d88a0453360021ec57d253a7d16c9a66ac059ddaaadb6db3e2b9293c865'
    br=(path/f'prepare.{digest}.json').read_bytes()
    serialized_body_bytes=len(br); b=validate_prepare_envelope(hr,br); del br,hr
    validate_input_binding(b,local_input_receipt())
    validate_prepare_roster(b)
    expression_counts=validate_old_records(b['old_blocks'],(505,503,503,503))
    receipts=[b['residual_blob']]+[x[k] for x in b['old_blocks'] for k in ('lower_basis_blob','lifted_grade_blob')]+[x['blob'] for x in b['packets']]
    if len(receipts)!=13 or len({r['file'] for r in receipts})!=13: raise RuntimeError('receipts')
    require_exact_roster(names,{'prepare.HEAD',f'prepare.{digest}.json',*(r['file'] for r in receipts)})
    authenticate_prepare_blobs(path,b)
    old_scan=scan_old_rows(path,b['old_blocks'],return_leads=retain); old_row_diagnostic,old_leads=old_scan if retain else (old_scan,None)
    total=sum(r['bytes'] for r in receipts)
    ranks=[]; nodes=seeds=actors=origins=0
    for i,x in enumerate(b['old_blocks']):
        r=x['record']; rank=(505,503,503,503)[i]; attempt=(2064,2056,2056,2056)[i]
        if x['rank']!=rank or r['rank']!=rank or r['attempts']!=attempt or r['queue_exhausted'] is not True or r['actor_order']!=[1,-1,2,-2] or len(r['seed_reductions'])!=44 or len(r['actor_transitions'])!=rank or any(len(z)!=4 for z in r['actor_transitions']): raise RuntimeError('block_counters')
        leads=set()
        for j,n in enumerate(r['dag_nodes']):
            if n['pivot']!=j or n['scale'] not in (1,2) or n['lead'] in leads or any(int(z[0])>=j or int(z[1]) not in (1,2) for z in n['reductions']): raise RuntimeError('dag')
            leads.add(n['lead'])
        ranks.append(rank);nodes+=len(r['dag_nodes']);seeds+=44;actors+=4*rank;origins+=attempt
    if ranks!=[505,503,503,503] or (nodes,seeds,actors,origins)!=(2014,176,8056,8232) or len(b['defect_origins'])!=8232 or sha(canonical(b['defect_origins']))!=b['defect_origin_sha256']: raise RuntimeError('totals')
    if (expression_counts['actor_rows'],expression_counts['actor_expressions'],expression_counts['seed_expressions'],expression_counts['dag_nodes'])!=(2014,8056,176,2014): raise RuntimeError('expression_counter_totals')
    result={'terminal':'TASK554_PREPARE_OLD_ROWS_SCANNED','body_sha256':digest,'ranks':ranks,'attempts_per_block':[2064,2056,2056,2056],'dag_rows':nodes,'origins':origins,'seed_expressions':seeds,'actor_expressions':actors,'expression_counters':expression_counts,'old_row_diagnostic':old_row_diagnostic,'authenticated_blob_bytes':total,'serialized_body_bytes':serialized_body_bytes,'streaming_chunk_ceiling':1048576,'elapsed_seconds':time.perf_counter()-replay_started,'peak_rss_bytes':peak_rss_bytes(),'roster_sha256':sha(canonical(sorted(names))),'memory':'parsed body JSON retained; serialized body deleted before blob pass; row slices only; 1MiB authentication buffer; OS cache not claimed free'}
    return (result,b,old_leads) if retain else result
def ingest_all_five(prepare_root,block_roots):
    started=time.perf_counter(); prepare_result,prepare,leads=ingest_prepare(prepare_root,retain=True); diagnostics=[]; next_row=2014
    for index,(root,rank) in enumerate(zip(block_roots,(1509,1512,1512,1512))):
        block_root,body,body_bytes=validate_block_envelope(root,index,prepare); counts=validate_block_semantics(body,prepare,index,rank); new_rows,scan=scan_block_basis(block_root,body,index,rank)
        for row in new_rows: row['row']=next_row; next_row+=1
        leads.extend(new_rows); diagnostics.append({'character_index':index,'body_sha256':PARENTS['block'+str(index)][1],'serialized_body_bytes':body_bytes,'basis_sha256':BLOCK_BASIS_SHA[index],**scan,'expression_counters':counts}); del body,new_rows
    summary=summarize_old_leads(leads)
    if summary['rows']!=8059 or summary['distinct_global_leads']!=8059 or summary['coefficient_one_global_leads']!=8059 or summary['global_echelonicity'] is not True: raise RuntimeError('p1_global_lead_completion')
    return {'terminal':'TASK554_ALL_FIVE_P1_STRUCTURALLY_INGESTED','prepare':prepare_result,'block_ranks':[1509,1512,1512,1512],'offsets':[0,505,1008,1511,2014,3523,5035,6547,8059],'blocks':diagnostics,'global_summary':summary,'elapsed_seconds':time.perf_counter()-started,'peak_rss_bytes':peak_rss_bytes(),'resident_matrix':False,'semantic_equations_replayed':False,'precision2':False,'verified':False}
def main():
    a=argparse.ArgumentParser();a.add_argument('--selftest',action='store_true');a.add_argument('--prepare-dir',type=Path);a.add_argument('--block-dirs',type=Path,nargs=4);x=a.parse_args()
    if x.selftest:selftest();return 0
    if x.block_dirs:
        if not x.prepare_dir: a.error('--block-dirs requires --prepare-dir')
        print(json.dumps(ingest_all_five(x.prepare_dir,x.block_dirs),sort_keys=True,separators=(',',':')));return 0
    if x.prepare_dir: print(json.dumps(ingest_prepare(x.prepare_dir),sort_keys=True,separators=(',',':')));return 0
    print(json.dumps({'status':'NOT_READY','reason':'Task640_step8_join'}));return 2
if __name__=='__main__':sys.exit(main())
