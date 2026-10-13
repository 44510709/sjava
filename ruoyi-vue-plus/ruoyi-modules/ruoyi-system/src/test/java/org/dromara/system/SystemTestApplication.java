package org.dromara.system;

import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;
import org.springframework.boot.context.properties.ConfigurationPropertiesScan;

/**
 * 业务模块测试专用启动桩。
 *
 * <p>{@code ruoyi-modules/ruoyi-system} 模块本身没有启动类（启动类在 {@code ruoyi-admin}），
 * {@code @SpringBootTest} / {@code @WebMvcTest} 默认会向上搜索 {@code @SpringBootConfiguration}，
 * 找不到就会报错。本类作为 {@code src/test/java} 下的桩，提供 slice 注解所需的 root config。
 *
 * <p>生产代码不会引用本类；{@code src/test/java} 不进入最终 jar。
 */
@SpringBootApplication(scanBasePackages = "org.dromara.system")
@ConfigurationPropertiesScan(basePackages = "org.dromara.system")
public class SystemTestApplication {

    /**
     * 不调用，桩类无需启动逻辑。
     */
    public static void main(String[] args) {
        // 仅作为 Spring Boot 配置类的载体，不真的启动。
        SpringApplication.run(SystemTestApplication.class, args);
    }
}
