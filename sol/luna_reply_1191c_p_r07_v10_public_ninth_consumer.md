# Task1191c — P 第9群公開 consumer の静的納品

Noether/root の追加委嘱により、公開 driver の `producer_parent2346_contract_fixture_gate(entry)` 一部品を固定した。数学P最終sourceとTask1191 P返信は変更していない。実行/import/AST/compile/selftest、fixture生成、数学payload再計算、新agent、Git/GHA/network/credential、C private/source/diff/fixture/tableの読取はすべて0。

R = `C:/Users/81905/AppData/Local/Temp/shadow-atelier-audit163`。納品基点は `R/task1191/P/public-ninth-consumer-v1/`。sourceは **14953 B / 274e9d2beac4dfaa703ac3d7319caa6f2c2275408968ec89c82d3c9066a6577c**、全224 LF・top-level3関数。公開第9群契約 **291018 B / 35ba37be737d51feb994680d5111ce8e9adedce65242b7292bf780079b289a3b** を `P_NINTH_SERIALIZER` として参照する。carrierの完全一致と全driverへの組込みはNoether、全文別読・採用と配置はrootが担当する。

F1. Noetherと確定したABIは、entry exact2 `{root: Path, selftest: 全自己検査dict}`、返値は旧gateと同じtuple2 `(observed, case_rows)`。rootは実第9群 `batch-parent-v9`、case_rowsは29件。上位wrapperが旧第8群gateを先に完全受領することを明示依存とした。この部品の第8 child-execution読取だけで旧第8全受領を代行したとは呼ばない。

F2. 成功枝は全92 canonical JSON・7 opaque raw・1 child stderr streamの100 files、37 dirs、登録emptydirを実在庫と比較する。全JSONは型を含むcanonical全bytes、opaqueは全rawを比較してからfile pinを返す。streamに空・ASCIIの余剰条件は設けない。全positive/negative/support、29ケースの順序・変異・目的label・拒否票、scope/ledger/子stdout/子executionの全保存値を公開DSLへ結ぶ。primary positiveとnegativeの全canonical差によるno-op除外、sealed文書のgeneric sealを確認し、native-v9とcurrent-v10のnamespaceを混同しない。登録key family全体の除去もあるため、返値の比較宣言は `whole_saved_positive_and_registered_mutation_compared` とし、「1 scalar fieldだけ」とは宣言しない。

F3. current code_contractの実P10配置名/D3、実parent argvのwhole registry D3、子native0、full argv、env allowlistを保存票へ結ぶ。第8と第9のsource/registry/Python・元parent deadlineは前後とも実値が一致する。親selftest300秒とは別のdeadline・時計観測・再計算を追加していない。child nativeは親が保存した票からの読取であり、独立に子を実行したとの主張ではない。元のchecked_execution/source/registry/parent receipt custodyは既存driverの依存として保持する。

F4. 不足・型/値/keys/raw/seal/在庫/依存不一致は既存例外経路へ伝える。partial/UNKNOWNやmissingを成功値・0計測で埋めない。全fixture/child/source/registryのafter比較後だけ、observedと29件の比較記録を返す。数学判定・旧selftestの実結果は変更しない。

F5. 基点はNoetherが実公開driver **16522905 B / d57d5ece97d18f66a83da4fd7defbf7b476b0cee1d9a9482455a09615cb50984** から抽出した4小片であり、そのdriver全体・archiveは読んでいない。

- 第8 vars/values/gate小片8148 B / 07714b14445f402dc47e3141772bee0d32efd7fb1850479a1e30c395f0e60875。
- 第7有限DSL evaluator5757 B / c3a914981266e6f086e5150ed1016adbdc9bc6d9dbb23fad284ce1097aeb33ca。
- 公開utilities3409 B / a631c63e24f0f3ff04b4cc103ec69ae8a3e27dec733646b4ac23375d23e9fb7b。
- ordinary/JSON patch1858 B / 75199a81c7b93710e5f5d71aae5edfda26e03f0952505eab2dc3b0cdae33c8b5。

