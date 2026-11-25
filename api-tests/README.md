# Chinese Poetry API 自动化测试

## 技术方案

- `pytest`：测试编排、fixture、参数化和标记
- `requests`：HTTP 客户端
- `openpyxl`：生成 Excel 测试用例文档
- 分层结构：`config/` 配置、`api/` 请求封装、`tests/` 测试用例、`data/` 用例数据、`reports/` 输出

## 运行环境

默认请求地址为 `http://localhost:1279`，要求 Docker 服务已启动。

```powershell
cd D:\AIcode\诗泉\chinese-poetry-api\api-tests
python -m pip install -r requirements.txt
pytest
```

切换服务地址：

```powershell
$env:POETRY_API_BASE_URL = "http://localhost:1279"
pytest -m smoke
```

运行指定范围：

```powershell
pytest -m "contract or negative"
pytest tests/test_poems.py -q
```

语义检索依赖服务端配置向量文件与 embedding API。未启用时对应测试会验证服务返回 `503` 并自动跳过，不会误报。

## 目录

```text
api-tests/
├── api/client.py
├── config/settings.py
├── data/testcases.json
├── reports/
├── tests/test_meta.py
├── tests/test_poems.py
├── tests/test_resources.py
├── conftest.py
├── pytest.ini
└── requirements.txt
```
