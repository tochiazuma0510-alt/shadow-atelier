#!/usr/bin/env python3
"""Task640: fresh precision-two endpoint-signature consumer.

The result-dependent path is intentionally downstream of an accepted Task601
receipt.  It never enters a grade-two owner or membership decision.
"""
from __future__ import annotations
import argparse, hashlib, importlib.util, json, os, struct, sys, tempfile, time
from pathlib import Path
import numpy as np

ROOT = Path(__file__).resolve().parents[1]
PREBUILD = ROOT / 'search/d972_r07_a0_first_rung_grade2_prebuild_v1.py'
PREBUILD_SHA256 = 'acffa38731a28d85539f765537010e6bf20f55c7f7feae0099d56c58c808ffc8'
V12F=ROOT/'search/d972_r07_history_free_positive_fast_resume_v12f.py'
V12F_SHA256='22d2ebda554cfacc78393dda7f43a9a6550e7f134dd8f44f87ab0f62241bbbbb'
T601_PRODUCER = 'ce036c4a1a92d16a78cb8da8c16dee282a6a981889f821e6df82eaecdd8fba0a'
T601_CHECKER = '8c3dd039368f63d62ef79694a196f73d0b626134df39673c5e48c98c7c8787f9'
TASK601_RUN, TASK601_ATTEMPT = '33734643746', '1'
TASK601_HEAD = 'b401d724bbdbef8cf67e96def22fc51c014ab546'
TASK601_ARTIFACT = 'task625-grade1-selected-slp-staged-v3-33734643746-1'
SOURCE_RUN, SOURCE_ATTEMPT = '33677346616', '1'
CANDIDATE_RUN, CANDIDATE_ATTEMPT = '33707397894', '1'
MARKER = 'R07_FRESH_PRECISION2_ENDPOINT_SIGNATURE_V4_CANDIDATE'
V484_PROOF_SHA256 = '25e292c8d996000c5dd442619f9afa269d83193ce5f58e4f3536c55b61f77492'
RUNTIME_PROFILE = {
    'profile': 'endpoint-minimal-v4',
    'contexts': 31,
    'context_named_uses': 46,
    'fine_source_order': 59049,
    'q0_marked_rows': 2,
    'generic_joint_closure': False,
    'generic_roster': False,
    'base_fox_rows': False,
    'pb3_boundary_rows': False,
    'pb4_boundary_rows': False,
    'generic_target': False,
    'generic_runtime_model': False,
    'v484_proof_sha256': V484_PROOF_SHA256,
    'v12f_sha256': V12F_SHA256,
    'task565_prebuild_sha256': PREBUILD_SHA256,
    'words_sha256': '90ba603368307e16b27b2bad9d84847c7bedc501fab811b8919d96e3c8936893',
    'g760_sha256': '518f09820b8d7baee6b58ebf366cebf7b02a9a945cd1350cf8c701a4e6bc2b4d',
}

LEDGER_SHA = '040ab853535db8aad06fba295adf8b59bb1cd77435e7c64a1edcc34cdacb4cd7'
TEN = (0, 1, 2, 3, 0, 4, 5, 6, 7, 8, 9)
SIGNS = (1, -1, 1, -1, -1, 1, 1, 1, 1, -1, -1)
SEEDS, LOWER, TOP, PACKED = 44, 32260, 48384, 12096
WORDS_SHA='90ba603368307e16b27b2bad9d84847c7bedc501fab811b8919d96e3c8936893'
PURE = (((), (0, 0)), ((-2,) * 9, (0, 1)), ((-2, -2, 1, 1, 2, 1, 2, 1, 1), (1, 0)), ((-2, -2, -2, -1, -2, -1, -1, -1, -2, -1), (1, 1)))
PAPER_PINS = {'sol/proof_r07_selected_slp_leaf_gated_precision2_join_v470.md':'b56aa15ee87b4831cc999525233cfadbe8e62cd25c0503c0c98fce3106fb2b7a','sol/sol_reply_611_audit_r07_selected_slp_leaf_gated_precision2_join_v1.md':'4212afae131eda13c8d1199bd2a41ad2b232957fd8de2d565fbfe24e34fccd92','sol/proof_r07_endpoint_signature_precision2_consumer_v471.md':'38d271514baf838953b6003f954be60c689771f0fd1c9fec14de1dfc55daf99f','sol/sol_reply_613_audit_r07_endpoint_signature_precision2_consumer_v1.md':'04acf864fd2fd95c13880510feb5087588f3f3970418f47ed44614f5bc74f75b','sol/sol_reply_622_reaudit_r07_task601_packed_memory_release_v3.md':'4eaf1f92f4ef1fdd0a7f3289175d7c8b97c5ac85714b0b368d4aa66a20f151e0'}
PAPER_PINS.update({'sol/sol_reply_627_audit_r07_task623_endpoint_consumer_v2.md':'5ce7efabb36c454c688248249acd47ee9c6e4594039cb872674101e34239538c','sol/sol_reply_630_audit_r07_precision2_actual_context_contract.md':'d64122daa3b6396e494d8309eb98ecadebad2062a173a80fca2ab88baacd7dd1','sol/proof_r07_eleven_endpoint_six_row_restriction_repair_v478.md':'a7e5df7f14d35b7dc971127e187fbc16abe00b3b5190fac341666b94bbf1e72b','sol/sol_reply_636_reaudit_r07_eleven_endpoint_six_row_v478.md':'2cdecfcb47cf6727d45cbc7cf494c84230a5be5af489d6bca306a4df04552c79','sol/sol_reply_639_audit_r07_task625_success_artifact.md':'b48fe4bfb43aedb76c9109e2ca73e7a9de323687c69c64807e74f3ad62db0a1b','sol/proof_r07_first_rung_witness_presentation_dovetail_v479.md':'df6850c9e7c86a83ade26c37064a7deb38ec3c8d7907b1eec6ff0d5268b22986','sol/sol_reply_641_audit_r07_first_rung_dovetail_v479.md':'498df880f86805cffab50756dc32435a2a79a3426071c7bdd290820a6dadddf7','sol/luna_task_643_r07_task640_compositional_parent_amendment.md':'0ae5a1e7724bb878a36d7382ad3f393cdaff486cc036e6fe41a7e565e257bac5','sol/proof_r07_a0_affine_truncated_two_rung_engine_v443.md':'80970217b415d7b764e399b5ce5892075b1f82f7f87f0c6199e9f6b0e404f24c','sol/proof_r07_a0_psl504_occurrence_floor_v437.md':'4671e1f46e5489355b850e7f2c04d73d36d96d7eca1feadde199b56ae273e3d6','sol/proof_r07_a0_relative_fibre_echelon_lift_v441.md':'5cb52ffd02d2cd5c89e08080931065123a7208f7d5a2878acddb5d9ac2958fbb','sol/proof_r07_first_rung_graded_fourier_blocks_v445.md':'98d073c896cae8304252327ea285b876f8868b6c2d00e8ba3c00465ea86612e7','sol/proof_r07_first_rung_character_blocks_coupled_monomials_v446.md':'389ceee1250b892ec4845753af23f4455e619e2d72782931645d8b8176764756','sol/proof_r07_grade1_to_grade2_split_presentation_handoff_repair_v451.md':'3ec2d1351e16bf0fcde3abe8da346b8765b26c30796ff48e415c46ac51d933b4','sol/proof_r07_selected_slp_adjoint_fox_replay_v467.md':'f80a63b2db0efe56777a48d1ddaab61518df9a802884549834e63e517e9a8dc5','sol/proof_r07_canonical_selected_dependency_slp_v468.md':'b1e0f09ae0c6f136804e37bc8db8cba85bccede0880ed5f26afed880d28829a6','sol/proof_r07_canonical_selected_dependency_slp_physical_replay_v469.md':'bae6864e6f00f65bfd3ff18a4c5676d5afe190ad0f2c6ffaf83cd9683d3f26f6','sol/proof_r07_selected_slp_staged_adjoint_repair_v475.md':'757ffab5aa011643efa3df4b133dc03d423895d57a003ed6830a47528388148e'})

