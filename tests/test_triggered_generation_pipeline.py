import json
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[1]
SKILLS_ROOT = PROJECT_ROOT / ".agents" / "skills"
REFERENCES = SKILLS_ROOT / "references"
AGENTS = PROJECT_ROOT / "AGENTS.md"
WENAN = SKILLS_ROOT / "wenan-skill" / "SKILL.md"
HUMANIZER = SKILLS_ROOT / "humanizer" / "SKILL.md"
TRIGGER_REGISTRY = REFERENCES / "generation-trigger-registry.md"
MANIFEST = REFERENCES / "generation-manifest.json"
STRUCTURE_LEDGER = PROJECT_ROOT / "content-state" / "script-structure-ledger.json"

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


def read(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def test_machine_manifest_declares_the_complete_stage_order() -> None:
    manifest = json.loads(read(MANIFEST))
    assert manifest["orchestrator"] == "wenan-skill"
    stages = manifest["stages"]
    for required in (
        "lock_semantic_promise",
        "check_promise_answerability",
        "validate_promise_fulfillment",
    ):
        assert required in stages

    assert stages == [
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

    for required in (
        "object_and_context",
        "decision_dimension",
        "required_answer",
        "answer_boundary",
        "adjacent_non_substitutes",
    ):
        assert required in manifest["temporary_state_required_fields"]
    assert "viewer_one_sentence_takeaway" in manifest["temporary_state_required_fields"]
    assert "check_one_sentence_takeaway" in stages
    assert "check_news_landing_point" in stages
    assert stages.index("check_one_sentence_takeaway") > stages.index("validate_promise_fulfillment")
    assert stages.index("check_one_sentence_takeaway") < stages.index("recheck_facts")

    assert manifest["visible_title_handoff"] is False
    assert manifest["persistent_state_write"] == "confirmed_or_published_only"
    ledger = json.loads(read(STRUCTURE_LEDGER))
    assert ledger["workflow_version"] == manifest["workflow_version"]


def test_default_oral_length_is_applied_without_dropping_evidence() -> None:
    manifest = json.loads(read(MANIFEST))
    assert "length_mode_and_target" not in manifest["temporary_state_required_fields"]

    stages = manifest["stages"]
    assert "set_length_mode" not in stages
    assert "check_placement_eligibility" not in stages
    assert stages.index("draft") < stages.index("check_content_coverage")
    assert stages.index("oralization_review") < stages.index("check_content_coverage")
    assert stages.index("check_content_coverage") < stages.index("validate_promise_fulfillment")

    length_policy = manifest["length_policy"]
    assert length_policy["explicit_user_target"]["phase"] == "pre_draft"
    assert length_policy["reference_corpus_default"]["phase"] == "pre_draft"

    registry = read(TRIGGER_REGISTRY)
    for required in (
        "篇幅校准与内容覆盖门",
        "以约 500 字作为完整口播稿的弹性篇幅参考",
        "正文不含标题、标签和资料出处",
        "较短但已经讲清楚的稿件可以直接交付",
        "不删掉必要条件",
        "不得用相邻知识、虚构案例或重复结论凑字数",
    ):
        assert required in registry

    router = read(WENAN)
    assert "目标时长/篇幅（可选）" in router
    assert "用户指定" in router

    active = "\n".join(
        read(path)
        for path in (
            AGENTS,
            WENAN,
            TRIGGER_REGISTRY,
            REFERENCES / "b2b-content-quality-gate.md",
        )
    )
    assert "260–400" not in active


def test_all_complete_script_entries_build_the_same_temporary_state() -> None:
    manifest = json.loads(read(MANIFEST))
    router = read(WENAN)
    assert "同一任务内临时内容状态" in router
    assert "直接要求完整文案" in router
    assert "标题方向确认" in router
    assert "都必须先建立同一份临时内容状态" in router
    assert "标题交接单" not in router

    for path in (
        AGENTS,
        REFERENCES / "b2b-content-quality-gate.md",
        REFERENCES / "b2b-topic-conversion-loop.md",
    ):
        assert "生成标题交接单" not in read(path), path

    for required in (
        "内容承诺",
        "受众任务",
        "可证结论",
        "主张—来源—表达强度",
        "适用边界",
        "植入资格",
        "待解决项",
    ):
        assert required in router

    assert "generation-manifest.json" in router
    assert "generation-trigger-registry.md" in router
    assert manifest["stages"].index("lock_semantic_promise") < manifest["stages"].index(
        "check_promise_answerability"
    )
    assert manifest["stages"].index("check_promise_answerability") < manifest["stages"].index("draft")
    assert manifest["stages"].index("validate_promise_fulfillment") < manifest["stages"].index(
        "recheck_facts"
    )


def test_trigger_registry_is_the_only_shared_execution_authority() -> None:
    registry = read(TRIGGER_REGISTRY)
    for heading in (
        "事实与来源门",
        "结构路由门",
        "钩子触发",
        "衔接触发",
        "口语化触发",
        "植入触发",
        "收尾触发",
        "最终结构去重",
    ):
        assert heading in registry

    agents = read(AGENTS)
    router = read(WENAN)
    assert "generation-trigger-registry.md" in agents
    assert "generation-trigger-registry.md" in router


def test_deprecated_packaging_first_rules_are_not_executable() -> None:
    active = "\n".join(
        read(path)
        for path in (
            AGENTS,
            WENAN,
            REFERENCES / "expression-craft.md",
            REFERENCES / "hook-pattern-library.md",
            REFERENCES / "company-soft-placement.md",
            REFERENCES / "b2b-content-quality-gate.md",
        )
    )
    for deprecated in (
        "每条文案至少用 3 种不同逻辑",
        "连续 3 次不重复",
        "隔三跳一",
        "先选“钩子”→再选“软植入策略”",
        "最后根据开头情绪",
        "每次轮换使用，禁止连续用同一种",
        "超过25字必须打断",
        "超过 25 字必须打断",
        "连续两句长句后",
        "5字以内的短句",
        "机制段末必须",
        "每段首句必须",
    ):
        assert deprecated not in active


def test_shared_topic_weight_table_is_not_copied_into_skills() -> None:
    for path in sorted(SKILLS_ROOT.glob("*/SKILL.md")):
        content = read(path)
        assert "话题类型与技法权重对照表" not in content, path


def test_generating_skills_delegate_shared_routing_and_do_not_fix_a_skeleton() -> None:
    for name in GENERATING_SKILLS:
        content = read(SKILLS_ROOT / name / "SKILL.md")
        assert "generation-trigger-registry.md" in content, name
        assert "Default Structure" not in content, name

    for relative in PATTERN_FILES:
        content = read(SKILLS_ROOT / relative)
        assert "Default Structure" not in content, relative


def test_humanizer_rechecks_unverified_user_drafts_and_can_change_macro_shape() -> None:
    content = read(HUMANIZER)
    assert "用户直接提供" in content
    assert "不得自动视为已核实" in content
    assert "删除重复脚手架" in content
    assert "重排段落" in content
    assert "事实命题、限定条件、因果强度和责任关系" in content


def test_complete_script_has_one_final_delivery_not_a_forced_before_after_pair() -> None:
    router = read(WENAN)
    agents = read(AGENTS)
    assert "一份最终口播文案" in router
    assert "一份通过事实复检" in agents
    assert "原文案、优化后文案" not in router


def test_structure_dedup_uses_meaning_not_sentence_library_indices() -> None:
    registry = read(TRIGGER_REGISTRY)
    for dimension in (
        "主信息关系",
        "证据形态",
        "公司角色",
        "结尾形式",
        "表层句法骨架",
    ):
        assert dimension in registry
    assert "`主信息关系｜证据形态｜公司角色｜结尾形式｜表层句法骨架`" in registry

    manifest = json.loads(read(MANIFEST))
    assert manifest["structure_signature"] == [
        "main_relation",
        "evidence_form",
        "company_role",
        "ending_form",
        "surface_skeleton",
    ]

    ledger = json.loads(read(STRUCTURE_LEDGER))
    entry_schema = ledger["entry_schema"]
    for required in manifest["structure_signature"]:
        assert required in entry_schema
    for retired_pre_draft_dimension in ("action_sequence", "ending_task"):
        assert retired_pre_draft_dimension not in entry_schema

    assert "不把签名相同直接作为否决条件" in registry
    assert "多样性不得覆盖真实性" in registry
    assert "没有历史记录" in registry
    assert "不得声称" in registry
