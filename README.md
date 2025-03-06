# CatCat 插件

CatCat 是一个用于 Ncatbot 的插件，提供了群聊消息的自动回复功能。

## 功能

- 自动回复群聊消息
- 兼容回调函数注册
- 支持自定义回复内容

## 安装

1. 将 CatCat 插件文件夹放置在 `ncatbot/plugins` 目录下。
2. 确保在 `ncatbot/plugins/CatCat/config` 目录下存在以下配置文件：
   - `config.yaml`：包含 API 密钥等配置信息
   - `cat_prompt.txt`：包含自定义回复提示内容

## 配置

在 `config/config.yaml` 文件中，添加以下内容：

```yaml
api_key: "your_api_key_here"
```

在 `cat_prompt.txt` 文件中，添加自定义的回复提示内容。

## 使用

1. 启动 Ncatbot。
2. 在群聊中发送消息，CatCat 插件会根据配置自动回复消息。
3. 发送 `测试CatCat` 消息以测试插件是否正常工作。


## 贡献

欢迎 [提交问题](https://github.com/IppClub/ncatbot-catcat/issues) 和 [贡献代码](https://github.com/IppClub/ncatbot-catcat/pulls) ！

## 许可证

此项目基于 MIT 许可证。