LEAF_HEADER=struct.Struct('<8sBBBB32sQ'); LEAF_RECORD=struct.Struct('<IIBI')
EXPECTED_FILES={
'grade_edges':('grade-edges.bin',12372120,'aa3a506fd2f1358e6edce102d5fb6f129a4b75bd2675e03bb401f01904e47557'),
'grade_nodes':('grade-nodes.bin',146276,'6b79485d9c69a05cf0d6c64788bc4f341792c8cedbb4f00cd1fdc887d42ca82b'),
'grade_origins':('grade-origins.bin',30506112,'fcc5e5e43a9923b549e0b894c8ab995e545f78563134f37dae99917026283e68'),
'literal_leaves':('literal-leaves.bin',565981,'4a0b631004c9fbbf0b3cc965ff606711e04081c7d79beecb2db6b7be264fc851'),
'lower_companions':('lower-companions.bin',10045728,'299ff5f214d32a85bea401705bffe01b2cf4f4f327c50a34f26fed1ba433dcaa'),
'lower_edges':('lower-edges.bin',1911741,'b83e05df054d43952640b4442f08fb54aadf3303675dedc5443268aa3c3e9809'),
'lower_nodes':('lower-nodes.bin',48169,'4e9b5a98f9b434649d3eeac664fdcdc029d81a1247b193cb3260dabe2c22ee3c'),
'lower_origins':('lower-origins.bin',3350237,'1cbbb4444858828d9b3ddb78c799a087c6ada69b058155f02d11e5f63316135c'),
'lower_stored':('lower-stored.bin',3350237,'50361df9c85a525e0c3f73a2ef82a337a870b3cb4eb30caad5816df49c98a683'),
'old_lower_zero':('old-lower-zero.bin',712001,'f2793fac59ae4cb798f479f764eb494b5db51256fb7d01dfc523000a7b217a33'),
'roots':('roots.json',255846,'af1b035e0eb0af6e593770affb52a52905609fd9c19e988b0b7e8cf69e7592c5'),
'selected_grade':('selected-grade.bits',631,'e2fd7f3147f4880e42d6da6f211f2ed7991af9d9d1925416ec30120c46ac832a'),
'selected_lower':('selected-lower.bits',208,'771af58b72061d7c94ec28c9086c375bf4e1c5b55254cbb11a541fea4093d48e'),
'source_ancestry':('source-ancestry.json',149359882,'315f9d9be5c7301b7b54ca5f545a17ca1d491f2d1d24e40f426ce831388f2908'),
'source_refs':('source-refs.json',19876945,'18767d10ab9e697c5f9cb54fbdcabfbc1824c0f4e0afde15e0e550e4a3b781ea')}
DECISION_BODY='62412762b3a208d31febb6c6b8d4707f880471ed32cf62c79c18108065ab7b5d'
DECISION_HEAD='07de7a817e8c5ae2e7346402a290c32631d05b0cc621d03702faa6cb43a948c0'
BASIS_SHA='b562c980c22a25a932bae1b548f72aeede5637b9612afc908fff9a9aecff069d'; REMAINDER_SHA='564cbfafc869a8c6eb761a392caa5e792b546bf577af7fe808177b2fdf13cbb0'
PREPARE_SHA='1f191d88a0453360021ec57d253a7d16c9a66ac059ddaaadb6db3e2b9293c865'


def sha(data): return hashlib.sha256(data).hexdigest()
def sha_obj(value): return sha(json.dumps(value, sort_keys=True, separators=(',', ':'), ensure_ascii=True).encode('ascii'))
def canon(value): return (json.dumps(value, sort_keys=True, separators=(',', ':'), ensure_ascii=True) + '\n').encode('ascii')
def fail(reason): raise RuntimeError(reason)
def freely_reduce(word):
    out=[]
    for value in word:
        value=int(value)
        if value not in (-2,-1,1,2): fail('actor_letter')
        if out and out[-1] == -value: out.pop()
        else: out.append(value)
    return tuple(out)
def terms(value):
    if not isinstance(value,list): fail('terms_shape')
    acc={}
    for item in value:
        if not isinstance(item,list) or len(item)!=3 or type(item[0]) is not int or not 1<=item[0]<=SEEDS or type(item[2]) is not int or item[2] not in (1,2): fail('terms_semantics')
        key=(item[0],freely_reduce(item[1])); acc[key]=(acc.get(key,0)+item[2])%3
    return [[s,list(w),c] for (s,w),c in sorted(acc.items()) if c]
def guard(started):
    if time.monotonic()-started > float(os.environ.get('TASK640_SECONDS','5400')): fail('UNKNOWN_RESOURCE:time')
    try:
        import resource
        if resource.getrusage(resource.RUSAGE_SELF).ru_maxrss*1024 > int(os.environ.get('TASK640_MAX_RSS',str(7*1024**3))): fail('UNKNOWN_RESOURCE:rss')
    except ImportError: pass
