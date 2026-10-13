# 测试脚手架使用手册 · P1（2026-10-13）

> 给 RuoYi-Vue-Plus 6.0.0 + Spring Boot 4.1.1 业务模块写测试时用。
> P1 第一站以 `ruoyi-system/config` 为最小样板。

---

## 1 · 30 秒速查

| 测什么 | 用哪个注解 | 文件 |
|---|---|---|
| **Service 纯逻辑**（绕开缓存/Mapper链式） | `@ExtendWith(MockitoExtension.class)` | `src/test/java/.../service/impl/*LogicTest.java` |
| **Controller 路由 + 参数绑定 + JSON 响应** | `@WebMvcTest` + `@MockitoBean` | `src/test/java/.../controller/*Test.java` |
| **集成测试**（启动容器，连真实 PG/Redis） | `@SpringBootTest(classes = SystemTestApplication.class)` | 同上 |
| **Mapper**（真实 SQL） | `@SpringBootTest` + `@Autowired Mapper` | `src/test/java/.../mapper/*Test.java` |

---

## 2 · Spring Boot 4.x 的两件大事（必读）

### 2.1 模块拆分

Spring Boot 4 把原来 `spring-boot-starter-test` 里的部分注解挪到了独立 artifact：

| 注解 | 3.x 包 | 4.x 包 | 需要额外加的依赖 |
|---|---|---|---|
| `@WebMvcTest` | `org.springframework.boot.test.autoconfigure.web.servlet.WebMvcTest` | `org.springframework.boot.webmvc.test.autoconfigure.WebMvcTest` | `spring-boot-starter-webmvc-test` |
| `@MockitoBean`（推荐） | — | `org.springframework.test.context.bean.override.mockito.MockitoBean` | （spring-test 7 自带） |
| `@MockBean`（deprecated） | `org.springframework.boot.test.mock.mockito.MockBean` | 同左（位置未变） | `spring-boot-test` |

**操作**：在要用 `@WebMvcTest` 的模块 pom 加：

```xml
<dependency>
    <groupId>org.springframework.boot</groupId>
    <artifactId>spring-boot-starter-webmvc-test</artifactId>
    <scope>test</scope>
</dependency>
```

### 2.2 `@MockBean` 已 deprecated

Spring 官方推荐改用 Spring Framework 7 的 `@MockitoBean`：

```java
// 旧（还能用，4.x 保留）
@MockBean
private ISysConfigService service;

// 新（推荐，4.x 起官方）
@MockitoBean
private ISysConfigService service;
```

两者行为基本一致；本项目脚手架统一用 `@MockitoBean`。

---

## 3 · 样板：业务模块测试的两类写法

### 3.1 Service 纯逻辑测试

适用：方法不依赖 MyBatis-Plus `mapper.lambda()` 链式调用、也没被 `@Cacheable` 包裹。

```java
@ExtendWith(MockitoExtension.class)
class SysConfigServiceLogicTest {

    @Mock
    private SysConfigMapper configMapper;  // Mapper 是接口，可直接 Mock

    @InjectMocks
    private SysConfigServiceImpl service;  // 真实注入被测 Service

    @Test
    @DisplayName("按 ID 查询：直接返回 mapper 的 VO 结果")
    void shouldReturnVoFromMapperWhenSelectById() {
        // given
        SysConfigVo expected = new SysConfigVo();
        when(configMapper.selectVoById(1L)).thenReturn(expected);

        // when
        SysConfigVo actual = service.selectConfigById(1L);

        // then
        assertEquals(1L, actual.getConfigId());
    }
}
```

**局限**：
- MyBatis-Plus 的 `mapper.lambda().eq(...).one()` 链式调用难以 Mock（返回类型每一步都在变）。
  涉及该写法的 Service 方法留给 `@SpringBootTest` 集成测试，或绕开 lambda 用 Criteria/QueryWrapper 直接构造。
- `@Cacheable` / `@CachePut` 注解在没有 Spring 缓存管理器的测试中不会拦截方法体，方法照常执行。
  但要测"缓存命中/失效"路径就需要 `@SpringBootTest` + 真实 Redis。

### 3.2 Controller 路由测试

适用：验证 URL、参数绑定、JSON 响应结构。

