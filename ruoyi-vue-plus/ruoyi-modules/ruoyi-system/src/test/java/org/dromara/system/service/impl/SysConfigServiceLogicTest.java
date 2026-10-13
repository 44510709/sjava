package org.dromara.system.service.impl;

import com.baomidou.mybatisplus.core.conditions.query.LambdaQueryWrapper;
import com.baomidou.mybatisplus.extension.plugins.pagination.Page;
import org.dromara.common.core.domain.PageResult;
import org.dromara.common.mybatis.core.page.PageQuery;
import org.dromara.system.domain.bo.SysConfigBo;
import org.dromara.system.domain.vo.SysConfigVo;
import org.dromara.system.mapper.SysConfigMapper;
import org.junit.jupiter.api.DisplayName;
import org.junit.jupiter.api.Test;
import org.junit.jupiter.api.extension.ExtendWith;
import org.mockito.InjectMocks;
import org.mockito.Mock;
import org.mockito.junit.jupiter.MockitoExtension;

import java.util.List;

import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.junit.jupiter.api.Assertions.assertNotNull;
import static org.mockito.ArgumentMatchers.any;
import static org.mockito.Mockito.when;

/**
 * SysConfigService 纯逻辑单元测试（无 Spring 上下文）。
 *
 * <p>本测试只覆盖不依赖 MyBatis-Plus {@code mapper.lambda()} 链式调用、
 * 也未被 {@code @Cacheable} / {@code @CachePut} 包裹的方法。
 * 涉及缓存的方法需要在 {@code @SpringBootTest} 中集成测试。
 *
 * <p><b>为什么不用 @SpringBootTest：</b> 启动整个容器需要 PG/Redis，
 * 不适合做模块级脚手架。集成测试留给后续或 Testcontainers（待规划）。
 */
@DisplayName("SysConfigService 纯逻辑单元测试")
@ExtendWith(MockitoExtension.class)
class SysConfigServiceLogicTest {

    @Mock
    private SysConfigMapper configMapper;

    @InjectMocks
    private SysConfigServiceImpl service;

    @Test
    @DisplayName("按 ID 查询：直接返回 mapper 的 VO 结果")
    void shouldReturnVoFromMapperWhenSelectById() {
        SysConfigVo expected = new SysConfigVo();
        expected.setConfigId(1L);
        expected.setConfigKey("sys.test.key");
        when(configMapper.selectVoById(1L)).thenReturn(expected);

        SysConfigVo actual = service.selectConfigById(1L);

        assertNotNull(actual);
        assertEquals(1L, actual.getConfigId());
        assertEquals("sys.test.key", actual.getConfigKey());
    }

    @Test
    @DisplayName("列表查询：透传 mapper 的 VO 列表")
    void shouldReturnListFromMapperWhenSelectConfigList() {
        SysConfigBo bo = new SysConfigBo();
        bo.setConfigName("测试");
        SysConfigVo vo = new SysConfigVo();
        vo.setConfigName("测试");
        when(configMapper.selectVoList(any(LambdaQueryWrapper.class))).thenReturn(List.of(vo));

        List<SysConfigVo> list = service.selectConfigList(bo);

        assertEquals(1, list.size());
        assertEquals("测试", list.get(0).getConfigName());
    }

    @Test
    @DisplayName("分页查询：把 Page 转为 PageResult")
    void shouldConvertPageToPageResult() {
        SysConfigBo bo = new SysConfigBo();
        PageQuery pageQuery = new PageQuery();
        Page<SysConfigVo> mockPage = new Page<>(1, 10);
        mockPage.setRecords(List.of(new SysConfigVo()));
        mockPage.setTotal(1L);
        when(configMapper.selectVoPage(any(), any(LambdaQueryWrapper.class))).thenReturn(mockPage);

        PageResult<SysConfigVo> result = service.selectPageConfigList(bo, pageQuery);

        assertNotNull(result);
        assertEquals(1L, result.getTotal());
        assertEquals(1, result.getRows().size());
    }
}