def load_kernel():
    if sha(PREBUILD.read_bytes()) != PREBUILD_SHA256: fail('prebuild_sha256')
    if str(ROOT/'search') not in sys.path: sys.path.insert(0,str(ROOT/'search'))
    spec=importlib.util.spec_from_file_location('task640_pinned_kernel',PREBUILD)
    if spec is None or spec.loader is None: fail('kernel_loader')
    module=importlib.util.module_from_spec(spec); spec.loader.exec_module(module); return module
def require(condition,message):
    if not condition: fail(message)
class EndpointMinimalJointEvaluator:
    """The exact J.identity/J.eval projection required by direct_column."""
    __slots__ = ('_old', '_e3', '_e4', '_contexts', 'identity')

    def __init__(self, old, e3, e4, contexts):
        require(len(contexts) == 31, 'endpoint context evaluator width')
        self._old, self._e3, self._e4 = old, e3, e4
        self._contexts = tuple(contexts)
        self.identity = (e3.identity, tuple(e4.identity for _ in self._contexts))

    def eval(self, word):
        return (self._e3.eval(self._old.embed_f2_pb3(word)),
                tuple(self._e4.eval(word, context)
                      for context in self._contexts))


def runtime_profile_gate(value):
    require(value == RUNTIME_PROFILE, 'endpoint runtime profile')


def validate_context_registry(contexts, aliases, context_public, serializer):
    require(type(contexts) is list and len(contexts) == 31,
            'endpoint context count')
    require(type(aliases) is dict and len(aliases) == 46 and
            all(type(value) is int and 1 <= value <= 31
                for value in aliases.values()), 'endpoint context aliases')
    require(type(context_public) is dict and
            context_public.get('context_count') == 31 and
            context_public.get('named_use_count') == 46 and
            context_public.get('deduplication') == 'exact E4 pair equality',
            'endpoint context receipt')
    rows = context_public.get('contexts')
    named = context_public.get('named_uses')
    require(type(rows) is list and len(rows) == 31 and
            type(named) is list and len(named) == 46,
            'endpoint context receipt rows')
    require(named == [{'name': name, 'context_id': value}
                      for name, value in aliases.items()],
            'endpoint context alias receipt')
    require([row.get('context_id') for row in rows] == list(range(1, 32)),
            'endpoint context order')
    require(context_public.get('context_rows_sha256') ==
            sha_obj(rows) and
            context_public.get('named_use_mapping_sha256') == sha_obj(named),
            'endpoint context receipt digest')
    for index, (pair, row) in enumerate(zip(contexts, rows), 1):
        require(type(pair) is tuple and len(pair) == 2 and
                row.get('left_hex') == serializer(
                    pair[0], 'endpoint context left').hex() and
                row.get('right_hex') == serializer(
                    pair[1], 'endpoint context right').hex(),
                'endpoint context row binding')
    return context_public


def validate_q0_marked(q3):
    coarse = q3.get('coarse_models') if isinstance(q3, dict) else None
    model = coarse.get('Q0') if isinstance(coarse, dict) else None
    marked = model.get('marked_permutations') if isinstance(model, dict) else None
    require(type(marked) is list and len(marked) == 2,
            'endpoint Q0 marked row count')
    for row in marked:
        require(type(row) is list and len(row) == 36 and
                sorted(int(value) for value in row) == list(range(1, 37)),
                'endpoint Q0 marked row domain')
    return marked


def endpoint_runtime_profile_gate(runtime):
    forbidden = {
        'joint_closure', 'joint_roster', 'roster', 'raw_base_targets',
        'pb3_boundary_rows', 'pb4_boundary_rows', 'target', 'light_public',
        'producer_exact_target', 'qstates', 'qids', 'parents', 'memberships',
    }
    require(forbidden.isdisjoint(runtime),
            'endpoint forbidden generic runtime object')


def endpoint_checkpoint(meter, phase):
    meter.check(phase)
    print('A0_PROGRESS side=producer phase=' + phase +
          ' elapsed_seconds=' + str(int(time.monotonic() - meter.started)),
          flush=True)


def build_endpoint_minimal(module, registry, meter, words):
    """Build exactly the seven v484 consumer steps, with no generic prefix."""
    registry.authenticate(meter)
    endpoint_checkpoint(meter, 'endpoint_minimal_step_1_source_authentication')

    live = registry.load('live')
    p176 = registry.load('task176')
    old = registry.load('old')
    q3 = registry.json('q3')
    # v5: bind the Q3 literal-owner validator to the pinned v12f module.
    q3_owner = module.validate_q3_literal_owner(q3)
    endpoint_checkpoint(meter, 'endpoint_minimal_step_2_load_sources')

    e3, e4, _ = old.reconstruct_quotients(q3)
    endpoint_checkpoint(meter, 'endpoint_minimal_step_3_reconstruct_quotients')

    contexts, aliases, context_public = old.cheap_context_registry(e4)
    validate_context_registry(
        contexts, aliases, context_public,
        lambda value, label: p176.packed_joint_blob(value, label))
    endpoint_checkpoint(meter, 'endpoint_minimal_step_4_context_registry')

    g760 = [int(value) for value in words.get('g760', ())]
    require(len(g760) == 760 and sha_obj(g760) ==
            RUNTIME_PROFILE['g760_sha256'], 'endpoint g760 pin')
    endpoint_checkpoint(meter, 'endpoint_minimal_step_5_g760_pin')

    runtime = {
        'live': live, 'p176': p176, 'old': old, 'e3': e3, 'e4': e4,
        'contexts': contexts, 'aliases': aliases,
        'context_public': context_public, 'q3': q3,
        'q3_literal_owner': q3_owner, 'meter': meter,
        'bridge': {'g760': {'word': list(g760), 'sha256': sha_obj(g760)}},
    }
    endpoint_runtime_profile_gate(runtime)
    endpoint_checkpoint(meter, 'endpoint_minimal_step_6_fine_deletion_before')
    install_endpoint_deletion(runtime)
    endpoint_checkpoint(meter, 'endpoint_minimal_step_6_fine_deletion_after')

    runtime['joint_group'] = EndpointMinimalJointEvaluator(
        old, e3, e4, contexts)
    producer = module.ProducerAllSeven(runtime)
    endpoint_checkpoint(meter, 'endpoint_minimal_step_7_joint_evaluator')
    identity_e3 = p176.packed_joint_blob(
        e3.identity, 'endpoint zero E3 identity')
    identity_e4 = p176.packed_joint_blob(
        e4.identity, 'endpoint zero E4 identity')
    require(producer.coordinates(()) ==
            (identity_e3,) * 5 + (identity_e4,) * 5,
            'endpoint_zero_canary')
    endpoint_checkpoint(meter, 'endpoint_minimal_step_7_zero_word_canary')
    return module, producer, runtime


