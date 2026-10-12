# NEXT_STEP · 当前任务与下一步

> 这是**最重要的记忆文件**。
> 每次结束任务时，AI 立即更新本文件。
> 每次新对话开始时，AI **首先读取**本文件。

---

## 当前任务

**任务名称**：建立「项目规则 + 项目记忆 + Git 版本管理」机制 ✅

**当前阶段**：机制建立完成 / 待用户确认 AI 插件

**本次目标**：
1. 在当前目录创建 `AGENTS.md`、`docs/learning/*.md`、`.gitignore`。
2. `git init` 并做首次提交。
3. 提示用户补全 IntelliJ IDEA 中使用的 AI 插件信息（影响规则文件路径）。

**已确认事实**：
- 当前目录：`/Users/wyz/Downloads/sjava`
- GitHub 仓库：`https://github.com/44510709/sjava.git`（**未 clone**，按用户要求「项目先不搭建」）
- 操作系统：macOS（Darwin 24.2.0，从环境信息推断，**未经 `sw_vers` 命令确认**）
- IDE：IntelliJ IDEA（用户已确认）
- Git：2.39.3 已可用

**已完成操作**：
- [x] `mkdir -p docs/learning`
- [x] 移动 `JAVA_RUOYI_MASTER_PROMPT.md` → `docs/learning/`
- [x] 写入 `.gitignore`
- [x] 写入 `docs/learning/PROJECT_STATE.md`
- [x] 写入 `docs/learning/PROJECT_MAP.md`
- [x] 写入 `docs/learning/PROGRESS.md`
- [x] 写入 `docs/learning/ERROR_LOG.md`
- [x] 写入 `docs/learning/DECISIONS.md`
- [x] 写入 `docs/learning/NEXT_STEP.md`
- [x] 写入 `AGENTS.md`
- [x] `git init`
- [x] 首次提交 `chore: 初始化项目机制（规则 / 记忆 / Git）`

**当前问题**：无

**下一步操作**：
1. 用户确认 IntelliJ IDEA 中具体使用的 AI 插件。
2. 根据插件，AI 给出该插件对应的规则文件配置建议（不影响本机制的主干）。
3. 用户开始按 `NEXT_STEP.md` 切换到「环境验证阶段」。

---

## 下一阶段：环境验证

> 当用户确认「机制 OK，可以开始」时进入该阶段。

### 步骤
1. 确认操作系统版本（`sw_vers` / `uname -a`）
2. 确认包管理器（Homebrew 状态、版本）
3. 确认 Java / Maven / 数据库是否已安装
4. **不预先装，先 clone 仓库**
5. clone 后核对：
   - 实际项目 README 与架构
   - Java / Maven / 数据库版本要求
   - 是否真是若依
6. 用户同意后再安装 / 启动 / 跑通

### 完成标准
- 项目能 clone 到本地
- `mvn -v` 与项目要求一致
- `mvn clean compile` 通过
- 至少能启动 `ruoyi-admin`（或对应主模块），控制台无致命错误

### 注意事项
- **不**未经用户同意安装 JDK / Maven / 数据库。
- **不**未经用户同意执行 `git remote add origin` / `git push`。
- **不**做任何破坏性操作（删除文件、reset --hard、强制 push）。
- clone 后第一时间核对实际版本再继续。

---

## 任务切换规则

1. **任务完成时**：AI 必须更新本文件，把已完成项打勾、记录下一步。
2. **任务切换时**：AI 必须更新本文件，**不**直接开始新任务。
3. **多日跨度时**：本文件是首选恢复点，比聊天历史更可靠。
4. **计划与现状冲突时**：以本文件为准，但要带证据修正。

---

## 更新历史

| 日期 | 更新摘要 | 操作 |
|---|---|---|
| 2026-10-12 | 初始化；首次建立机制完成 | AI 自动 |
