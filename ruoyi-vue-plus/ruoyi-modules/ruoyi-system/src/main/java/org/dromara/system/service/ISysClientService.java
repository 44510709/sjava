package org.dromara.system.service;

import org.dromara.system.domain.vo.SysClientVo;

/**
 * 客户端Service接口
 * <p>
 * 仅保留登录链路所需的客户端查询，客户端管理功能已移除（sys_client 表数据保留）。
 *
 * @author Michelle.Chung
 * @date 2023-06-18
 */
public interface ISysClientService {

    /**
     * 查询客户端信息基于客户端id
     */
    SysClientVo queryByClientId(String clientId);

}
