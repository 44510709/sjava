# CURRENT_TASK · 当前任务与下一步

> 这是**最关键的动态记忆文件**。
>
> 每次会话开始，AI 必须**先读本文件**。
> 每次会话结束，AI 必须**更新本文件**。
>
> 注意：本文件由 `NEXT_STEP.md` 合并而来，不再保留 `NEXT_STEP.md`。

---

## 当前任务

### 任务名称

建立「AI 开发与学习控制系统」（**进行中**）

### 当前阶段

机制建立完成；待用户做"新会话恢复测试"。

### 本次目标（本任务范围内）

1. ✅ 设计一套可恢复、可验证的控制系统（参考用户方案 v2）。
2. ✅ 改造文件结构：建立 `CLAUDE.md` 入口，升级 `AGENTS.md` 为 11 章规则。
3. ✅ 创建长期 / 训练 / 任务类文件：`PROJECT_OVERVIEW` / `LEARNING_PROFILE` / `TRAINING_PROTOCOL` / `ROADMAP` / `CURRENT_TASK` / `SESSION_LOG`。
4. ✅ 移动 `PROJECT_MAP` / `PROJECT_STATE` 到 `docs/`。
5. ✅ 删除旧 `NEXT_STEP.md`。
6. ✅ Git 提交本次改造（commit `e76223f`）。
7. ⏳ 等用户做新会话恢复测试，确认机制生效。

### 已确认事实（带证据）

| 事实 | 证据 |
|---|---|
| 当前目录 = `/Users/wyz/Downloads/sjava` | `pwd` 输出 |
| Git 仓库已 init 在 main 分支 | `git log --oneline` |
| 首次提交：`chore: 初始化项目机制（规则 / 记忆 / Git）` | `git log --oneline` |
| GitHub 仓库：`https://github.com/44510709/sjava.git` | 用户提供 |
| 仓库**未 clone** | `ls -la` 中无源码 |
| 操作系统 = macOS | 系统环境（`Darwin 24.2.0`） |
| IDE = IntelliJ IDEA | 用户 2026-10-12 确认 |
| **AI 工具 = Claude Code** | 用户 2026-10-12 确认 |
| Git 版本 = 2.39.3 | `git --version` |

### 未确认（待验证）

- 操作系统版本（`sw_vers` 未实际执行）
- 用户是否已在 IntelliJ IDEA 中安装 Claude Code 集成（CLI 与 IDE 是两条路径）
- JDK / Maven / 数据库是否已装
- 用户的工作流偏好（CLI 开在终端 vs IDE 内嵌插件）
- 是否准备 clone `sjava` 仓库

### 当前问题

无阻断性问题。剩下的是：

1. 用户实际验证"新会话能否恢复上下文"
2. 用户下一步意图（环境检查 / clone / 暂缓）

### 下一步操作

**给用户的建议步骤**：

1. **新开会话做恢复测试**
   - 新建 Claude Code 会话，发送 `CLAUDE.md` 第 6 节的测试指令
   - 观察 Claude 是否列出读了哪些文件，能否区分事实 / 推断 / 待确认
2. **如果测试通过** → 准备进入"环境检查"阶段
3. **如果测试失败** → 检查 `CLAUDE.md` 路径或读取机制，回到本文件讨论

---

## 当前任务完成判断标准

| 验收项 | 是否满足 |
|---|---|
| `AGENTS.md` 升级为系统性 11 章规则 | ✅ |
| `CLAUDE.md` 作为 Claude Code 入口存在 | ✅ |
| 三大类记忆（稳定 / 项目事实 / 动态）各有归属文件 | ✅ |
| 当前任务文件统一为 `CURRENT_TASK.md` | ✅ |
| 学习档案（LEARNING_PROFILE / TRAINING_PROTOCOL / ROADMAP）建立 | ✅ |
| 会话交接记录（SESSION_LOG）建立 | ✅ |
| Git 提交完整、可回滚 | ✅ |

**全部 ✅ 才能把"建立控制系统"任务标记为完成。**

---

## 下一任务占位（用户确认后填写）

> 完成后 AI 必须更新本节。模板：

```markdown
### 下一任务

**任务名称**：_

**前置条件**：本任务全部 ✅

**目标**：见 CURRENT_TASK.md 新版
```

---

## 任务切换规则

1. 任务完成时：AI 必须更新本文件，把已完成项打勾、记录下一步。
2. 任务切换时：AI 必须更新本文件，**不**直接开始新任务。
3. 多日跨度：本文件是首选恢复点，比聊天历史更可靠。
4. 计划与现状冲突：先核实事实，以本文件为准修正。

---

## 版本

| 日期 | 变更 |
|---|---|
| 2026-10-12 | 首版建立（合并自 `NEXT_STEP.md`） |