def load_all_seven(words):
    if sha(V12F.read_bytes()) != V12F_SHA256:
        fail('v12f_sha256')
    spec = importlib.util.spec_from_file_location('task640_v12f', V12F)
    if spec is None or spec.loader is None:
        fail('v12f_loader')
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    meter = module.Meter(float(os.environ.get('TASK640_SECONDS', '9600')))
    endpoint_checkpoint(meter, 'endpoint_minimal_start')
    snapshots = {key: (ROOT / row[0]).read_bytes()
                 for key, row in module.SOURCE_PINS.items()}
    registry = module.SourceRegistry(snapshots)
    return build_endpoint_minimal(module, registry, meter, words)


def install_endpoint_deletion(runtime):
    """Install only the endpoint deletion prefix required by the producer."""
    p176,old=runtime['p176'],runtime['old']
    e3,e4=runtime['e3'],runtime['e4']
    fine,fine_public=p176.build_fine_deletion(e3,e4,runtime['meter'])
    if not isinstance(fine_public,dict) or fine_public.get('source_order')!=59049:
        fail('endpoint_fine_source_order')
    q0_rows = validate_q0_marked(runtime['q3'])
    q0_marked=[p176.canonical_packed_permutation(
        old.perm_from_row(row,36),36,'task640 Q0 mark')
        for row in q0_rows]
    delete,deletion_public=p176.make_deleter(old,e3,e4,fine,q0_marked)
    if not callable(delete): fail('endpoint_delete_callable')
    deletion_public['fine']=fine_public
    runtime.update({'delete':delete,'deletion_public':deletion_public})
    if 'delete' not in runtime or not callable(runtime['delete']):
        fail('endpoint_delete_install')
    return runtime
def authenticate_paper_pins():
    for name,digest in PAPER_PINS.items():
        path=ROOT/name
        if not path.is_file() or sha(path.read_bytes())!=digest: fail('paper_pin:'+name)
def parse_literal_leaves(raw,ancestry_digest):
    if len(raw)<LEAF_HEADER.size: fail('leaf_header_short')
    magic,version,quotient_specific,common,states_exported,binding,count=LEAF_HEADER.unpack_from(raw)
    if (magic,version,quotient_specific,common,states_exported)!=(b'R07LEAF1',1,1,0,0) or binding.hex()!=ancestry_digest: fail('leaf_header')
    if count>int(os.environ.get('TASK640_RECORD_CAP','100000')): fail('UNKNOWN_RESOURCE:record_cap')
    cursor=LEAF_HEADER.size; previous=None; result=[]
    for _ in range(count):
        if cursor+LEAF_RECORD.size>len(raw): fail('leaf_record_short')
        payload,seed,coefficient,length=LEAF_RECORD.unpack_from(raw,cursor); cursor+=LEAF_RECORD.size
        if length>int(os.environ.get('TASK640_PATH_LENGTH_CAP','4096')): fail('UNKNOWN_RESOURCE:path_length_cap')
        if payload!=9+length or cursor+length>len(raw) or not 1<=seed<=SEEDS or coefficient not in (1,2): fail('leaf_record')
        path=tuple(struct.unpack_from('<%db'%length,raw,cursor)) if length else (); cursor+=length
        if freely_reduce(path)!=path: fail('leaf_not_reduced')
        key=(seed,path)
        if previous is not None and key<=previous: fail('leaf_order')
        previous=key; result.append([seed,list(path),coefficient])
    if cursor!=len(raw): fail('leaf_eof')
    return result
def raw_seed_gate(raw_terms):
    seeds=sorted({int(row[0]) for row in raw_terms})
    if any(not 1<=seed<=SEEDS for seed in seeds): fail('raw_seed')
    return seeds
def state_key(item): return (item.get('kind'),tuple(int(x) for x in item.get('ids',[])),tuple(int(x) for x in item.get('prefix',[])))
def sign(label,parity): return 1 if ((int(label[0])*parity[0]+int(label[1])*parity[1])&1)==0 else 2
def recompute_leaves(ancestry):
    states=ancestry.get('derived',{}).get('states'); roots=ancestry.get('roots')
    if not isinstance(states,list) or not isinstance(roots,list): fail('derived_shape')
    table={}
    for state in states:
        key=state_key(state)
        if key in table: fail('derived_duplicate')
        table[key]=state
    out={}; visits=0
    def emit(seed,word,coefficient):
        key=(int(seed),freely_reduce(word)); value=(out.get(key,0)+int(coefficient))%3
        if value: out[key]=value
        else: out.pop(key,None)
    def walk(edge):
        nonlocal visits
        state=table.get(state_key(edge))
        if state is None: fail('derived_missing')
        visits+=1
        if visits>20000000: fail('UNKNOWN_RESOURCE:derived_edges')
        coefficient=int(edge.get('coefficient',0))%3
        if state.get('kind')=='old':
            node=state.get('source_node',{}); origin=node.get('origin',{}) if isinstance(node,dict) else {}
            if origin.get('kind')=='projected_seed':
                seed=int(state.get('seed_index',origin.get('seed',0))); ref=state.get('source_ref',{}); ch=int(ref.get('character',0)); label=(ch>>1,ch&1)
                for word,parity in PURE: emit(seed,tuple(state.get('prefix',[]))+tuple(word),coefficient*sign(label,parity))
        for child in state.get('children',[]): walk(child)
    for root in roots: walk(root)
    return [[s,list(w),c] for (s,w),c in sorted(out.items())]
