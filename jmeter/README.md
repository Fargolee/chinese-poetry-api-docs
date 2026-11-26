# JMeter 性能测试

测试计划：`chinese-poetry-api.jmx`

覆盖接口：健康检查、诗词列表、朝代过滤、关键词搜索、随机诗词、作者列表、朝代列表、体裁列表。

## GUI 调试

```powershell
jmeter -t chinese-poetry-api.jmx
```

默认地址为 `http://localhost:1279`，可在 JMeter 的 User Defined Variables 中修改 `host`、`port` 和 `protocol`。

## 非 GUI 运行

建议正式压测使用非 GUI 模式：

```powershell
jmeter -n `
  -t chinese-poetry-api.jmx `
  -Jthreads=20 `
  -Jramp_up=60 `
  -Jloops=100 `
  -Jduration=600 `
  -l results.jtl `
  -e `
  -o report
```

参数说明：

| 参数 | 默认值 | 说明 |
|---|---:|---|
| `threads` | 5 | 并发线程数 |
| `ramp_up` | 30 | 启动线程所需秒数 |
| `loops` | 10 | 每个线程循环次数 |
| `duration` | 300 | 调度持续时间，单位秒 |
| `delay` | 0 | 启动延迟，单位秒 |

打开报告：

```text
report/index.html
```

## 注意事项

- 服务默认限流为 `10 RPS`、突发 `20`；压测收到 `429` 时应单独统计，不要直接当作服务端 5xx 故障。
- 先运行低并发基线，再逐步提高 `threads`，同时观察 P95/P99、错误率、CPU、内存和容器重启。
- 语义检索依赖 embedding 服务，建议单独建立测试计划，避免外部依赖延迟影响普通接口结论。
- `results.jtl`、`report/` 等运行产物不应提交到 Git。