```java
@WebMvcTest(SysConfigController.class)
@Import(SystemTestApplication.class)   // ← 关键：见 §4
class SysConfigControllerTest {

    @Autowired
    private MockMvc mockMvc;

    @MockitoBean
    private ISysConfigService configService;   // 替换整个 Service

    @Test
    @DisplayName("GET /system/config/{id} 返回详情")
    void shouldReturnVoOnGetInfo() throws Exception {
        SysConfigVo vo = new SysConfigVo();
        vo.setConfigId(1L);
        when(configService.selectConfigById(anyLong())).thenReturn(vo);

        mockMvc.perform(get("/system/config/{id}", 1L))
            .andExpect(status().isOk())
            .andExpect(jsonPath("$.code").value(200))
            .andExpect(jsonPath("$.data.configId").value(1));
    }
}
```

**不覆盖**：
- `@SaCheckPermission` 权限拦截 — `@WebMvcTest` 不加载 SaToken 拦截器，留给集成测试或切面测试。
- `@RepeatSubmit` / `@Lock4j` / `@Log` AOP — 同上。
- `@Validated` 参数校验 — 简单场景可加 `MockMvc.addFilters()` 跑通，但默认不验证。

---

## 4 · 业务模块没启动类怎么办（关键坑）

`@WebMvcTest` / `@SpringBootTest` 会向上搜索 `@SpringBootConfiguration`。`ruoyi-admin` 是项目唯一启动类，业务模块（`ruoyi-modules/*`）的测试用它找不到根配置。

**解决方案**：每个需要 slice 测试的业务模块，在 `src/test/java/org/dromara/<模块>/` 下放一个桩启动类：

```java
// ruoyi-system/src/test/java/org/dromara/system/SystemTestApplication.java
@SpringBootApplication(scanBasePackages = "org.dromara.system")
@ConfigurationPropertiesScan(basePackages = "org.dromara.system")
public class SystemTestApplication {}
```

然后在 slice 测试上 `@Import(SystemTestApplication.class)`：

```java
@WebMvcTest(MyController.class)
@Import(SystemTestApplication.class)
class MyControllerTest { ... }
```

**为什么不用 `@SpringBootTest(classes = ...)`**：slice 注解（`@WebMvcTest` / `@DataJdbcTest`）自带必要的 autoconfig；再加全栈 `@SpringBootTest` 会启动 Redis/PG 等重型上下文，与"快速跑测试"目标相悖。

**为什么不让 `ruoyi-system` 依赖 `ruoyi-admin`**：依赖反向（admin 依赖 system），admin 模块是聚合入口，不是被依赖。

---

## 5 · 跑测试

### 5.1 跑全部

```bash
mvn test
```

跑完会生成报告：`ruoyi-system/target/surefire-reports/` 下 XML + TXT。

### 5.2 跑单个

```bash
mvn test -pl ruoyi-modules/ruoyi-system \
  -Dtest='SysConfigServiceLogicTest,SysConfigControllerTest' \
  -DfailIfNoTests=false
```

### 5.3 跑某个方法

```bash
mvn test -pl ruoyi-modules/ruoyi-system \
  -Dtest='SysConfigControllerTest#shouldReturnVoOnGetInfo'
```

### 5.4 跳过集成测试（默认就跳）

```bash
mvn test -DskipITs
```

---

## 6 · 接下来能做什么（路标）

P1 第一站最小样板已就位（3 文件 + 0 行 pom 改动不影响其他模块）。后续按需：

| 任务 | 说明 | 工作量 |
|---|---|---|
| 给其他 3 个核心 Service 各写 1 套测试 | 用户/角色/菜单 | 1-2 小时 |
| 集成测试骨架（`@SpringBootTest` + Testcontainers PG/Redis） | 验证 SQL/SaToken/缓存联动 | 半天 |
| CI：GitHub Actions 跑 `mvn test` | 提交即反馈 | 1 小时 |
| 静态检查：Spotless + Checkstyle | 代码风格门禁 | 半天 |

挑哪个进 P2 由你定。

---

## 7 · 版本

| 日期 | 变更 |
|---|---|
| 2026-10-13 | 首版（P1 配套：业务测试样板 + Spring Boot 4 模块拆坑记录） |