def auth_parent(path):
    manifest_raw=(path/'manifest.json').read_bytes(); manifest=json.loads(manifest_raw)
    if canon(manifest)!=manifest_raw or sha(manifest_raw)!='381f961fc808076c5c0adbc98e32c19742565087bffbcd5f99772533e05d5c22': fail('task601_manifest')
    if manifest.get('cursor')!=8059 or manifest.get('lower_offer_count')!=2014 or manifest.get('grade_offer_count')!=6398 or manifest.get('lower_rank')!=1661 or manifest.get('grade_rank')!=5044: fail('task601_route')
    for key,expected in {'direct_occurrence_replay':False,'next_degree2_residual':None,'A0':False,'COMMON':False,'FAKE':False,'IHARA':False,'cross_checked':False,'verified':False}.items():
        if key not in manifest or manifest[key] is not expected: fail('task601_claims')
    files=manifest.get('files',{}); loaded={}
    if not isinstance(files,dict) or set(files)!=set(EXPECTED_FILES): fail('task601_files')
    for key,(filename,size,digest) in EXPECTED_FILES.items():
        receipt=files[key]
        if receipt!={'file':filename,'bytes':size,'sha256':digest}: fail('task601_receipt')
        target=path/filename
        if target.stat().st_size!=size: fail('task601_receipt_size')
        h=hashlib.sha256()
        with target.open('rb') as stream:
            for chunk in iter(lambda:stream.read(1024*1024),b''): h.update(chunk)
        if h.hexdigest()!=digest: fail('task601_receipt_sha')
        if key in ('roots','literal_leaves'): loaded[key]=target.read_bytes()
    if sum(item[1] for item in EXPECTED_FILES.values())!=232502114 or len(manifest_raw)+232502114!=232511148: fail('task601_payload_size')
    if manifest.get('roots') != files.get('roots',{}).get('file'): fail('task601_roots_pointer')
    roots_raw=loaded.get('roots')
    if roots_raw is None or canon(json.loads(roots_raw))!=roots_raw: fail('task601_canonical')
    rebuilt=parse_literal_leaves(loaded['literal_leaves'],EXPECTED_FILES['source_ancestry'][2])
    verdict_path=path/'task625-verdict.json'
    verdict_raw=verdict_path.read_bytes(); verdict=json.loads(verdict_raw)
    if len(verdict_raw)!=1120 or sha(verdict_raw)!='a650aa8d5d78f52145fff5ba7769ad2036cfd16e90e3caaf367b4517e07d2740' or canon(verdict)!=verdict_raw or verdict.get('marker')!='R07_GRADE1_SELECTED_SLP_V2_CHECKER_PASS': fail('task601_verdict')
    if verdict.get('verified') is not False or verdict.get('cross_checked') is not False or verdict.get('cursor')!=8059 or verdict.get('coefficient_count')!=3317: fail('task601_verdict_fields')
    if (path/'task625-replayed-verdict.json').read_bytes()!=verdict_raw: fail('task601_independent_replay')
    roots=json.loads(roots_raw)
    if roots.get('C_1')!={'type':'Compose','left':'C_<1','right':'C_T'} or roots.get('C_T',{}).get('type')!='OrderedProduct' or len(roots.get('C_T',{}).get('children',[]))!=3317 or roots.get('C_<1',{}).get('type')!='RegisteredPriorProduct' or len(roots.get('C_<1',{}).get('terms',[]))!=2622: fail('task601_roots')
    for key,expected in {'direct_occurrence_replay':False,'next_degree2_residual':None,'A0':False,'COMMON':False,'FAKE':False,'IHARA':False,'cross_checked':False,'verified':False}.items():
        if key not in roots or roots[key] is not expected: fail('task601_root_claims')
    return manifest,loaded,roots,rebuilt
def auth_candidate(path,roots):
    head_raw=(path/'decision-v2.HEAD').read_bytes(); head=json.loads(head_raw)
    if sha(head_raw)!=DECISION_HEAD or canon(head)!=head_raw or head.get('body_sha256')!=DECISION_BODY: fail('candidate_head')
    body_raw=(path/f'decision-v2.{DECISION_BODY}.json').read_bytes(); body=json.loads(body_raw)
    coefficients=body.get('member_coefficients')
    if sha(body_raw)!=DECISION_BODY or canon(body)!=body_raw or body.get('terminal')!='GRADE1_DECISION_MEMBER' or body.get('lower_rank')!=1661 or body.get('grade_rank')!=5044 or not isinstance(coefficients,list) or len(coefficients)!=3317: fail('candidate_body')
    expected=[{'type':'GradeNodeRef','pivot':int(p),'coefficient':int(c)} for p,c in coefficients]
    if roots.get('C_T')!={'type':'OrderedProduct','children':expected}: fail('candidate_root_order')
    basis=(path/body['basis_receipt']['file']).read_bytes(); remainder=(path/body['remainder_receipt']['file']).read_bytes()
    if len(basis)!=30506112 or sha(basis)!=BASIS_SHA or len(remainder)!=6048 or sha(remainder)!=REMAINDER_SHA or any(remainder): fail('candidate_member_equation')
    return body
def auth_state(path):
    head_raw=(path/'prepare.HEAD').read_bytes(); head=json.loads(head_raw)
    if canon(head)!=head_raw or head.get('body_sha256')!=PREPARE_SHA: fail('state_prepare')
def signature(path,model):
    coordinates=model.coordinates(path)
    if len(coordinates)!=10: fail('eleven_coordinate_source')
    return tuple(('E3' if j<6 else 'E4',coordinates[tag]) for j,tag in enumerate(TEN))
def extend_signature(parent,letter,model,v12f):
    atom=signature((letter,),model); answer=[]
    for index,((kind,left_raw),(_kind,right_raw)) in enumerate(zip(parent,atom)):
        block=1 if index<6 else 3; quotient=model.rt['e3'] if index<6 else model.rt['e4']
        left=v12f.producer_unpack_element(model.rt,left_raw,block); right=v12f.producer_unpack_element(model.rt,right_raw,block)
        answer.append((kind,v12f.producer_element_blob(model.rt,quotient.mul(left,right))))
    return tuple(answer)
def first_six_shift_gate(context,expected_shifts):
    if tuple(context.physical_shifts)!=expected_shifts: fail('first_six_prefix_table')
