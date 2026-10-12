package org.dromara.system.service.impl;

import lombok.RequiredArgsConstructor;
import org.dromara.common.core.constant.CacheNames;
import org.dromara.system.domain.SysClient;
import org.dromara.system.domain.vo.SysClientVo;
import org.dromara.system.mapper.SysClientMapper;
import org.dromara.system.service.ISysClientService;
import org.springframework.cache.annotation.Cacheable;
import org.springframework.stereotype.Service;

/**
 * 客户端Service业务层处理
 * <p>
 * 仅保留登录链路所需的客户端查询，客户端管理（列表/新增/修改/删除/导出）已移除。
 *
 * @author Michelle.Chung
 * @date 2023-06-18
 */
@RequiredArgsConstructor
@Service
public class SysClientServiceImpl implements ISysClientService {

    private final SysClientMapper clientMapper;

    /**
     * 查询客户端信息基于客户端id
     *
     * @param clientId 客户端标识
     * @return 客户端详情
     */
    @Cacheable(cacheNames = CacheNames.SYS_CLIENT, key = "#clientId")
    @Override
    public SysClientVo queryByClientId(String clientId) {
        return clientMapper.lambda().eq(SysClient::getClientId, clientId).voOne();
    }

}
