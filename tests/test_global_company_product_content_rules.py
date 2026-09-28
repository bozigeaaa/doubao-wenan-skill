import json
import re
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[1]
PROJECT_RULES = PROJECT_ROOT / "AGENTS.md"
ROUTER = PROJECT_ROOT / ".agents/skills/wenan-skill/SKILL.md"
PLACEMENT = PROJECT_ROOT / ".agents/skills/references/company-soft-placement.md"
QUALITY_GATE = PROJECT_ROOT / ".agents/skills/references/b2b-content-quality-gate.md"
TOPIC_LOOP = PROJECT_ROOT / ".agents/skills/references/b2b-topic-conversion-loop.md"
README = PROJECT_ROOT / "README.md"
MANIFEST = PROJECT_ROOT / ".agents/skills/references/generation-manifest.json"
TRIGGER_REGISTRY = PROJECT_ROOT / ".agents/skills/references/generation-trigger-registry.md"
FIRE_TOPIC_LIBRARY = PROJECT_ROOT / ".agents/skills/saudi-camp-fire-script/references/fire-topic-library.md"
HOTSPOT_TITLE_SELECTION = PROJECT_ROOT / ".agents/skills/global-hotspot-industry-impact-script/references/title-selection.md"

SPECIALIST_FILES = [
    PROJECT_ROOT / ".agents/skills/saudi-breakout-story-script/SKILL.md",
    PROJECT_ROOT / ".agents/skills/global-hotspot-industry-impact-script/SKILL.md",
    PROJECT_ROOT / ".agents/skills/saudi-professional-knowledge-script/SKILL.md",
    PROJECT_ROOT / ".agents/skills/saudi-light-steel-script/SKILL.md",
    PROJECT_ROOT / ".agents/skills/saudi-sanitary-unit-script/SKILL.md",
    PROJECT_ROOT / ".agents/skills/saudi-camp-fire-script/SKILL.md",
    PROJECT_ROOT / ".agents/skills/saudi-product-seeding-script/SKILL.md",
    PROJECT_ROOT / ".agents/skills/saudi-brand-proof-script/SKILL.md",
]