def evaluate(roots,replaced,loaded,task601,candidate,out):
    candidate_body=auth_candidate(candidate,roots)
    words_path=ROOT/'scratchpad/a0_paper_words_v1.json'
    if sha(words_path.read_bytes())!=WORDS_SHA: fail('words_sha256')
    kernel=load_kernel(); words=json.loads(words_path.read_text(encoding='utf-8')); context=kernel.grade1.Context(words)
    if tuple(context.aggregate_table)!=((0,0,1),(1,0,2),(2,0,1),(3,1,2),(4,1,2),(5,1,1)): fail('first_six_sign_block_table')
    gtags=context.source_word_tags(tuple(map(int,words['g760']))); identity=(kernel.grade1.floor.ID9,0,0,(0,0,0))
    expected_shifts=(identity,gtags[2],gtags[2],kernel.grade1.affine_mul(gtags[5],kernel.grade1.affine_inv(gtags[4])),gtags[5],gtags[5])
    first_six_shift_gate(context,expected_shifts)
    _v12f,all_seven,seven_runtime=load_all_seven(words)
    prior=roots.get('C_<1',{}).get('terms',[]); raw_terms=prior+replaced
    reached_seeds=raw_seed_gate(raw_terms); complete=terms(raw_terms); paths=sorted({tuple(x[1]) for x in complete})
    if len(paths)>int(os.environ.get('TASK640_PATH_CAP','2000000')): fail('UNKNOWN_RESOURCE:path_cap')
    trie={():signature((),all_seven)}
    for path in paths:
        for n in range(1,len(path)+1):
            prefix=path[:n]
            if prefix not in trie:
                trie[prefix]=extend_signature(trie[prefix[:-1]],prefix[-1],all_seven,_v12f)
                if len(trie)>int(os.environ.get('TASK640_TRIE_CAP','2000000')): fail('UNKNOWN_RESOURCE:trie_cap')
                if trie[prefix]!=signature(prefix,all_seven): fail('trie_right_recurrence')
    base_checks=len(reached_seeds)*11
    if base_checks>484: fail('endpoint_ceiling')
    for seed in reached_seeds:
        endpoints=all_seven.coordinates(tuple(int(x) for x in words['relators'][seed-1]))
        identities=(all_seven.rt['e3'].identity,all_seven.rt['e4'].identity)
        for j,tag in enumerate(TEN):
            if endpoints[tag] != all_seven.rt['p176'].packed_joint_blob(identities[j>=6],'endpoint identity'): fail('endpoint_gate')
    for seed,path,_coefficient in complete:
        all_seven.direct_column(path,tuple(int(x) for x in words['relators'][seed-1]))
        guard(started)
    buckets={}
    for seed,word,coefficient in complete:
        key=(seed,trie[tuple(word)]); buckets[key]=((buckets.get(key,(0,tuple(word)))[0]+coefficient)%3,tuple(word))
    buckets={k:v for k,v in buckets.items() if v[0]};
    if len(buckets)>len(complete): fail('signature_bound')
    if len(complete)+len(trie)+len(buckets)>int(os.environ.get('TASK640_STATE_CAP','50000000')): fail('UNKNOWN_RESOURCE:state_cap')
    cache={i+1:kernel.evaluate_seed_precision2(context,tuple(map(int,w))) for i,w in enumerate(words['relators'])}
    replay=[np.zeros(kernel.PHYSICAL_DEGREE0_WIDTH,dtype=np.uint8),np.zeros(kernel.PHYSICAL_DEGREE1_WIDTH,dtype=np.uint8),np.zeros(kernel.PHYSICAL_DEGREE2_WIDTH,dtype=np.uint8),np.zeros(4,dtype=np.uint8)]
    for (seed,_),(coefficient,path) in buckets.items():
        acted=kernel.act_precision2(context,*cache[seed],context.source_word_tags(path)); physical=kernel.aggregate_precision2(context,*acted)
        for dst,src in zip(replay,physical): dst[:]=(dst.astype(np.uint16)+coefficient*src.astype(np.uint16))%3
        guard(started)
    target=kernel.direct_target_precision2(context,words); difference=tuple(((a.astype(np.int16)-b.astype(np.int16))%3).astype(np.uint8) for a,b in zip(target,replay)); lower=np.concatenate((difference[0],difference[1],difference[3]))
    if lower.size!=LOWER or np.any(lower): fail('lower_nonzero')
    rho2=difference[2]; packed=kernel.grade1.pack_trits(rho2).tobytes()
    if len(packed)!=PACKED: fail('rho2_width')
    decoded=kernel.grade1.unpack_trits(np.frombuffer(packed,dtype=np.uint8),TOP)
    if not np.array_equal(decoded,rho2): fail('rho2_roundtrip')
    if out.exists(): fail('output_exists')
    out.parent.mkdir(parents=True,exist_ok=True)
    stage=Path(tempfile.mkdtemp(prefix='.task640-',dir=out.parent))
    def store(name,data):
        if len(data)>int(os.environ.get('TASK640_DURABLE_CAP',str(1024**3))): fail('UNKNOWN_RESOURCE:durable')
        (stage/name).write_bytes(data); return {'file':name,'bytes':len(data),'sha256':sha(data)}
    target_dense=np.concatenate(target).astype(np.uint8).tobytes(); lower_dense=lower.astype(np.uint8).tobytes(); top_dense=rho2.astype(np.uint8).tobytes()
    path_rows=[[list(path),[[kind,raw.hex()] for kind,raw in trie[path]]] for path in sorted(trie)]
    bucket_rows=[[seed,[[kind,raw.hex()] for kind,raw in sig],coefficient,list(path)] for (seed,sig),(coefficient,path) in sorted(buckets.items(),key=lambda row:(row[0][0],repr(row[0][1])))]
    receipts={
      'rho2_packed':store('rho2.bin',packed),'rho2_dense':store('rho2-dense.bin',top_dense),
      'lower_dense':store('lower-dense.bin',lower_dense),'target_dense':store('target-dense.bin',target_dense),
      'path_signatures':store('path-signatures.json',canon(path_rows)),
      'signature_buckets':store('signature-buckets.json',canon(bucket_rows)),
      'roots':store('authenticated-roots.json',loaded['roots'])}
    sparse=[[int(i),int(rho2[i])] for i in np.flatnonzero(rho2)]
    parent={'task601_run':TASK601_RUN,'task601_attempt':TASK601_ATTEMPT,'task601_head':TASK601_HEAD,'task601_job':100582244001,'task601_job_name':'selected-slp','task601_artifact':TASK601_ARTIFACT,'task601_artifact_id':9885925239,'task601_artifact_bytes':50793121,'task601_artifact_digest':'sha256:ac3121f3bc1a7e2a6c267f20352e953b7343f9085015dd74e4a67e4b90129a75','task601_manifest_sha256':sha((task601/'manifest.json').read_bytes()),'task601_producer_sha256':T601_PRODUCER,'task601_checker_sha256':T601_CHECKER,'task601_replayed_verdict_sha256':'a650aa8d5d78f52145fff5ba7769ad2036cfd16e90e3caaf367b4517e07d2740','source_run':SOURCE_RUN,'candidate_run':CANDIDATE_RUN,'decision_sha256':DECISION_BODY,'basis_sha256':BASIS_SHA,'remainder_sha256':REMAINDER_SHA}
    runtime_profile_gate(RUNTIME_PROFILE)
    manifest={'schema':'d972.r07.a0.fresh-precision2-endpoint-signature.v4','marker':MARKER,'runtime_profile':RUNTIME_PROFILE,'parent':parent,'root':'Compose(C_<1,C_T)','source_ancestry_sha256':EXPECTED_FILES['source_ancestry'][2],'roots_sha256':sha(loaded['roots']),'occurrence':{'count':11,'types':['E3']*6+['E4']*5,'coordinates':list(TEN),'signs':list(SIGNS),'base_checks':base_checks,'max_base_checks':484,'all_seven_canary':True,'first_six_typed_restriction':True},'compression':{'L':len(complete),'U':len(trie),'G':len(buckets),'G_le_L':len(buckets)<=len(complete),'seed_cache_count':len(cache)},'dimensions':{'lower':LOWER,'top':TOP,'packed_rho2':PACKED},'rho2':{'support':len(sparse),'sparse_sha256':sha(canon(sparse)),'dense_sha256':sha(top_dense),'packed_sha256':sha(packed),'packing_roundtrip':True},'files':receipts,'degree1_task625_physical_replay':True,'degree1_task595_member_equation_zero':True,'member_coefficient_count':len(candidate_body['member_coefficients']),'lower_all_zero':True,'direct_occurrence_replay':False,'next_degree2_residual':None,'grade2_MEMBER':False,'grade2_NONMEMBER':False,'A0':False,'ORDER_54432':False,'full_Q0':False,'COMMON':False,'cofinal_lift':False,'FAKE':False,'IHARA':False,'cross_checked':False,'verified':False}
    manifest_raw=canon(manifest)
    if sum(row['bytes'] for row in receipts.values())+len(manifest_raw)>int(os.environ.get('TASK640_DURABLE_CAP',str(1024**3))): fail('UNKNOWN_RESOURCE:durable')
    (stage/'manifest.json').write_bytes(manifest_raw); os.replace(stage,out); return manifest