第8小片末尾の第4def headerは本文がないため新sourceに含めていない。第8変数束縛と第7finite evaluatorを明示差分で合成し、必要なstream/`$format17g`/`$seal`だけを加えた。既存 `ordinary`、`v8_seventh_patch`、`v7_sixth_read/same/seal`、`scan/pin` 等のABIは保持する。

F6. 全source・基点4小片をEOFまで自己別読した。3部品の全正逆raw partitionと最終連結bytesを照合。公開定義の144 `$file_pin`、16 `$ref` は登録先に閉じ、全100ファイル依存グラフは無循環。5つのmapは元772件上限内であり、定義の展開実行やfixture生成は行っていない。f94320と63a31eのnative0はauthoring/metadata処理だけで、納品fragmentの実行ではない。未解消の自己所見はない。

最終目録 `public-ninth-consumer-final-material-manifest-v1.json` は **2957 B / 1d058c84fd18096ad9128fa8401bf73fbdabbb09ddef037febd78616d1315d81**。全基点fresh前後一致を保存した。全raw差分票は **52532 B / eaebe682715919662d312012382ec00fc1a747a018cc287f2b0ba97aef916dbb**、ABI/scope票は **6227 B / bba0c8e46689ca9a988ec797d12fa9304a7a505208373ffcd9e731de5405547f**、作者別読票は **2952 B / 870354de3a6627289019415ff8d2d39a2cf09ccde8c4c977bc18097c46d73d8a**。全pinをroot/Noetherへ送付済み。rootの追加別読と全組立は別段階であり、本稿を実runtime成功と扱わない。

以下は `v10_p_ninth_fixture_consumer_fragment_v1.py` の全原bytesを収録したもの。