def read(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def assert_contains(content: str, expected: str, name: str) -> None:
    assert expected in content, f"Missing {name}: {expected}"


def test_global_rules_gate_company_and_product_content_by_relevance() -> None:
    project_rules = read(PROJECT_RULES)
    router = read(ROUTER)
    placement = read(PLACEMENT)
    quality_gate = read(QUALITY_GATE)
    readme = read(README)

    # 2026-09-23 用户确认：公司/产品是默认植入项，不依赖条件触发。
    # 核心规则统一为“默认执行植入，但内容必须按相关性把关、用户明确要求不写时排除”。
    for content, label in (
        (project_rules, "project rules"),
        (router, "router"),
        (quality_gate, "quality gate"),
        (placement, "placement rules"),
        (readme, "README"),
    ):
        assert "默认植入" in content or "默认执行" in content, (
            f"Missing default-placement semantic in {label}"
        )
        assert "用户明确要求不写" in content, (
            f"Missing explicit opt-out in {label}"
        )

    assert_contains(placement, "默认植入", "default placement")
    assert_contains(readme, "默认植入", "default placement in README")
    assert_contains(project_rules, "用户明确要求不写时直接排除", "explicit opt-out")
    assert_contains(placement, "检查不等于必须植入", "conditional placement")
    assert_contains(placement, "帮助回答同一判断动作或变量", "substantive placement")


def test_global_rules_lock_semantic_promise_and_keep_claims_relevant_to_its_answer() -> None:
    project_rules = read(PROJECT_RULES)
    router = read(ROUTER)
    quality_gate = read(QUALITY_GATE)
    placement = read(PLACEMENT)
    readme = read(README)

    for content, label in (
        (project_rules, "project rules"),
        (router, "router"),
        (quality_gate, "quality gate"),
        (readme, "README"),
    ):
        assert_contains(content, "内容承诺", f"content promise in {label}")
        assert_contains(content, "判断动作或变量", f"decision dimension in {label}")

    assert_contains(router, "本稿必须给出的答案", "required answer in router state")
    assert_contains(project_rules, "本稿必须给出的答案", "required answer in project state")
    assert_contains(quality_gate, "可证结论必须直接回答标题锁定的判断动作或变量", "answerability gate")
    assert_contains(placement, "所需答案", "placement answer requirement")
    assert_contains(project_rules, "直接回答标题承诺、提供回答所需证据，或解释证据为何改变答案", "claim relevance")
    assert_contains(quality_gate, "直接回答语义承诺、提供回答所需证据，或解释该证据为什么会改变答案", "quality claim relevance")
    assert_contains(placement, "提供所需证据或解释证据为何改变答案", "placement claim relevance")
    assert_contains(project_rules, "让本篇目标受众不需要暂停思考或反复回看也能跟上", "target-audience clarity")
    assert_contains(router, "受众可用结果", "viewer usable result")
    assert_contains(quality_gate, "低认知负荷", "low-cognitive-load gate")
    assert_contains(router, "同一论证链中承担真实角色", "router company bridge")


def test_evidence_strength_is_calibrated_instead_of_forcing_absolute_claims() -> None:
    project_rules = read(PROJECT_RULES)
    placement = read(PLACEMENT)

    assert_contains(project_rules, "证据不要求一次证明所有结果", "calibrated evidence")
    assert_contains(placement, "保留项目用途、图纸、业主要求、配置、审批路径", "qualified claim conditions")
    assert_contains(placement, "不把可能性、比较判断或风险降低写成确定结果", "no causal upgrade")
    assert_contains(placement, "不自行补造客户反馈、项目结果", "no invented outcomes")


def test_topic_conversion_can_change_angle_or_reject_when_no_valid_bridge_exists() -> None:
    project_rules = read(PROJECT_RULES)
    placement = read(PLACEMENT)
    topic_loop = read(TOPIC_LOOP)

    assert_contains(project_rules, "先转换真实角度", "angle conversion")
    assert_contains(project_rules, "不值得写", "angle rejection")
    assert_contains(placement, "仍不成立就停止植入", "placement rejection")
    assert_contains(topic_loop, "先转换角度", "topic conversion")
    assert_contains(topic_loop, "不值得写", "topic rejection")


def test_all_specialist_skills_delegate_conditional_placement_to_shared_rules() -> None:
    for path in SPECIALIST_FILES:
        content = read(path)
        assert_contains(content, "generation-trigger-registry.md", f"trigger registry in {path.name}")
        assert "公司和产品必须参与回答同一个核心问题" not in content, path


def test_active_runtime_documents_match_the_semantic_promise_contract() -> None:
    for content, label in ((read(PROJECT_RULES), "project rules"), (read(README), "README")):
        assert_contains(content, "内容承诺", f"content-promise contract in {label}")
        assert_contains(content, "判断动作或变量", f"decision-dimension contract in {label}")

    assert_contains(read(PROJECT_RULES), "用户明确要求不写", "explicit opt-out in project rules")

    router = read(ROUTER)
    assert_contains(router, "本稿必须给出的答案", "required-answer contract in router")
    assert_contains(router, "明确不写", "explicit opt-out in router")

    placement = read(PLACEMENT)
    assert_contains(placement, "同一判断动作或变量", "decision-dimension contract in placement rules")
    assert_contains(placement, "用户没有明确要求不写公司和产品", "explicit opt-out in placement rules")


def test_audience_value_gate_changes_a_real_decision_without_prescribing_prose_shape() -> None:
    manifest = json.loads(read(MANIFEST))
    stages = manifest["stages"]
    assert stages.index("check_promise_answerability") < stages.index("check_audience_value")
    assert stages.index("check_audience_value") < stages.index("draft")

    registry = read(TRIGGER_REGISTRY)
    for expected in (
        "明确受众",
        "改变一个判断",
        "可核对依据",
        "责任或适用边界",
        "提前确认、注意核对、找供应商沟通",
        "缩小承诺、补证据或停止成稿",
        "不得用 CTA、清单、术语或篇幅",
        "不规定段落、句式或收尾",
    ):
        assert_contains(registry, expected, f"audience-value rule: {expected}")

    usable_result_contract = "可核对依据、责任或适用边界，或会影响决策的因果理解"
    for content, label in ((read(PROJECT_RULES), "project rules"), (read(ROUTER), "router")):
        assert_contains(content, usable_result_contract, f"usable-result contract in {label}")
        assert "判断、核对动作或责任边界" not in content, label


def test_fire_topic_library_exposes_evidence_scopes_not_finished_question_frames() -> None:
    topic_library = read(FIRE_TOPIC_LIBRARY)
    assert not re.search(
        r"(?mi)^\s*(?:[-*]\s*)?Core question:\s*.+[?？]\s*$", topic_library
    )
    assert_contains(topic_library, "evidence scopes", "evidence-scope boundary")
    assert_contains(topic_library, "not title wording, question forms, or script structures", "non-template boundary")


def test_hotspot_title_rules_do_not_anchor_every_candidate_to_finished_question_examples() -> None:
    title_rules = read(HOTSPOT_TITLE_SELECTION)
    assert "Examples for delivery-related hotspots" not in title_rules
    assert not re.search(r"(?m)^\s*标题：.+[?？]?\s*$", title_rules)
    assert_contains(title_rules, "Do not keep finished sample titles", "no finished title anchors")