def _tiny_joint_fixtures():
    class TinyQ:
        def __init__(self, degree, generators):
            self.identity = tuple(range(degree))
            self.generators = list(generators)

        @staticmethod
        def mul(left, right):
            return tuple(right[left[index]] for index in range(len(left)))

        @classmethod
        def inverse(cls, value):
            answer = [0] * len(value)
            for index, target in enumerate(value):
                answer[target] = index
            return tuple(answer)

        def eval(self, word, images=None):
            marked = self.generators if images is None else images
            value = self.identity
            for letter in word:
                image = marked[abs(letter) - 1]
                if letter < 0:
                    image = self.inverse(image)
                value = self.mul(value, image)
            return value

    class TinyOld:
        @staticmethod
        def embed_f2_pb3(word):
            return [(1 if abs(letter) == 1 else 3) *
                    (1 if letter > 0 else -1) for letter in word]

    def cycle(degree):
        return tuple(list(range(1, degree)) + [0])

    def swap(degree):
        return tuple([1, 0] + list(range(2, degree)))

    e3 = TinyQ(3, [cycle(3)] * 3)
    e4 = TinyQ(4, [cycle(4)] * 6)
    contexts = [(cycle(4), cycle(4)) for _ in range(31)]
    old = TinyOld()
    minimal = EndpointMinimalJointEvaluator(old, e3, e4, contexts)

    class TinyGeneric:
        def __init__(self):
            self.identity = (e3.identity, tuple(e4.identity for _ in contexts))

        def eval(self, word):
            return (e3.eval(old.embed_f2_pb3(word)),
                    tuple(e4.eval(word, context) for context in contexts))

    generic = TinyGeneric()
    conjugate = (1, 1, 2, -1, -2, -1)
    checked = [(), (1, 2, -1, -2), conjugate]
    for word in checked:
        require(minimal.eval(word) == generic.eval(word),
                'fixture lightweight/generic joint equality')
    for index, sign0 in enumerate(SIGNS):
        word = (1 if sign0 > 0 else -1,
                2 if TEN[index] % 2 else -2)
        require(minimal.eval(word) == generic.eval(word),
                'fixture eleven occurrence joint equality')

    e3_mutated = TinyQ(3, [cycle(3), cycle(3), swap(3)])
    mutated_e3 = EndpointMinimalJointEvaluator(old, e3_mutated, e4, contexts)
    require(mutated_e3.eval(conjugate) != minimal.identity,
            'fixture E3 mutation accepted')
    mutated_contexts = list(contexts)
    mutated_contexts[0] = (swap(4), cycle(4))
    mutated_e4 = TinyQ(4, [cycle(4)] * 6)
    mutated_e4_joint = EndpointMinimalJointEvaluator(
        old, e3, mutated_e4, mutated_contexts)
    require(mutated_e4_joint.eval(conjugate) != minimal.identity,
            'fixture E4 context mutation accepted')
    return {'joint_equality_cases': 14, 'joint_mutation_rejections': 2}