```python
def v10_p_ninth_variables(root,execution):
    contract=P_NINTH_SERIALIZER
    child=read(root/'child-execution.json',True)
    require(type(child) is dict and set(child) == set(contract['public_exact_keys']['child_execution']),
        'P-ninth-child-execution-exact14')
    deadline=child['parent_deadline_monotonic']
    require(type(deadline) in (int,float) and math.isfinite(deadline) and deadline > 0,
        'P-ninth-actual-positive-parent-deadline')
    keys=child['inherited_environment_keys']
    env_contract=contract['runtime_variables']['actual_inherited_environment_keys']
    require(type(keys) is list and all(type(key) is str for key in keys) and keys == sorted(set(keys)) and
        set(env_contract['required']) <= set(keys) <= set(env_contract['required']+env_contract['optional_exact_allowlist']),
        'P-ninth-exact-allowed-inherited-key-names-no-values')
    arguments=execution['argv']
    require(arguments.count('--audit-region-registry') == 1,'P-ninth-single-parent-registry-argument')
    registry_path=Path(arguments[arguments.index('--audit-region-registry')+1]).resolve()
    registry=pin(registry_path,'audit-region-registry.json')
    require(registry['bytes'] == INHERITANCE_REGISTRY_PIN['bytes'] and
        registry['sha256'] == INHERITANCE_REGISTRY_PIN['sha256'],'P-ninth-real-full-current-registry-pin')
    current=code_contract()['producer']
    require(current['file'] == contract['runtime_variables']['actual_source']['file_const'],
        'P-ninth-current-producer-exact-placed-identity')
    source_path=(ROOT/current['file']).resolve()
    require(pin(source_path,current['file']) == current,'P-ninth-actual-final-P-whole-source')
    values={'actual_parent_deadline_monotonic':deadline,'actual_inherited_environment_keys':keys,
        'actual_source':current,'actual_registry':{k:registry[k] for k in ('bytes','sha256')},
        'actual_python_executable':arguments[0],'actual_source_absolute_path':str(source_path),
        'actual_group_absolute_path':str(root.resolve()),'actual_registry_absolute_path':str(registry_path)}
    require(set(values) == set(contract['runtime_variables']),'P-ninth-all-eight-external-variable-bindings')
    for key in ('actual_python_executable','actual_source_absolute_path','actual_group_absolute_path','actual_registry_absolute_path'):
        require(type(values[key]) is str and Path(values[key]).is_absolute(),'P-ninth-absolute-child-identity:'+key)
    return values,child

def v10_p_ninth_values(root,external_variables):
    contract = P_NINTH_SERIALIZER
    require(contract['current_schema'] == SCHEMA,'P-ninth-current-schema-binding')
    definitions,raw_definitions = contract['value_definitions'],contract['raw_byte_definitions']
    streams=contract['raw_stream_definitions']
    require(not (set(definitions) & set(raw_definitions) or set(definitions) & set(streams) or
        set(raw_definitions) & set(streams)),'P-ninth-three-disjoint-file-kinds')
    completed,active = {},set()
    def raw_expected(row):
        if row['format'] == 'ascii':
            value = row['text'].encode('ascii')
        elif row['format'] == 'hex':
            value = bytes.fromhex(row['hex'])
        else:
            require(row['format'] == 'concatenated_hex_runs','P-ninth-finite-raw-format')
            pieces = []
            for part in row['runs']:
                ordinary(part['repeat'],0,12096)
                pieces.append(bytes.fromhex(part['hex']) * part['repeat'])
            value = b''.join(pieces)
        require(len(value) == row['bytes'] and sha(value) == row['sha256'],'P-ninth-public-raw-definition-pin')
        return value
    def checked_file(name):
        safe_name(name)
        require(name in definitions or name in raw_definitions or name in streams,'P-ninth-registered-reference-file')
        if name in completed:
            return copy.deepcopy(completed[name])
        require(name not in active,'P-ninth-no-definition-cycle')
        active.add(name)
        try:
            if name in streams:
                require(name == 'child-stderr.txt','P-ninth-only-original-unconstrained-child-stderr')
                value=(root/name).read_bytes()
            else:
                value = raw_expected(raw_definitions[name]) if name in raw_definitions else expand(definitions[name],external_variables)
            if name in raw_definitions:
                require((root / name).read_bytes() == value,'P-ninth-actual-full-raw:' + name)
            elif name in definitions:
                v7_sixth_read(root,name,value)
            completed[name] = value
            return copy.deepcopy(value)
        finally:
            active.remove(name)
    def expand(node,variables):
        if type(node) is list:
            return [expand(value,variables) for value in node]
        if type(node) is not dict:
            return node
        operations = [key for key in node if key.startswith('$')]
        if not operations:
            return {key:expand(value,variables) for key,value in node.items()}
        require(len(node) == len(operations) == 1,'P-ninth-single-reserved-expression')
        operation = operations[0];item = node[operation]
        sub = lambda value:expand(value,variables)
        if operation == '$ref':
            require(type(item) is str and item in definitions,'P-ninth-exact-definition-reference')
            return checked_file(item)
        if operation == '$file_pin':
            require(type(item) is dict and set(item) == {'path','file'},'P-ninth-file-reference-shape')
            checked_file(item['path'])
            return pin(root / safe_name(item['path']),safe_name(item['file']))
        if operation == '$var':
            require(type(item) is str and item in variables,'P-ninth-bound-variable')
            return copy.deepcopy(variables[item])
        if operation == '$get':
            value = sub(item['value'])
            require(type(value) is dict and item['key'] in value,'P-ninth-existing-object-projection')
            return value[item['key']]
        if operation == '$decimal':
            value = sub(item);ordinary(value,0)
            return str(value)
        if operation == '$hex_lower':
            value,width = sub(item['value']),item['width'];ordinary(value,0);ordinary(width,1,64)
            require(value < 16 ** width,'P-ninth-hex-no-overflow')
            return format(value,'0' + str(width) + 'x')
        if operation in ('$text_concat','$array_concat'):
            values = [sub(value) for value in item]
            wanted = str if operation == '$text_concat' else list
            require(all(type(value) is wanted for value in values),'P-ninth-concatenation-types')
            return ''.join(values) if wanted is str else [child for value in values for child in value]
        if operation == '$sha256_ascii':
            value = sub(item);require(type(value) is str,'P-ninth-ASCII-token-string')
            return sha(value.encode('ascii'))
        if operation == '$if_equal':
            return sub(item['then'] if canonical(sub(item['left'])) == canonical(sub(item['right'])) else item['else'])
        if operation == '$json_patch':
            return v8_seventh_patch(sub(item['base']),item['operations'],sub)
        if operation == '$project_array':
            value = sub(item['value']);require(type(value) is list,'P-ninth-project-array')
            ordinary(item['start'],0,len(value));ordinary(item['stop'],item['start'],len(value))
            return [{key:row[key] for key in item['keys']} for row in value[item['start']:item['stop']]]
        if operation == '$format17g':
            value=sub(item)
            require(type(value) in (int,float) and math.isfinite(value) and value > 0,'P-ninth-real-deadline-format')
            return format(value,'.17g')
        if operation == '$seal':
            require(type(item) is dict and set(item) == {'kind','body'},'P-ninth-public-seal-expression-exact2')
            value=sub(item['body'])
            require(type(value) is dict and not {'schema','sha256'} & set(value) and
                item['kind'] == 'parent2346-contract-selftest','P-ninth-explicit-unsigned-child-result')
            return v7_sixth_seal({'schema':SCHEMA+'.'+item['kind'],**value})
        require(operation == '$map','P-ninth-unsupported-public-expression:' + operation)
        rows = []
        def each(depth,environment):
            if depth == len(item['ranges']):
                for key,value in item['bindings'].items():
                    require(key not in environment,'P-ninth-distinct-bound-name')
                    environment[key] = expand(value,environment)
                rows.append(expand(item['value'],environment))
                require(len(rows) <= 772,'P-ninth-finite-public-array-limit')
                return
            row = item['ranges'][depth]
            ordinary(row['start'],0,772);ordinary(row['stop'],row['start'],772);ordinary(row['step'],1,772)
            require(row['variable'] not in environment,'P-ninth-distinct-range-name')
            for index in range(row['start'],row['stop'],row['step']):
                each(depth+1,{**environment,row['variable']:index})
        each(0,dict(variables))
        return rows
    for name in [*streams,*raw_definitions,*definitions]:
        checked_file(name)
    require(set(completed) == set(contract['exact_file_inventory']['files']),'P-ninth-all100-definition-domain')
    return completed

def producer_parent2346_contract_fixture_gate(entry):
    require(type(entry) is dict and set(entry) == {'root','selftest'},'P-ninth-entry-exact2')
    root,selftest=entry['root'],entry['selftest']
    require(isinstance(root,Path) and root.name == 'batch-parent-v9','P-ninth-registered-group-root')
    require(type(selftest) is dict and type(selftest.get('tests')) is list and len(selftest['tests']) == 9,
        'P-ninth-parent-selftest-nine-groups')
    contract=P_NINTH_SERIALIZER
    v7_sixth_same(selftest['tests'][8],contract['selftest_group_exact_value'],'P-ninth-actual-29-case-result')
    execution=checked_execution('producer-selftest')
    observed=scan(root)
    variables,child=v10_p_ninth_variables(root,execution)
    # The upper wrapper has already accepted the complete original eighth group.
    eighth_root=root.parent/'production-key-contract'
    eighth_variables,eighth_child=v9_p_eighth_variables(eighth_root,execution)
    shared=('actual_parent_deadline_monotonic','actual_source','actual_registry',
        'actual_python_executable','actual_source_absolute_path','actual_registry_absolute_path')
    v7_sixth_same({key:variables[key] for key in shared},{key:eighth_variables[key] for key in shared},
        'P-ninth-and-eighth-same-original-parent-deadline-source-registry')
    values=v10_p_ninth_values(root,variables)
    v7_sixth_same(child,values['child-execution.json'],'P-ninth-whole-child-execution-before-after')
    inventory=contract['exact_file_inventory']
    require(inventory['file_count'] == 100 and inventory['json_file_count'] == 92 and
        inventory['opaque_binary_file_count'] == 7 and inventory['raw_stream_count'] == 1 and
        inventory['directory_count_excluding_group_root'] == 37,'P-ninth-exact-public-finite-cardinalities')
    require(len(contract['value_definitions']) == 92 and len(contract['raw_byte_definitions']) == 7 and
        set(contract['raw_stream_definitions']) == {'child-stderr.txt'},'P-ninth-exact-92JSON-seven-opaque-one-stream')
    v7_sixth_same([row['file'] for row in observed['files']],inventory['files'],'P-ninth-all100-files')
    v7_sixth_same(observed['directories'],inventory['directories'],'P-ninth-all37-directories')
    v7_sixth_same(scan(root/'positive'),values['scope.json']['positive_inventory'],'P-ninth-actual-positive-whole-inventory')
    for name in inventory['required_empty_directories']:
        directory=root/safe_name(name)
        require(directory.is_dir() and not directory.is_symlink() and not any(directory.iterdir()),
            'P-ninth-registered-actual-empty-directory:'+name)
    ledger=values['case-ledger.json']['cases']
    cases=contract['case_order_and_exact_mutations']
    require(type(ledger) is list and type(cases) is list and len(ledger) == len(cases) == 29,
        'P-ninth-all29-saved-ledger-cases')
    for ordinal,(row,spec) in enumerate(zip(ledger,cases,strict=True)):
        ordinary(spec['ordinal'],ordinal,ordinal)
        v7_sixth_same(row['name'],spec['name'],'P-ninth-case-order')
        v7_sixth_same(row['expected_gate'],spec['expected_gate'],'P-ninth-case-purpose')
        v7_sixth_same(row['observed_error'],spec['expected_observed_error_if_rejected'],'P-ninth-exact-normal-refusal-label')
        positive=values['positive/'+spec['positive_files'][0]]
        negative=values[spec['name']+'/input.json']
        require(canonical(positive) != canonical(negative),'P-ninth-actual-primary-mutation-not-noop:'+spec['name'])
        # Generic seal only: native-v9 and current-v10 namespaces remain distinct.
        for value in (positive,negative):
            if type(value) is dict and {'schema','sha256'} <= set(value):
                v7_sixth_same(value,v7_sixth_seal({key:item for key,item in value.items() if key != 'sha256'}),
                    'P-ninth-actual-generic-seal-before-key-or-namespace-boundary:'+spec['name'])
    variables_after,child_after=v10_p_ninth_variables(root,checked_execution('producer-selftest'))
    v7_sixth_same(variables_after,variables,'P-ninth-current-source-registry-and-child-identity-after-pin')
    v7_sixth_same(child_after,child,'P-ninth-child-metadata-after-pin')
    eighth_variables_after,eighth_child_after=v9_p_eighth_variables(eighth_root,checked_execution('producer-selftest'))
    v7_sixth_same(eighth_variables_after,eighth_variables,'P-ninth-eighth-source-registry-deadline-after-pin')
    v7_sixth_same(eighth_child_after,eighth_child,'P-ninth-eighth-child-execution-after-pin')
    v7_sixth_same(scan(root),observed,'P-ninth-full-fixture-before-after')
    child_pin=pin(root/'child-execution.json','child-execution.json')
    eighth_pin=pin(eighth_root/'child-execution.json','production-key-contract/child-execution.json')
    parent_pin=pin(REPORT/'execution/producer-selftest-result.json','execution/producer-selftest-result.json')
    return observed,[{'case':row['name'],'positive':row['positive'],'negative':row['negative'],'rejection':row['rejection'],
        'observed_error':row['observed_error'],'intended_label_reached':True,
        'whole_saved_positive_and_registered_mutation_compared':True,'ordinary_helper_reexecuted':False,
        'child_execution':child_pin,'eighth_child_execution':eighth_pin,
        'same_original_parent_deadline_as_eighth':True,
        'child_native_exit_code_read_from_parent_saved_receipt':child['native_exit_code'],
        'actual_parent_selftest_execution':parent_pin,'child_observation_independently_reexecuted':False} for row in ledger]

```

AUDIT_1191C_P_VERDICT: PUBLIC_P_NINTH_CONSUMER_STATIC_COMPLETE; TARGET_EXECUTION_0; ROOT_ASSEMBLY_ADOPTION_AND_RUNTIME_SEPARATE
