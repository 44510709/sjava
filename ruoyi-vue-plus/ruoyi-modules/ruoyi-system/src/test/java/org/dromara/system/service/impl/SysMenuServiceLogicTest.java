package org.dromara.system.service.impl;

import org.dromara.system.domain.SysMenu;
import org.dromara.system.domain.vo.RouterVo;
import org.dromara.system.domain.vo.SysMenuVo;
import org.dromara.system.mapper.SysMenuMapper;
import org.dromara.system.mapper.SysRoleMapper;
import org.dromara.system.mapper.SysRoleMenuMapper;
import org.junit.jupiter.api.DisplayName;
import org.junit.jupiter.api.Test;
import org.junit.jupiter.api.extension.ExtendWith;
import org.mockito.InjectMocks;
import org.mockito.Mock;
import org.mockito.junit.jupiter.MockitoExtension;

import java.util.List;
import java.util.Set;

import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.junit.jupiter.api.Assertions.assertNotNull;
import static org.junit.jupiter.api.Assertions.assertTrue;
import static org.mockito.Mockito.when;

/**
 * SysMenuService 纯逻辑单元测试（无 Spring 上下文）。
 *
 * <p>覆盖绕过 {@code mapper.lambda()} 链式调用和
 * {@code LoginHelper.isSuperAdmin(...)} 静态判断的方法。
 *
 * <p><b>不覆盖的方法及原因：</b>
 * <ul>
 *   <li>{@code insertMenu}：{@code MapstructUtils.convert} 静态初始化依赖 Spring 容器</li>
 *   <li>{@code updateMenu}：同上</li>
 *   <li>{@code selectMenuList*}：依赖 {@code LoginHelper.isSuperAdmin} 静态调用 + 链式 lambda</li>
 *   <li>{@code selectMenuTreeByUserId}：同上 + 树构建，逻辑适合集成测试</li>
 *   <li>{@code hasChildByMenuId} / {@code checkMenuExistRole}：依赖 {@code mapper.lambda()}</li>
 *   <li>{@code checkMenuNameUnique} / {@code checkRouteConfigUnique}：同上 + 业务规则需真实数据</li>
 * </ul>
 */
@DisplayName("SysMenuService 纯逻辑单元测试")
@ExtendWith(MockitoExtension.class)
class SysMenuServiceLogicTest {

    @Mock
    private SysMenuMapper menuMapper;

    @Mock
    private SysRoleMapper roleMapper;

    @Mock
    private SysRoleMenuMapper roleMenuMapper;

    @InjectMocks
    private SysMenuServiceImpl menuService;

    @Test
    @DisplayName("按用户ID查权限：透传 mapper 的 Set<String>")
    void shouldReturnPermsSetFromMapper() {
        Set<String> expected = Set.of("system:user:list", "system:user:query");
        when(menuMapper.selectMenuPermsByUserId(1L)).thenReturn(expected);

        Set<String> actual = menuService.selectMenuPermsByUserId(1L);

        assertEquals(expected, actual);
        assertEquals(2, actual.size());
    }

    @Test
    @DisplayName("按菜单ID查详情：直接返回 mapper 的 VO 结果")
    void shouldReturnVoFromMapperWhenSelectById() {
        SysMenuVo vo = new SysMenuVo();
        vo.setMenuId(10L);
        vo.setMenuName("用户管理");
        when(menuMapper.selectVoById(10L)).thenReturn(vo);

        SysMenuVo actual = menuService.selectMenuById(10L);

        assertNotNull(actual);
        assertEquals(10L, actual.getMenuId());
        assertEquals("用户管理", actual.getMenuName());
    }

    @Test
    @DisplayName("删除菜单：透传 mapper.deleteById 的返回行数")
    void shouldReturnDeletedRowCount() {
        when(menuMapper.deleteById(10L)).thenReturn(1);

        int rows = menuService.deleteMenuById(10L);

        assertEquals(1, rows);
    }

    @Test
    @DisplayName("buildMenus 空列表：返回空列表")
    void shouldReturnEmptyListWhenBuildMenusInputEmpty() {
        List<RouterVo> actual = menuService.buildMenus(List.of());

        assertNotNull(actual);
        assertTrue(actual.isEmpty());
    }

    @Test
    @DisplayName("buildMenus 单个目录菜单：返回带 alwaysShow 的路由")
    void shouldBuildRouterForDirectoryMenu() {
        SysMenu dir = new SysMenu();
        dir.setMenuId(1L);
        dir.setMenuName("系统管理");
        dir.setMenuType("M"); // TYPE_DIR
        dir.setVisible("0");
        dir.setIsFrame("1"); // 否（不是内链）
        dir.setPath("/system");
        dir.setParentId(0L); // TOP_PARENT_ID
        dir.setComponent("Layout");
        dir.setOrderNum(1);

        List<RouterVo> routers = menuService.buildMenus(List.of(dir));

        assertEquals(1, routers.size());
        RouterVo router = routers.get(0);
        // path="/system" 经过 StringUtils.capitalize 后路由名以 / 开头
        assertEquals("/system" + dir.getMenuId(), router.getName());
        assertEquals("/system", router.getPath());
        assertEquals("Layout", router.getComponent());
        // visible="0" 表示显示 → hidden=false
        assertEquals(Boolean.FALSE, router.getHidden());
    }

    @Test
    @DisplayName("buildMenuTreeSelect 多层菜单：构建单根树（parent 折叠子节点）")
    void shouldBuildTreeForMenuList() {
        SysMenuVo parent = new SysMenuVo();
        parent.setMenuId(1L);
        parent.setParentId(0L);
        parent.setMenuName("系统管理");
        parent.setOrderNum(1);

        SysMenuVo child = new SysMenuVo();
        child.setMenuId(2L);
        child.setParentId(1L);
        child.setMenuName("用户管理");
        child.setOrderNum(1);

        List<cn.hutool.core.lang.tree.Tree<Long>> trees =
            menuService.buildMenuTreeSelect(List.of(parent, child));

        // TreeBuildUtils.build 把 child 挂到 parent 下，返回 1 个根节点
        assertEquals(1, trees.size());
        assertEquals(1L, trees.get(0).getId().longValue());
        assertEquals("系统管理", trees.get(0).getName());
    }
}
