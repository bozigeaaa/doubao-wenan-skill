import json
import re
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[1]
SKILLS_ROOT = PROJECT_ROOT / ".agents" / "skills"
REFERENCES = SKILLS_ROOT / "references"
AGENTS = PROJECT_ROOT / "AGENTS.md"
WENAN = SKILLS_ROOT / "wenan-skill" / "SKILL.md"
HUMANIZER = SKILLS_ROOT / "humanizer" / "SKILL.md"
REGISTRY = REFERENCES / "generation-trigger-registry.md"
QUALITY_GATE = REFERENCES / "b2b-content-quality-gate.md"
PLACEMENT = REFERENCES / "company-soft-placement.md"
COMPLIANCE = REFERENCES / "compliance-wordlist.md"
COMPANY_CLAIM_LEDGER = REFERENCES / "company-claim-evidence-ledger.md"
COMPANY_CLAIM_LEDGER_JSON = PROJECT_ROOT / "content-state" / "company-claim-evidence-ledger.json"
MANIFEST = REFERENCES / "generation-manifest.json"
TEST_RUNNER = PROJECT_ROOT / "tests" / "run_rule_tests.py"
TOPIC_CONVERSION = REFERENCES / "b2b-topic-conversion-loop.md"
NEGATIVE_EXAMPLES = REFERENCES / "negative-examples.md"
HOOK_LIBRARY = REFERENCES / "hook-pattern-library.md"
IMPACT_FILTER = (
    SKILLS_ROOT
    / "global-hotspot-industry-impact-script"
    / "references"
    / "impact-filter.md"
)
LOCAL_DELIVERY_PROOF = REFERENCES / "local-manufacturing-delivery-proof.md"
FIRE_FACT_CHECK = (
    SKILLS_ROOT / "saudi-camp-fire-script" / "references" / "fact-check-rules.md"
)
LIGHT_FACT_CHECK = (
    SKILLS_ROOT / "saudi-light-steel-script" / "references" / "fact-check-rules.md"
)
PROFESSIONAL_FACT_RULES = (
    SKILLS_ROOT / "saudi-professional-knowledge-script" / "references" / "fact-rules.md"
)
BRAND_FACT_RULES = (
    SKILLS_ROOT / "saudi-brand-proof-script" / "references" / "fact-rules.md"
)
SANITARY_FACT_CHECK = (
    SKILLS_ROOT / "saudi-sanitary-unit-script" / "references" / "fact-check-rules.md"
)

GENERATING_SKILLS = (
    "global-hotspot-industry-impact-script",
    "saudi-brand-proof-script",
    "saudi-breakout-story-script",
    "saudi-camp-fire-script",
    "saudi-light-steel-script",
    "saudi-product-seeding-script",
    "saudi-professional-knowledge-script",
    "saudi-sanitary-unit-script",
)

PATTERN_FILES = (
    "global-hotspot-industry-impact-script/references/script-pattern.md",
    "saudi-brand-proof-script/references/proof-pattern.md",
    "saudi-breakout-story-script/references/story-pattern.md",
    "saudi-camp-fire-script/references/script-pattern.md",
    "saudi-light-steel-script/references/script-pattern.md",
    "saudi-product-seeding-script/references/seeding-pattern.md",
    "saudi-professional-knowledge-script/references/script-pattern.md",
    "saudi-sanitary-unit-script/references/script-pattern.md",
)

GENERATING_INTERFACES = tuple(
    SKILLS_ROOT / name / "agents" / "openai.yaml" for name in GENERATING_SKILLS
)


