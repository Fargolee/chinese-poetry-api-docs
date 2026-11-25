# REST API 接口测试用例文档

## 测试对象

- 服务：Chinese Poetry API
- 规范：`openapi.yaml`，OpenAPI 3.2.0
- 基础地址：`http://localhost:1279`
- 接口范围：13 个 REST endpoint

## 技术方案

- 自动化框架：`pytest`
- HTTP 客户端：`requests`
- 测试数据与用例源：`api-tests/data/testcases.json`
- Excel 交付物：`rest-api-test-cases.xlsx`
- 执行报告：`api-tests/reports/junit.xml`

## 覆盖范围

| 模块 | 覆盖内容 | 用例数 |
|---|---|---:|
| 服务元数据 | 健康检查、统计信息、OpenAPI 文档 | 3 |
| 诗词列表 | 默认/繁体、作者/朝代/体裁过滤、页码分页、游标分页、边界值 | 9 |
| 诗词搜索 | 关键词、朝代、搜索范围、缺失参数、非法参数 | 4 |
| 语义检索 | 启用时返回结果、未启用时 503 降级 | 1 |
| 随机诗词 | 默认、作者、体裁、分类、朝代、飞花令、组合过滤、互斥参数 | 7 |
| 作者 | 列表、详情、不存在资源 | 3 |
| 朝代 | 列表、详情、不存在资源 | 2 |
| 体裁 | 列表、详情、不存在资源 | 2 |
| **合计** | **正向、契约、边界、异常和降级场景** | **32** |

## 优先级

- `P0`：健康检查、统计、诗词列表、关键词搜索、随机诗词等核心可用性。
- `P1`：过滤、分页、资源详情、参数校验、错误响应和语义检索。

## 交付文件

- [Excel 测试用例](./rest-api-test-cases.xlsx)
- [机器可读用例 JSON](./api-tests/data/testcases.json)
- [Python 自动化测试项目](./api-tests/README.md)
- [JUnit 执行报告](./api-tests/reports/junit.xml)
