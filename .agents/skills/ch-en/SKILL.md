---
name: ch-en
description: 中文小说转英文skill
---

将此提示词粘贴给 AI（如 ChatGPT、Claude），配合你的中英文稿使用。AI 会逐项检查并输出问题清单。
使用方式
请用以下标准逐项检查我的英文翻译。每项只输出发现的问题，通过的项目可以跳过不报。
【中文原稿】[粘贴中文全文]
【英文译稿】[粘贴英文全文]
检查标准如下：
第一轮：全局结构性检查
1. 学术引注扫描
全文搜索 (See, (cf., (Records of, (Book of, (History of 等括号引注
统计出现次数
标准：AlphaNovel 通俗读物正文中不应出现学术括号引注
每处标注：应删除/融入叙述/移入章末注释
2. 拼音术语词典式排版扫描
全文搜索 (Rén —、(Dào —、(Lǐ — 等拼音加破折号英文释义的格式
统计出现次数
标准：每个术语首次出现用一句话自然解释，不应出现词典式括号罗列
每处标注：应改写为嵌入式自然解释
3. 语气一致性检查
判断全文语气归属：A) 学术通俗读物（如 Sapiens）B) 口语聊天式（如 Mark Manson）C) 两者之间反复横跳
标准：必须统一为一种语气。AlphaNovel 偏向 B。
标注语气来回切换的具体段落位置
第二轮：中式英语 / 中文语感残留
逐句检查以下模式，发现即标注原文行号和问题：

4. 直译句式
Pause for a moment. → 中文“暂停一下”的直译，英文口语不这么说
The answer is absolutely yes. → “答案是：绝对能”直译
What we want to do here is... → “我们要做的是”直译
let us formally introduce... → “隆重介绍”直译
All right, my friend— → “好了，朋友”直译
I know that... → “我知道”直译（英语常可省略）
not merely X, but also Y → “不仅……而且”的惯性映射（检查是否滥用）
5. 中文修辞习惯映射
三连排比：检查 A, B, and C 式三连动词/名词短语是否来自中文三段式排比（如“应对内卷、摆脱焦虑、实现自我突破”）
成语硬译：检查是否存在四字成语逐字翻译造成的不自然表达
重复强调：中文常说“A 就是 A”类强调，检查英文是否存在冗余重复
6. 中文逻辑连接词残余
therefore / thus / hence 频率是否过高（中文“因此”“所以”惯性映射）
on the contrary / in contrast 是否必要
of course / naturally / undoubtedly 是否在中文对应处必然出现
第三轮：术语与用词
7. 术语生僻度检查
对下列高频哲学术语，检查英文选词是否过于学术、美国普通读者是否需要查字典： | 中文 | 生僻/学术化（违规） | 可接受 | | --- | --- | --- | | 无为 | noncoercive action, non-action | effortless action, acting without forcing | | 浩然之气 | floodlike moral energy, vast-flowing spirit | vast spirit, boundless moral force | | 君子 | superior person, exemplary person | (exemplary person 可接受但需自然解释） | | 礼 | ritual propriety | propriety / right conduct / ritual（视语境） | | 兼爱 | impartial care / inclusive care | universal love, love without distinction | | 仁 | humaneness | benevolence, compassion, human-heartedness | | 道 | the Way / the Path | （可接受，但 Dao 单独使用也可） | | 天理 | heavenly principle | （可接受但需首次解释） | | 良知 | innate moral knowing / conscience | (innate moral knowing 可接受） |

8. 用词过于正式检查
搜索以下词汇频率，判断是否过量：

moreover, furthermore, nevertheless, consequently, accordingly
profound, enduring, inexhaustible, lofty
标准：每 1000 词不超过 2-3 次
9. 中文概念直译成怪词检查
搜索 life-upgrade guide、strategist of life、hall of wisdom — 这些都是中文“人生升级攻略”“人生战略家”“智慧殿堂”的直译，英语读者会觉得 awkward
标准：必须找到英语母语者真正会用的对应表达
第四轮：句法与节奏
10. 句子长度检查
统计超过 35 词的句子数量
标准：网文段落每句平均 15-25 词，复杂句不超过 30-35 词
超标句子逐句标注
11. 段落长度检查
统计超过 8 行的段落
标准：移动端阅读（AlphaNovel 主要场景）每段不超过 5-6 行
12. 重复句式模式检查
搜索连续段落是否以相同结构开头（如连续三段以 He... / They... / It is... 开头）
搜索 not only... but also 的复现频率
搜索 In his view, / He believed / He argued 的复现频率
第五轮：美国读者可理解性
13. 文化负载词检查
标注所有英文读者不可能从上下文推断含义的文化专有名词，包括但不限于：

中文书名拼音（如 Shi Ji、Lun Yu）——检查是否给了英文通称或简短解释
历史官职（如“守藏室之史”）
特定典故（如“孟母三迁”）
标准：每个必须能在句中理解，不能依赖读者已有知识
14. 人称一致性检查
全文搜索 you、we、one、the reader
标准：统一人称。AlphaNovel 推荐用 you 为主，we 为辅
标注人称混乱的位置
输出格式
请按以下格式输出检查结果：

=== 第一轮：全局结构性检查 ===
1. 学术引注：[数量]处 → [处理建议列表]
2. 拼音术语词典排版：[数量]处 → [位置列表]
3. 语气一致性：[判断] → [具体位置]
=== 第二轮：中式英语 ===
4. 直译句式：[数量]处 → [逐条：行号+原文+问题+建议]
5. 中文修辞映射：[数量]处 → [逐条]
6. 逻辑连接词残余：[数量]处 → [逐条]
=== 第三轮：术语用词 ===
7. 术语生僻度：[逐条标注]
8. 过于正式用词：[统计+超标项]
9. 直译怪词：[逐条标注]
=== 第四轮：句法节奏 ===
10. 超标长句：[数量]句 → [行号列表]
11. 超标长段落：[数量]段 → [行号列表]
12. 重复句式模式：[具体标注]
=== 第五轮：可理解性 ===
13. 文化负载词：[逐条标注+可理解性评估]
14. 人称一致性问题：[具体标注]
=== 总评 ===
- 通过项数 / 总项数
- 是否可发布（需全部通过）
- 优先修改建议（P0/P1/P2 分级）
附：快速自检口诀（人工用）
一读出声：舌头打结处必改。二看引注：括号来源全删除。三查拼音：词典格式全改写。四数长句：一行超30词就断。五听语气：学术腔和聊天腔只能留一个。六想读者：10年级阅读水平的美国人能不能看懂每一句？ 自行规划翻译长度，如果超出一次输出的最大限度，就分成几个文件生成。不要缩减提炼减少内容。