def read(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def directly_referenced_generation_rules() -> tuple[Path, ...]:
    referenced: list[Path] = []
    active_reference = re.compile(
        r"`(?P<path>(?:\.agents/skills/references/|references/|content-state/)"
        r"[^`]+\.(?:md|json))`"
    )

    skill_files = (
        WENAN,
        *(SKILLS_ROOT / skill_name / "SKILL.md" for skill_name in GENERATING_SKILLS),
    )
    for skill_file in skill_files:
        skill_dir = skill_file.parent
        for match in active_reference.finditer(read(skill_file)):
            raw_path = match.group("path")
            path = (
                PROJECT_ROOT / raw_path
                if raw_path.startswith((".agents/", "content-state/"))
                else skill_dir / raw_path
            )
            assert path.exists(), f"Active rule reference does not exist: {path}"
            referenced.append(path)

    return tuple(dict.fromkeys(referenced))


def manifest_declared_rules() -> tuple[Path, ...]:
    manifest = json.loads(read(MANIFEST))
    paths = tuple(
        PROJECT_ROOT / manifest[field]
        for field in ("trigger_registry", "quality_gate", "compliance_review")
    )
    for path in paths:
        assert path.exists(), f"Manifest-declared rule does not exist: {path}"
    return paths


def active_generation_paths() -> tuple[Path, ...]:
    paths = (
        AGENTS,
        WENAN,
        REGISTRY,
        QUALITY_GATE,
        REFERENCES / "expression-craft.md",
        PLACEMENT,
        TOPIC_CONVERSION,
        NEGATIVE_EXAMPLES,
        HOOK_LIBRARY,
        HUMANIZER,
        *(SKILLS_ROOT / name / "SKILL.md" for name in GENERATING_SKILLS),
        *(SKILLS_ROOT / relative for relative in PATTERN_FILES),
        *GENERATING_INTERFACES,
        *directly_referenced_generation_rules(),
        *manifest_declared_rules(),
    )
    return tuple(dict.fromkeys(paths))


def test_critical_specialist_rule_references_remain_in_the_active_closure() -> None:
    required_edges = {
        "global-hotspot-industry-impact-script": (
            "references/impact-filter.md",
            ".agents/skills/references/local-manufacturing-delivery-proof.md",
        ),
        "saudi-brand-proof-script": (
            "references/fact-rules.md",
            "content-state/company-claim-evidence-ledger.json",
        ),
        "saudi-breakout-story-script": ("references/fact-boundaries.md",),
        "saudi-camp-fire-script": ("references/fact-check-rules.md",),
        "saudi-light-steel-script": ("references/fact-check-rules.md",),
        "saudi-product-seeding-script": ("references/fact-rules.md",),
        "saudi-professional-knowledge-script": ("references/fact-rules.md",),
        "saudi-sanitary-unit-script": ("references/fact-check-rules.md",),
    }
    active_paths = set(active_generation_paths())

    for skill_name, references in required_edges.items():
        skill_dir = SKILLS_ROOT / skill_name
        skill = read(skill_dir / "SKILL.md")
        for raw_path in references:
            assert raw_path in skill, f"Missing active rule edge: {skill_name} -> {raw_path}"
            resolved = (
                PROJECT_ROOT / raw_path
                if raw_path.startswith((".agents/", "content-state/"))
                else skill_dir / raw_path
            )
            assert resolved in active_paths, f"Rule not scanned as active: {resolved}"

    assert COMPLIANCE in active_paths
    for field in ("trigger_registry", "quality_gate", "compliance_review"):
        assert PROJECT_ROOT / json.loads(read(MANIFEST))[field] in active_paths


def test_semantic_promise_contract_locks_the_title_decision_without_locking_prose_shape() -> None:
    registry = read(REGISTRY)
    for expected in (
        "对象与场景",
        "判断动作或变量",
        "本稿必须给出的答案",
        "答案的证据强度与适用边界",
        "相邻但不能替代本题的问题",
        "锁定的是语义靶心，不是正文顺序",
        "口语表达、问句上限、开头和动作结尾必须执行",
    ):
        assert expected in registry

    for path in (WENAN, QUALITY_GATE):
        assert "语义承诺" in read(path), path


def test_semantic_promise_machine_wiring_records_the_pressure_scenarios_for_task_four() -> None:
    registry = read(REGISTRY)
    # Python only verifies the wiring and documented rejection boundary. Task 4's
    # fresh-context pressure scenarios verify real semantic reject/accept behavior.
    for expected in (
        "仅共享项目名、产品名、行业或关键词，不构成相关性",
        "不能靠末尾补一句采购建议通过",
        "判断变量不同即失败",
    ):
        assert expected in registry


def test_active_generation_rules_remove_hard_templates_and_the_two_deleted_rule_families() -> None:
    active = {path: read(path) for path in active_generation_paths()}
    combined = "\n".join(active.values())

    for deprecated in (
        "Use short spoken sentences.",
        "Decide the intended ending before drafting.",
        "每段只承担一个可说清的推进动作",
        "给每段内部标一个动作",
        "每一段必须提供新的、已核实且必要的信息",
        "每一段必须提供某类新信息",
        "新段必须回答上段留下的问题、推进同一机制、改变条件或带来新证据",
        "独立段必须完成一个新的信息动作",
        "检查该段是否完成新的信息动作",
        "预告不得与本稿的条件式结论冲突",
        "预告不得否定本稿已经说明的条件结论",
        "Good next-video hook",
    ):
        assert deprecated not in combined, deprecated

    finished_frame = re.compile(r"(?mi)^\s*[-*]\s+Prefer\s+[\"“]")
    for path, content in active.items():
        assert not finished_frame.search(content), path

    generated_ending_menu = re.compile(
        r"(?mi)^\s*(?:[-*]|\d+\.)\s*.*\bEnd with\s+(?:the|a|an|your|buyer|one)\b"
    )
    for relative in PATTERN_FILES:
        assert not generated_ending_menu.search(read(SKILLS_ROOT / relative)), relative

    generation_directives = "\n".join(
        read(path)
        for path in (
            WENAN,
            REGISTRY,
            *(SKILLS_ROOT / name / "SKILL.md" for name in GENERATING_SKILLS),
            *(SKILLS_ROOT / relative for relative in PATTERN_FILES),
        )
    )
    forced_questionization = re.compile(
        r"(?i)(?:rewrite\s+broad\s+topics\s+into\s+one\s+precise\s+question|"
        r"convert\s+the\s+user's\s+topic\s+into\s+one\s+mechanism-level\s+question)"
    )
    complete_question_example = re.compile(
        r"(?m)^\s*[-*]\s+[\"“](?:Who|What|When|Where|Why|How|Which|Should|Can|"
        r"谁|什么|何时|哪里|为什么|如何|怎么|哪一个|是否).*[?？][\"”]\s*$"
    )
    default_pressure_subject = re.compile(
        r"(?im)^\s*(?!.*(?:不默认|不得)).*(?:Default pressure subjects|(?:默认|优先).{0,24}"
        r"(?:采购|项目经理|营地管理).{0,24}(?:压力|焦虑|担心))"
    )
    maximum_progress_verbs = re.compile(
        r"最多\s*(?:三|3)\s*个?(?:(?:推进动词)|(?:动词.{0,24}推进))"
    )
    assert not forced_questionization.search(generation_directives)
    assert not complete_question_example.search(generation_directives)
    assert not maximum_progress_verbs.search(generation_directives)
    assert not default_pressure_subject.search(generation_directives)


def test_topic_conversion_loop_does_not_prescribe_titles_endings_or_a_three_part_news_script() -> None:
    topic_loop = read(TOPIC_CONVERSION)

    assert not re.search(r"先确定\s*`?account_type`?\s*，?再定标题和结尾", topic_loop)
    assert not re.search(r"\|\s*账号类型\s*\|.*\|\s*结尾\s*\|", topic_loop)
    assert not re.search(
        r"可采用但不强制采用的表达结构：`[^`]*→[^`]*→[^`]*`", topic_loop
    )
    assert not re.search(r"structure_signature.*推进动作.*结尾任务", topic_loop, flags=re.DOTALL)


def test_agents_top_level_does_not_offer_a_fixed_functional_ending_menu() -> None:
    agents_generation_rules = read(AGENTS).split("## 知识库定位", maxsplit=1)[0]
    functional_ending_menu = re.compile(
        r"结尾.*(?:给决策规则.*给一个核对动作.*指出适用边界.*回扣开头后果.*"
        r"留一个需要判断的问题.*承接下一条)",
        flags=re.DOTALL,
    )
    assert not functional_ending_menu.search(agents_generation_rules)
    assert "以一个明确动作收尾" in agents_generation_rules
    assert "用户明确要求无 CTA 时直接结束" in agents_generation_rules


def test_generation_guides_use_content_promise_not_a_locked_or_supported_unique_core_question() -> None:
    generated_core_question = re.compile(
        r"(?:锁定|支撑).{0,40}(?:唯一核心问题|核心问题)", flags=re.DOTALL
    )
    for path in (QUALITY_GATE, HOOK_LIBRARY):
        content = read(path)
        assert not generated_core_question.search(content), path
        assert "内容承诺" in content, path


def test_default_oral_length_is_pre_draft_and_detailed_placement_is_conditional() -> None:
    registry = read(REGISTRY)
    manifest = json.loads(read(MANIFEST))

    assert manifest["stages"] == [
        "route_task",
        "verify_evidence",
        "lock_semantic_promise",
        "check_promise_answerability",
        "check_audience_value",
        "draft",
        "design_hook",
        "dispatch_placement_check_if_triggered",
        "oralization_review",
        "check_content_coverage",
        "recheck_oralization_if_content_changed",
        "deduplicate_structure",
        "recheck_oralization_if_dedup_changed",
        "validate_promise_fulfillment",
        "check_one_sentence_takeaway",
        "check_news_landing_point",
        "recheck_facts",
        "run_b2b_quality_gate",
        "run_compliance_review",
        "deliver",
    ]
    assert manifest["quality_gate"] == ".agents/skills/references/b2b-content-quality-gate.md"
    assert manifest["compliance_review"] == ".agents/skills/references/compliance-wordlist.md"

    length_policy = manifest["length_policy"]
    assert length_policy["explicit_user_target"]["phase"] == "pre_draft"
    assert length_policy["reference_corpus_default"]["phase"] == "pre_draft"
    assert "check_placement_eligibility" not in manifest["stages"]

    dispatch_stage = "dispatch_placement_check_if_triggered"
    assert dispatch_stage in manifest["stages"]
    assert manifest["stages"].index("design_hook") < manifest["stages"].index(dispatch_stage)
    assert manifest["stages"].index(dispatch_stage) < manifest["stages"].index("oralization_review")

    placement_branch = manifest["conditional_branches"]["placement_eligibility"]
    assert placement_branch["stage"] == "check_placement_eligibility"
    assert placement_branch["dispatch_stage"] == dispatch_stage
    assert placement_branch["after_stage"] == "design_hook"
    assert placement_branch["before_stage"] == "oralization_review"
    assert placement_branch["entry_conditions"] == [
        "user_requested_company_or_product",
        "product_is_topic",
        "news_selected_product",
    ]
    assert placement_branch["canonical_entry_conditions"] == [
        "explicit_company_or_product_request",
        "product_topic",
        "selected_product_news",
    ]
    for content in (registry, read(WENAN)):
        assert "placement_eligibility" in content


def test_reverse_answer_check_cannot_be_reduced_to_a_stage_name() -> None:
    registry = read(REGISTRY)
    section_match = re.search(
        r"## 反向答案检查\s*(?P<section>.*?)(?=\n## |\Z)",
        registry,
        flags=re.DOTALL,
    )
    assert section_match, "Missing reverse-answer behavior section"
    section = section_match.group("section")

    for expected in (
        "先不看标题",
        "对象与场景",
        "判断动作或变量",
        "实际答案",
        "结论强度和适用边界",
        "产品、公司或最后一句都不能替代正文的直接答案",
        "改写、补写、删减或重排后必须重新执行这道检查",
    ):
        assert expected in section


def test_action_ending_is_default_with_explicit_no_cta_exception() -> None:
    registry = read(REGISTRY)
    agents = read(AGENTS)

    for content in (registry, agents):
        assert "直接结束" in content or "自然结束" in content
        assert "用户明确" in content
        assert "CTA" in content

    assert "加一个与本题相关的动作结尾" in registry
    assert "用户明确要求无 CTA 时例外" in registry
    assert "不新增无依据的服务或效果承诺" in registry


def test_runtime_receipt_is_hidden_unless_requested_or_the_flow_is_blocked() -> None:
    manifest = json.loads(read(MANIFEST))

    assert manifest["receipt_mode"] == {
        "default": "hidden",
        "show_when": ["user_requested", "workflow_exception"],
        "expose_internal_reasoning": False,
    }
    for content in (read(AGENTS), read(WENAN), read(REGISTRY), read(QUALITY_GATE)):
        assert "前 6 条" not in content
        assert "前 6 条已确认或已发布稿" not in content
    assert "只有用户要求展开" in read(AGENTS)
    assert "运行回执默认隐藏，只在用户要求或流程异常时" in read(WENAN)
    assert "运行回执默认隐藏，仅在用户要求或流程异常时" in read(REGISTRY)
    assert "用户明确要求" in read(QUALITY_GATE)


def test_humanizer_enforces_shared_oral_style_without_changing_facts() -> None:
    humanizer = read(HUMANIZER)
    for expected in (
        "expression-craft.md",
        "理解、朗读、重复表达和语气",
        "不达口语标准",
        "不能只换几个同义词交差",
        "事实命题、限定条件、因果强度和责任关系",
    ):
        assert expected in humanizer


def test_natural_transitions_and_local_auxiliary_relations_do_not_become_new_templates() -> None:
    humanizer = read(HUMANIZER)
    registry = read(REGISTRY)
    agents = read(AGENTS)

    for expected in (
        "不承载新事实不等于“无信息过渡”",
        "能防止朗读跳跃的功能性过渡",
        "expression-craft.md",
    ):
        assert expected in humanizer

    for content in (registry, agents):
        assert "一个主导" in content
        assert "其他关系辅助" in content
        assert "不得另起一个判断变量" in content or "不得引入另一个判断变量" in content


def test_news_impact_and_local_delivery_rules_do_not_supply_finished_takeaway_or_qa_frames() -> None:
    impact_filter = read(IMPACT_FILTER)
    local_delivery = read(LOCAL_DELIVERY_PROOF)

    for content, label in (
        (impact_filter, "impact filter"),
        (local_delivery, "local delivery proof"),
    ):
        assert "语义承诺" in content, label
        assert "证据关系" in content, label
        assert "不规定问题形式、清单或段落" in content, label

    for deprecated in (
        "Default takeaway should answer",
        "What should someone doing Saudi projects recheck because of this?",
        "优先把问题写成",
        "本地交付链是否能接住",
        "供应商是否具备真实本地交付能力",
        "## 安全表达示例",
        "应改为：不同本地供应模式",
    ):
        assert deprecated not in impact_filter + local_delivery, deprecated

    assert not re.search(r'(?m)^\s*[-*]\s*[“"].+[”"]\s*$', local_delivery)


def test_fire_fact_check_stays_internal_and_returns_one_script_by_default() -> None:
    fire_rules = read(FIRE_FACT_CHECK)

    assert "Before returning a final script, list:" not in fire_rules
    assert "默认只交付一份成稿" in fire_rules
    assert "内部" in fire_rules
    assert "证据" in fire_rules
    assert "边界" in fire_rules


def test_content_type_routes_do_not_prescribe_three_part_seeding_or_forced_brand_scenes() -> None:
    agents = read(AGENTS)

    assert "讲清不选的代价、产品如何降低风险、为什么现在值得认真考虑" not in agents
    assert "必须用场景和逻辑自证" not in agents
    assert "不规定顺序或必备要素" in agents
    assert "场景只有在有证据且与本期内容承诺直接相关时才可使用" in agents


def test_generation_interfaces_do_not_restore_deleted_content_recipes() -> None:
    interfaces = {
        path.parent.parent.name: read(path) for path in GENERATING_INTERFACES
    }

    for deprecated in (
        "讲清不选的代价和产品降低风险的机制",
        "重点讲清不选的代价和为什么值得认真考虑",
        "用场景和交付逻辑自证",
        "仅在通过同链植入资格检查时带出公司或产品",
    ):
        assert all(deprecated not in content for content in interfaces.values()), deprecated

    assert "由内容承诺、证据和受众决策任务决定讲法" in interfaces[
        "saudi-product-seeding-script"
    ]
    assert "不预设场景或交付结构" in interfaces["saudi-brand-proof-script"]


def test_professional_fact_rules_only_dispatch_placement_on_the_three_shared_triggers() -> None:
    fact_rules = read(PROFESSIONAL_FACT_RULES)

    for trigger in (
        "用户明确要求公司或产品",
        "产品本身是主题",
        "新闻流程已选定产品",
    ):
        assert trigger in fact_rules

    assert "Explain the rule first." not in fact_rules
    assert "三项均未触发时，不检查也不写入公司或产品" in fact_rules
    assert "不设“先讲规则、再讲产品”等固定顺序" in fact_rules
    assert "采用固定顺序" not in fact_rules


def test_brand_fact_rules_omit_unconfirmed_realtime_variables_instead_of_disclaiming_them() -> None:
    fact_rules = read(BRAND_FACT_RULES)

    assert "没有当期确认资料时不写" in fact_rules
    assert "subject to current project confirmation" not in fact_rules
    assert "具体库存和交付周期，要以项目当期配置和排产为准。" not in fact_rules


def test_company_claim_ledger_does_not_offer_disclaimers_as_approved_copy() -> None:
    ledger = json.loads(read(COMPANY_CLAIM_LEDGER_JSON))
    approved_copy = "\n".join(
        claim.get("approved_public_wording") or "" for claim in ledger["claims"]
    )

    for deprecated in (
        "以当期项目确认结果为准",
        "应以最新组织与项目安排复核",
        "项目方可核对",
        "可进一步核对",
        "资料基础",
    ):
        assert deprecated not in approved_copy, deprecated

    for claim in ledger["claims"]:
        if claim["classification"] == "project_variable":
            assert claim["requires_project_confirmation"] is True, claim["claim_id"]
            assert not claim.get("approved_public_wording"), claim["claim_id"]
            assert claim.get("publication_rule") == (
                "取得当期确认后，才可按确认内容形成公开表述；未确认时不进入成稿。"
            )
        if claim["requires_project_confirmation"]:
            assert not claim.get("approved_public_wording"), claim["claim_id"]
            assert claim.get("publication_rule") == (
                "取得当期确认后，才可按确认内容形成公开表述；未确认时不进入成稿。"
            )


def test_sanitary_fact_check_does_not_supply_a_generic_compliance_sentence() -> None:
    fact_rules = read(SANITARY_FACT_CHECK)

    assert "Prefer safe phrasing:" not in fact_rules
    assert "项目需要按当地营地管理、劳工住宿和甲方检查要求配置卫生设施" not in fact_rules
    assert "无法核实" in fact_rules
    assert "不写" in fact_rules


def test_active_fact_rules_do_not_supply_finished_safe_copy_examples() -> None:
    safe_copy_heading = re.compile(
        r"(?mi)^##\s+Safe\s+(?:Framing|Claim Patterns|Proof Language|Phrasing)\s*$"
    )

    for path in active_generation_paths():
        content = read(path)
        assert not safe_copy_heading.search(content), path
        assert "Prefer safe phrasing:" not in content, path


def test_custom_test_runner_fails_closed_when_tests_are_missing() -> None:
    runner = read(TEST_RUNNER)

    for expected in (
        "REQUIRED_TEST_FILES",
        "missing_files",
        "No test functions discovered",
        "has no test functions",
    ):
        assert expected in runner


def test_compliance_review_cannot_replace_missing_evidence_with_safe_copy() -> None:
    compliance = read(COMPLIANCE)
    agents = read(AGENTS)

    for deprecated in (
        "可替代表达",
        "以项目确认结果为准",
        "来源撑不住，必须弱化或改口径",
        "否则写\"建议/通常/按项目确认\"",
        "没有依据就降级或删除",
        "降级为安全的专业表述",
        "只能写“面向长期使用”“降低后期维护压力”等安全表达",
        "在最终表达调整和事实复检后",
    ):
        assert deprecated not in compliance + agents, deprecated

    for expected in (
        "没有证据就删除或停止",
        "来源本身直接支持更窄或更弱的命题",
        "不能用条件词、免责句或弱化词修复缺失证据",
    ):
        assert expected in compliance


def test_pending_or_expired_claims_stay_out_of_the_finished_script() -> None:
    fire_skill = read(SKILLS_ROOT / "saudi-camp-fire-script" / "SKILL.md")
    light_steel_skill = read(SKILLS_ROOT / "saudi-light-steel-script" / "SKILL.md")
    combined = "\n".join(
        (
            read(AGENTS),
            read(WENAN),
            read(COMPANY_CLAIM_LEDGER),
            read(FIRE_FACT_CHECK),
            read(LIGHT_FACT_CHECK),
            fire_skill,
            light_steel_skill,
        )
    )

    for deprecated in (
        "能安全删除或降级的内容",
        "资料过期或无法复核时，降级为不带数值的能力表述",
        'keep it only as draft copy and flag it in "待核实高风险事实"',
        "其他面积口径如有冲突，标注待核实",
        "mark it as a fact slot that needs confirmation",
        "rewrite them as safer requirement directions or mark them for confirmation",
        "Use a safer professional explanation or mark it internally as a confirmation slot",
        "use safer long-term-use language if unresolved",
    ):
        assert deprecated not in combined, deprecated

    assert "过期数字不直接复用" in read(COMPANY_CLAIM_LEDGER)
    assert "普通业务介绍不因历史条目过期而一并阻断" in read(COMPANY_CLAIM_LEDGER)
    assert "不进入成稿" in read(AGENTS)
    assert "omit it from the script, obtain supporting evidence, narrow the content promise, or stop" in fire_skill
    assert "omit it from the script, obtain supporting evidence, narrow the content promise, or stop" in light_steel_skill


def test_one_sentence_takeaway_gate_is_wired_into_the_machine_workflow() -> None:
    manifest = json.loads(read(MANIFEST))
    registry = read(REGISTRY)
    router = read(WENAN)

    assert "viewer_one_sentence_takeaway" in manifest["temporary_state_required_fields"]
    assert "check_one_sentence_takeaway" in manifest["stages"]
    assert "check_news_landing_point" in manifest["stages"]
    assert manifest["stages"].index("check_one_sentence_takeaway") > manifest["stages"].index(
        "validate_promise_fulfillment"
    )
    assert manifest["stages"].index("check_news_landing_point") < manifest["stages"].index(
        "recheck_facts"
    )

    for expected in (
        "一句话总结门",
        "新闻落点检查",
        "观众一句话总结",
        "转播新闻",
        "以本篇目标受众身份",
        "明确对象或场景",
    ):
        assert expected in registry, expected

    assert "一句话总结检查" in router
    assert "新闻落点检查" in router
    assert "观众一句话总结" in router


def test_completeness_and_directness_rules_guard_against_thin_winding_vague_copy() -> None:
    registry = read(REGISTRY)
    gate = read(QUALITY_GATE)
    negative = read(NEGATIVE_EXAMPLES)

    for expected in (
        "讲清楚",
        "适用条件、比较口径",
        "内容过少而不是简洁",
        "简单不等于内容少",
    ):
        assert expected in registry or expected in gate, expected

    for symptom in ("转播新闻", "只讲结论不讲条件", "一句话说不清核心", "绕：铺垫过长与条件套条件"):
        assert symptom in negative, symptom
