# 新闻标题选择

## 标题任务

新闻标题不设置固定结构，也不强制写成项目问题。可以突出已核验新闻、变化、反差、受众处境、产品场景或项目判断中的任一重点，但须让观众立即识别本条与哪个行业对象、受众或具体场景有关。

用户从新闻核验卡选定新闻和产品后，标题须保持所选产品及结合理由，不得转向其他产品或纯新闻评论。产品名称不强制出现在标题文字中；不写产品名时，用沙特工地、工程营地、临建设施、项目采购等对象说明内容范围。标题承接同一个核心内容和传播承诺。

标题可以使用悬念、反差、风险感和情绪化口语增强点击，不必写完整证据链；可以放大关注点，但不能反转或编造事实。不得把“可能发生”写成“已经发生”，也不得暗示新闻项目已经采购、使用、要求或收到所选产品，除非核验来源明确证明。

## 候选数量与阶段

- 标题方向阶段遵循 `$wenan-skill`：默认生成 5 个，确有足够不同且可成稿的方向才给满，不足少给、不凑数；每个方向输出一个标题，候选另列理由、可写点、内容规划、新闻出处（字段定义以 `AGENTS.md` 为准）。
- 用户对候选不满意时，可要求更换，重新生成 5 个（换方向，不换表达）；第二轮更换后仍未满意，转用户直接给出方向或主题，系统按用户指示写。
- 用户直接要求完整文案且未要求候选时，内部比较后最终输出一个标题。
- 方向候选须显示所选产品及结合理由；产品名是否进入标题，按清晰度决定。
- 标题选定后进入定思路环节（见 `$wenan-skill`），按证据给出写作思路候选；可融合时提出融合建议。

## 本地交付能力触发条件

When the verified hotspot directly concerns shipping, ports, sailing schedules, imports, 跨境采购, arrival-to-site delivery, warehousing, distribution, installation, or delivery responsibility, include a genuinely distinct direction from the **local delivery capability** perspective when evidence supports it.

- Check whether the Saudi-local production, regular-stock allocation, parts supply, delivery, installation, and follow-up responsibility chain can actually support the project.
- Prefer titles that teach the buyer how to verify real local delivery capability; do not turn the title into a generic claim that all local suppliers are better.
- Do not default to China-side or overseas-shipment framing. Mention China, overseas sources, imports, or 跨境采购 only when that pathway is a verified and necessary part of the specific topic.
- For fire, approval, material, technical-selection, or camp-operation topics, do not force a local-delivery title unless local fulfilment responsibility is the verified decision variable and required answer.

Do not keep finished sample titles in this rule. Generate the wording only after the verified content promise is locked, so nearby examples cannot pull every title toward the same question form.

## 事实红线

- 具体事件、主体、数字和确定性结果须有依据。
- 可以省略不改变事实性质的背景条件，不能省略会反转结论的关键条件。
- 标题吸引点须由正文兑现，不用无关热点为产品制造机会感。

## Final Title Check

Before finalizing, ask internally:

- Does the title rely on a verified fact?
- Can a viewer identify the industry object, audience, or scene at first glance?
- Is the title normally within 19–36 characters?
- Does the title express one core content and remain natural and understandable in one reading?
- Does it remain compatible with the user-selected product and the verified product-fit reason?
- Does it avoid implying that the project already adopted or requested the product?
- If it uses the local-delivery angle, does the verified topic actually concern delivery or cross-border dependence rather than an unrelated technical issue?
