package org.dromara.system.controller.system;

import org.dromara.common.core.domain.PageResult;
import org.dromara.system.SystemTestApplication;
import org.dromara.system.domain.bo.SysConfigBo;
import org.dromara.system.domain.vo.SysConfigVo;
import org.dromara.system.service.ISysConfigService;
import org.junit.jupiter.api.DisplayName;
import org.junit.jupiter.api.Test;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.webmvc.test.autoconfigure.WebMvcTest;
import org.springframework.context.annotation.Import;
import org.springframework.test.context.bean.override.mockito.MockitoBean;
import org.springframework.test.web.servlet.MockMvc;

import java.util.List;

import static org.mockito.ArgumentMatchers.any;
import static org.mockito.ArgumentMatchers.anyLong;
import static org.mockito.Mockito.when;
import static org.springframework.test.web.servlet.request.MockMvcRequestBuilders.get;
import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.jsonPath;
import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.status;

/**
 * SysConfigController 路由测试。
 *
 * <p>使用 {@link WebMvcTest} 仅加载 Controller 与其直接依赖，
 * 不引入 SaToken / Redis / PG 等重型上下文。{@link ISysConfigService}
 * 被 {@link MockitoBean} 完全替换。
 *
 * <p><b>覆盖目标：</b> 路由可达 + 参数绑定 + JSON 响应结构。
 * 权限注解（{@code @SaCheckPermission}）需要 SaToken 拦截器上下文，
 * 留给集成测试或切面测试覆盖。
 */
@DisplayName("SysConfigController 路由测试")
@WebMvcTest(SysConfigController.class)
@Import(SystemTestApplication.class)
class SysConfigControllerTest {

    @Autowired
    private MockMvc mockMvc;

    @MockitoBean
    private ISysConfigService configService;

    @Test
    @DisplayName("GET /system/config/list 返回分页结果")
    void shouldReturnPageResultOnList() throws Exception {
        SysConfigVo vo = new SysConfigVo();
        vo.setConfigId(1L);
        vo.setConfigKey("sys.test.key");
        PageResult<SysConfigVo> pageResult = new PageResult<>();
        pageResult.setRows(List.of(vo));
        pageResult.setTotal(1L);
        when(configService.selectPageConfigList(any(SysConfigBo.class), any())).thenReturn(pageResult);

        mockMvc.perform(get("/system/config/list"))
            .andExpect(status().isOk())
            .andExpect(jsonPath("$.code").value(200))
            .andExpect(jsonPath("$.data.total").value(1))
            .andExpect(jsonPath("$.data.rows[0].configKey").value("sys.test.key"));
    }

    @Test
    @DisplayName("GET /system/config/{id} 返回详情")
    void shouldReturnVoOnGetInfo() throws Exception {
        SysConfigVo vo = new SysConfigVo();
        vo.setConfigId(1L);
        vo.setConfigKey("sys.test.key");
        vo.setConfigValue("test-value");
        when(configService.selectConfigById(anyLong())).thenReturn(vo);

        mockMvc.perform(get("/system/config/{id}", 1L))
            .andExpect(status().isOk())
            .andExpect(jsonPath("$.code").value(200))
            .andExpect(jsonPath("$.data.configId").value(1))
            .andExpect(jsonPath("$.data.configValue").value("test-value"));
    }

    @Test
    @DisplayName("GET /system/config/configKey/{key} 返回字符串值")
    void shouldReturnStringValueOnGetByKey() throws Exception {
        when(configService.selectConfigByKey("sys.test.key")).thenReturn("test-value");

        mockMvc.perform(get("/system/config/configKey/{key}", "sys.test.key"))
            .andExpect(status().isOk())
            .andExpect(jsonPath("$.code").value(200))
            .andExpect(jsonPath("$.data").value("test-value"));
    }
}
