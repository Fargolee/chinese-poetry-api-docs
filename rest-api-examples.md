# 中国古诗词 REST API 调用示例

服务地址：`http://localhost:1279`

所有 REST 接口的基础路径为：`/api/v1`。

## 健康与统计

### 健康检查

```bash
curl "http://localhost:1279/api/v1/health"
```

### 统计信息

```bash
curl "http://localhost:1279/api/v1/stats"
```

## 诗词列表

### 简体中文（默认）

```bash
curl "http://localhost:1279/api/v1/poems"
```

### 繁体中文

```bash
curl "http://localhost:1279/api/v1/poems?lang=zh-Hant"
```

### 按朝代过滤

```bash
curl "http://localhost:1279/api/v1/poems?dynasty=唐"
```

### 按作者过滤并分页

```bash
curl "http://localhost:1279/api/v1/poems?author=李白&page=2&page_size=50"
```

### 按 ID 过滤

多个 `type_id` 为“或”关系。

```bash
curl "http://localhost:1279/api/v1/poems?dynasty_id=1&type_id=11&type_id=12"
```

### 游标翻页

将上一页响应中 `pagination.next_cursor` 的值传给 `after`。

```bash
curl "http://localhost:1279/api/v1/poems?page_size=50&after=cG9lbTo0MjA"
```

## 搜索诗词

搜索结果按相关度排序。

### 关键词搜索

```bash
curl "http://localhost:1279/api/v1/poems/search?q=静夜思"
```

### 在指定朝代内搜索

也可以使用 `dynasty_id`；排序规则与不限朝代时一致。

```bash
curl "http://localhost:1279/api/v1/poems/search?q=月&dynasty=唐"
```

### 语义检索

服务端必须启用语义检索功能。

```bash
curl "http://localhost:1279/api/v1/poems/semantic?q=下雪天一个老人独自在小船上钓鱼&limit=10"
```

## 随机诗词

### 随机获取一首

```bash
curl "http://localhost:1279/api/v1/poems/random"
```

### 按作者过滤

```bash
curl "http://localhost:1279/api/v1/poems/random?author=李白"
```

### 按体裁过滤

```bash
curl "http://localhost:1279/api/v1/poems/random?type=五言绝句"
```

### 按分类和朝代过滤

“唐诗”等分类名涵盖该分类下的多个体裁，例如五言绝句、七言律诗等。

```bash
curl "http://localhost:1279/api/v1/poems/random?type=唐诗&dynasty=唐"
```

### 按单字随机获取（飞花令）

`char` 场景只能搭配 `lang`，不能与作者、体裁或朝代过滤同时使用。

```bash
curl "http://localhost:1279/api/v1/poems/random?char=春"
```

### 组合过滤

```bash
curl "http://localhost:1279/api/v1/poems/random?author=李白&type=五言绝句"
curl "http://localhost:1279/api/v1/poems/random?author=李白&type=五言绝句&dynasty=唐"
curl "http://localhost:1279/api/v1/poems/random?author=李白&dynasty=唐&type=五言绝句&type=七言绝句&type=五言律诗"
```

## 作者

### 作者列表

```bash
curl "http://localhost:1279/api/v1/authors?page=1&page_size=20"
```

### 作者详情

```bash
curl "http://localhost:1279/api/v1/authors/1"
```

## 朝代

### 朝代列表

```bash
curl "http://localhost:1279/api/v1/dynasties"
```

### 朝代详情

```bash
curl "http://localhost:1279/api/v1/dynasties/1"
```

## 诗词体裁

### 体裁列表

```bash
curl "http://localhost:1279/api/v1/types"
```

### 体裁详情

```bash
curl "http://localhost:1279/api/v1/types/10"
```

## 相关文档

- [OpenAPI 规范](./openapi.yaml)
- [交互式 REST API 文档](./rest-api.html)

