Ver. 0.1
# AI 自动知识整理系统 IdeaSecretary 烂笔头
请详细阅读本文档作为产品需求。同时可以将其作为待办清单，但是不要删除和修改内容。清单和完成情况概括应当附在文件末尾。产品文档应放在product document文件夹下。你也应当记录此文件，以便后续容易查找到需求文档的变化。
你应该思考我的需求是否合理，是否有改进空间，若有，向我询问并修改。你应该分析我的需求，并列出对后续开发的指导性意见。对于本文档没有涉及的部分，使用业界常用设计理念和方法完成。

## 概览
通过用户输入的内容，可以是文本、图片、链接等，自动进行知识整理。同时相应用户对知识库的问题请求。

## 架构
前后端分离，不过目前仅使用单个机器。

## UI设计
注意，同时兼容中文和英语。以英语作为主体和默认，根据客户端语言自动切换，适配深色和浅色模式。
### 介绍页面
IdeaSecretary                    Mission | Login & Regiseter
---


IDEA SECRETARY
(Flowing translations of "Ideas" in different languages, slowly, from right to left, with a faded color)



Mission
Are you troubled with your fantastic ideas? Do you want to document your thoughts and the way you have been without wasting too much time? IDEA SECRETARY is a tool to help you organize your ideas. Message, speak, or chat, whatever you like. You may be inspired by chatting.

Github link; author link(howl-fang.github.io)

### 登录页面
<通常设计>

### 仪表盘 (侧边，允许折叠至只显示图标，通常显示图标和文字。图标在左文字在右)
Treasury |
My Idea Base |
...
Account |
Settings |

#### Treasury
----------------
Chat Box; with speech to choose; can paste pictures. Urls are also supported.
<Features: # keep input; # give me inspiration; # talk to yourself>
<Default display: what comes up to your mind today? / Wanna have a mindstorm?>
----------------
<Suggestions on existing ideas, could be recommendation, or what you find useful.>
<Statistics: how many ideas, total words count, avaliable inspirations>

#### My Idea Base
<View: default in tree, avaliable in mindmap>
<Features: manually modifications, rebalance(sort out)>

#### Account
<openai api: openai api key blank; also provide url blank for self-hosted openai api>
<other features>

## AI调用
1. 使用openai api作为调用框架，支持官方api和自建api。
2. 使用维护的索引作快速查询，并且及时更新索引
3. 需要想出合理prompt，作为系统提示词。让用户直接丢入数据可以直接开始整理。
4. 对内容有思考和新想法，放在和用户输入存储的位置附近。
5. 对于其他部分的功能，也要添加相应的提示词机制。
6. 对于ai回复的错误控制格式，要有反馈语法的错误，并重新生成

## 数据存储方式
1. 使用ORM的SQLite数据库存储文本数据，其中使用markdown格式，同时维护一份索引用于快速查询。
2. 主要是用树形结构
3. 维护一个媒体资源索引，将媒体文件存在单独文件夹下，用uuid命名。媒体删除要保留在回收站，并定期清理。
4. 每隔一段时间整理知识库，精简库
5. 可以导出数据库为正常可读的zip文件，也可以生成思维导图。
6. 默认一个库，但是可以创建多个库。库之间没有联系，但可以共用媒体资源，共同维护媒体资源索引。
7. 每隔一定操作数，备份数据库。删除过时的数据库。

---

## 开发清单与完成情况（自动追加）

### 已完成
- [x] 使用 `uv` 初始化项目依赖管理（新增 `pyproject.toml` 与 `uv.lock`），并验证测试可通过。
- [x] 基于文档创建可运行后端（FastAPI + SQLite + ORM）。
- [x] 实现知识库管理（创建/列表）。
- [x] 实现 Idea 入库（支持 source_type/source_value，自动 AI 整理并存储 markdown）。
- [x] 实现树结构查询接口（`/api/ideas/library/{library_id}/tree`）。
- [x] 实现媒体资源索引与存储（UUID 命名）及回收站软删除。
- [x] 实现基础索引维护与问答接口。
- [x] 实现导出 zip 与 mindmap 文本接口。
- [x] 实现按操作计数触发数据库备份并清理旧备份。
- [x] 实现基础 UI：英语默认 + 中文切换，深浅色切换，Treasury 输入页面。
- [x] 产出产品文档到 `Documents/Product Document/MVP_Product_Document.md`。
- [x] 记录需求文档实现进展（本节）。

### 未完成 / 下一步
- [ ] 登录与注册完整流程（当前仅预留页面概念）。
- [ ] 语音输入与图片内容理解（当前仅支持媒体上传与引用）。
- [ ] 更强索引（FTS/向量）与推荐统计模块。
- [ ] UI 组件化与完整仪表盘交互。

### 对需求的改进建议（待你确认）
1. 第一阶段先收敛到“文本 + URL + 问答 + 导出”闭环，降低多模态复杂度。
2. 明确导出格式优先级（Mermaid / XMind / FreeMind）避免后续重复开发。
3. 明确账号体系（邮箱密码 or OAuth）以便尽早设计数据模型。

### 需求变更追踪说明
- 当前文档版本标识：`Ver. 0.1`
- 已将本次实现与建议固定在：`Documents/Product Document/MVP_Product_Document.md`