def selftest():
    fixture = _tiny_joint_fixtures()
    def mul(a,b): return (a[0]+b[0],a[1]+b[1],a[2]+b[2])
    if mul((1,0,0),(0,1,0))!=(1,1,0) or mul((0,1,0),(1,0,0))!=(1,1,0): fail('fixture_side_order')
    if tuple(-x for x in (1,-2,2))!=(-1,2,-2) or (2*2)%3!=1: fail('fixture_inverse_or_coeff2')
    digest='11'*32; good=LEAF_HEADER.pack(b'R07LEAF1',1,1,0,0,bytes.fromhex(digest),1)+LEAF_RECORD.pack(10,1,2,1)+struct.pack('<b',1)
    if parse_literal_leaves(good,digest)!=[[1,[1],2]]: fail('fixture_leaf_live')
    if raw_seed_gate([[1,[],1],[2,[],1],[2,[],2]])!=[1,2]: fail('fixture_raw_seed_before_cancel')
    class ShiftFixture:
        physical_shifts=((1,2),(3,4))
    first_six_shift_gate(ShiftFixture(),((1,2),(3,4)))
    try: first_six_shift_gate(ShiftFixture(),((1,2),(4,3)))
    except RuntimeError: shift_mutations=1
    else: fail('fixture_first_six_shift_mutation')
    rejected=0
    for bad in (b'X'+good[1:],good[:-1],good+bytes(1),good[:LEAF_HEADER.size]+LEAF_RECORD.pack(11,1,2,1)+struct.pack('<b',1)):
        try: parse_literal_leaves(bad,digest)
        except RuntimeError: rejected+=1
        else: fail('fixture_leaf_mutation')
    class FakeOld:
        def perm_from_row(self,row,width):
            if width != 36: fail('fixture_mark_width')
            return row
    class FakeP176:
        def __init__(self,source_order=59049):
            self.source_order=source_order; self.build_calls=0; self.make_calls=0
        def build_fine_deletion(self,e3,e4,meter):
            self.build_calls+=1
            return {b'fine':b'image'}, {'source_order':self.source_order}
        def canonical_packed_permutation(self,value,width,label):
            if width != 36: fail('fixture_canonical_width')
            return tuple(value)
        def make_deleter(self,old,e3,e4,fine,q0_marked):
            self.make_calls+=1
            if fine != {b'fine':b'image'} or len(q0_marked)!=2:
                fail('fixture_deleter_inputs')
            def delete(value):
                return (b'deleted',value)
            return delete, {'fixture_deleter':True}
    trap={'called':False}
    def fake_build_heavy(*args,**kwargs):
        trap['called']=True
        fail('fixture_build_heavy_called')
    fake_p176=FakeP176()
    fake_runtime={'p176':fake_p176,'old':FakeOld(),'e3':object(),
                  'e4':object(),'meter':object(),
                  'q3':{'coarse_models':{'Q0':
                      {'marked_permutations':[list(range(1,37)),list(range(36,0,-1))]}}},
                  'build_heavy':fake_build_heavy}
    generic_trap = {}
    def generic_builder_trap(name):
        def trapped(*args, **kwargs):
            generic_trap[name] = generic_trap.get(name, 0) + 1
            fail('fixture_generic_builder_called:' + name)
        return trapped
    for name in ('build_light', 'build_roster', 'build_base_rows',
                 'build_pb3_boundary', 'build_pb4_boundary',
                 'producer_exact_target', 'generic_runtime_model'):
        fake_runtime[name] = generic_builder_trap(name)
    install_endpoint_deletion(fake_runtime)
    if not (fake_p176.build_calls==1 and fake_p176.make_calls==1 and
            callable(fake_runtime.get('delete')) and
            fake_runtime['delete'](b'sample')==(b'deleted',b'sample') and
            fake_runtime['deletion_public']['fine']['source_order']==59049):
        fail('fixture_endpoint_installer')
    endpoint_runtime_profile_gate({'e3': object(), 'e4': object()})
    try:
        endpoint_runtime_profile_gate(fake_runtime)
    except RuntimeError:
        forbidden_runtime_rejections = 1
    else:
        fail('fixture_forbidden_runtime_accepted')
    bad_p176=FakeP176(59048)
    bad_runtime=dict(fake_runtime); bad_runtime['p176']=bad_p176
    try: install_endpoint_deletion(bad_runtime)
    except RuntimeError as exc:
        if str(exc)!='endpoint_fine_source_order':
            fail('fixture_wrong_fine_order_reason')
        wrong_fine_order=1
    else: fail('fixture_wrong_fine_order_accept')
    if trap['called'] or generic_trap:
        fail('fixture_generic_builder_trap')
    words_fixture = json.loads((ROOT/'scratchpad/a0_paper_words_v1.json').read_text(encoding='utf-8'))
    require(len(words_fixture['g760']) == 760 and
            sha_obj(list(map(int, words_fixture['g760']))) ==
            RUNTIME_PROFILE['g760_sha256'], 'fixture g760 pin')
    fixture_contexts = [(b'a', b'b')] * 31
    fixture_rows = [{'context_id': i + 1, 'left_hex': '61',
                     'right_hex': '62'} for i in range(31)]
    fixture_named = [{'name': 'fixture_' + str(i),
                      'context_id': (i % 31) + 1} for i in range(46)]
    fixture_public = {
        'context_count': 31, 'contexts': fixture_rows,
        'named_uses': fixture_named, 'named_use_count': 46,
        'named_use_mapping_sha256': sha_obj(fixture_named),
        'context_rows_sha256': sha_obj(fixture_rows),
        'deduplication': 'exact E4 pair equality'}
    validate_context_registry(
        fixture_contexts, {row['name']: row['context_id']
                           for row in fixture_named}, fixture_public,
        lambda value, label: value)
    runtime_profile_gate(RUNTIME_PROFILE)
    fixture_profile = dict(RUNTIME_PROFILE)
    fixture_profile['contexts'] = 30
    try:
        runtime_profile_gate(fixture_profile)
    except RuntimeError:
        profile_mutations = 1
    else:
        fail('fixture runtime profile mutation accepted')
    print(json.dumps({'fixture':'PASS','actor_multiplication':'PASS','inverse_action':'PASS','coefficient_2':'PASS','occurrence_components':11,'endpoint_ceiling':484,'leaf_live_mutations':rejected,'first_six_shift_mutations':shift_mutations,'endpoint_installer':'PASS','endpoint_fine_source_order':59049,'wrong_fine_order_rejected':wrong_fine_order,'build_heavy_trap_called':False,'generic_builders_called':False,'joint_equality_cases':fixture['joint_equality_cases'],'joint_mutation_rejections':fixture['joint_mutation_rejections'],'g760_length':760,'context_order':31,'q0_marked_rows':2,'runtime_profile_mutations':profile_mutations,'forbidden_runtime_rejections':forbidden_runtime_rejections,'seed_cache_bytes':10644832,'rho2_bytes':PACKED},sort_keys=True))
def main():
    global started
    ap=argparse.ArgumentParser(); ap.add_argument('--state',type=Path); ap.add_argument('--candidate',type=Path); ap.add_argument('--task601',type=Path); ap.add_argument('--out',type=Path); ap.add_argument('--selftest',action='store_true'); a=ap.parse_args()
    try:
        if a.selftest: selftest(); return 0
        if not a.state or not a.candidate or not a.task601 or not a.out: fail('usage')
        started=time.monotonic(); authenticate_paper_pins(); auth_state(a.state); _manifest,loaded,roots,rebuilt=auth_parent(a.task601); evaluate(roots,rebuilt,loaded,a.task601,a.candidate,a.out); return 0
    except Exception as exc:
        error=str(exc); status='UNKNOWN_RESOURCE' if error.startswith('UNKNOWN_RESOURCE:') else 'NOT_READY'
        print(json.dumps({'status':status,'error':error},sort_keys=True),file=sys.stderr); return 1
if __name__=='__main__': raise SystemExit(main())
