package org.dromara.system.controller.system;

import org.dromara.system.SystemTestApplication;
import org.dromara.system.domain.vo.SysMenuVo;
import org.dromara.system.service.ISysMenuService;
import org.junit.jupiter.api.DisplayName;
import org.junit.jupiter.api.Test;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.webmvc.test.autoconfigure.WebMvcTest;
import org.springframework.context.annotation.Import;
import org.springframework.test.context.bean.override.mockito.MockitoBean;
import org.springframework.test.web.servlet.MockMvc;

import static org.mockito.ArgumentMatchers.anyLong;
import static org.mockito.Mockito.when;
import static org.springframework.test.web.servlet.request.MockMvcRequestBuilders.get;
import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.jsonPath;
import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.status;

/**
 * SysMenuController 路由测试。
 *
 * <p>参考 {@code SysConfigControllerTest} 的样板，演示
 * {@code @WebMvcTest} + {@code @MockitoBean} 在第二个 controller 上的复用性。
 */
@DisplayName("SysMenuController 路由测试")
@WebMvcTest(SysMenuController.class)
@Import(SystemTestApplication.class)
class SysMenuControllerTest {

    @Autowired
    private MockMvc mockMvc;

    @MockitoBean
    private ISysMenuService menuService;

    @Test
    @DisplayName("GET /system/menu/{id} 返回详情")
    void shouldReturnVoOnGetInfo() throws Exception {
        SysMenuVo vo = new SysMenuVo();
        vo.setMenuId(10L);
        vo.setMenuName("用户管理");
        when(menuService.selectMenuById(anyLong())).thenReturn(vo);

        mockMvc.perform(get("/system/menu/{id}", 10L))
            .andExpect(status().isOk())
            .andExpect(jsonPath("$.code").value(200))
            .andExpect(jsonPath("$.data.menuId").value(10))
            .andExpect(jsonPath("$.data.menuName").value("用户管理"));
    }
}
