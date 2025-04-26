# GitHub Trending MCP

这是一个基于 FastMCP 框架的 GitHub 热门仓库获取工具，可以一次性获取 GitHub 当日的可选个数的热门仓库的详细信息，包括名称、链接、描述和 README 内容。
这样你就不用一篇一篇的翻README来总结博客了，可以节省AI 的 Prompt 。

## 功能特点

- 获取 GitHub 当日热门仓库列表
- 支持自定义获取仓库数量
- 支持代理配置（通过环境变量）
- 支持将结果保存为 Markdown 文件
- 自动处理同名文件，避免覆盖
- 提供完整的进度报告和日志记录

## 安装方法

### 从仓库安装

```bash
# 使用pip从GitHub仓库安装
pip install git+https://github.com/RusianHu/GitHubDailyTrendingFetcher-mcp.git
```

### 从本地安装

```bash
# 克隆仓库
git clone https://github.com/RusianHu/GitHubDailyTrendingFetcher-mcp.git
cd GitHubDailyTrendingFetcher-mcp

# 安装到本地环境
pip install -e .
```

## 使用方法

### 作为命令行工具运行

安装后，可以直接在命令行中运行：

```bash
# 使用 Python 模块方式运行（推荐）
python -m github_trending_mcp
```

### 作为 MCP 服务集成到 Roo Code

1. 打开 Roo Code 的 MCP 配置文件：
   ```
   %APPDATA%\Code\User\globalStorage\rooveterinaryinc.roo-cline\settings\mcp_settings.json
   ```

2. 添加 GitHub Trending MCP 服务配置：
   ```json
   {
     "mcpServers": {
       // 其他服务配置...
       "github-trending-mcp": {
         "command": "python",
         "args": [
           "-m",
           "github_trending_mcp"
         ],
         "alwaysAllow": [
           "get_github_trending",
           "get_proxy_status"
         ],
         "disabled": false
       }
     }
   }
   ```

3. 保存配置文件并重启 Roo Code

## 环境变量配置

可以通过以下环境变量配置代理：

- `PROXY_HOST`: 代理主机地址（默认为 "127.0.0.1"）
- `PROXY_PORT`: 代理端口（默认为 "10808"）
- `PROXY_PROTOCOL`: 代理协议（默认为 "socks5"）

### 设置环境变量示例

**Windows PowerShell**：
```powershell
$env:PROXY_HOST = "127.0.0.1"
$env:PROXY_PORT = "10808"
$env:PROXY_PROTOCOL = "socks5"
```

**Windows CMD**：
```cmd
set PROXY_HOST=127.0.0.1
set PROXY_PORT=10808
set PROXY_PROTOCOL=socks5
```

**Linux/macOS**：
```bash
export PROXY_HOST=127.0.0.1
export PROXY_PORT=10808
export PROXY_PROTOCOL=socks5
```

### 在 Roo Code MCP 配置中使用环境变量

```json
{
  "mcpServers": {
    "github-trending-mcp": {
      "command": "python",
      "args": [
        "-m",
        "github_trending_mcp"
      ],
      "env": {
        "PROXY_HOST": "127.0.0.1",
        "PROXY_PORT": "10808",
        "PROXY_PROTOCOL": "socks5"
      },
      "alwaysAllow": [
        "get_github_trending",
        "get_proxy_status"
      ],
      "disabled": false
    }
  }
}
```

### 在 Python 代码中设置环境变量

```python
import os

# 设置环境变量
os.environ["PROXY_HOST"] = "127.0.0.1"
os.environ["PROXY_PORT"] = "10808"
os.environ["PROXY_PROTOCOL"] = "socks5"

# 然后运行或导入 github_trending_mcp
import github_trending_mcp

# 运行 MCP 服务（推荐方式是使用 python -m github_trending_mcp 命令）
github_trending_mcp.run()

# 或者直接调用工具函数（需要自己处理异步）
import asyncio
from fastmcp import Context

async def main():
    ctx = Context()
    request = github_trending_mcp.TrendingRequest(
        repo_limit=5,
        use_proxy=True,
        save_to_file=True
    )
    result = await github_trending_mcp.get_github_trending(request, ctx)
    print(result)

asyncio.run(main())
```

## API 参考

### 工具：get_github_trending

获取 GitHub 当日热门仓库，包括名称、链接、描述和 README 内容。

**参数：**
- `repo_limit`: 要获取的仓库数量，默认为 5
- `use_proxy`: 是否使用代理，默认为 False
- `save_to_file`: 是否保存结果到文件，默认为 True

**返回：**
- Markdown 格式的热门仓库信息

**示例调用：**
```json
{
  "repo_limit": 10,
  "use_proxy": true,
  "save_to_file": true
}
```

### 工具：get_proxy_status

获取当前代理配置状态。

**参数：** 无

**返回：**
- 包含代理配置信息的字典

## 输出示例

下面是一个输出示例：

```
## GitHub 今日热门仓库 Top 5

### 1. [username/repo-name](https://github.com/username/repo-name)
**About:** 仓库描述信息
**README:**
​```markdown
README 内容...
​```

### 2. [username2/repo-name2](https://github.com/username2/repo-name2)
**About:** 仓库描述信息
**README:**
​```markdown
README 内容...
​```

---
**总输出文本长度:** 12345

报告已保存到: C:\path\to\github_trending_2023-05-01.md
```

> 注意：实际输出中的代码块会正确显示，这里为了展示嵌套的代码块而做了特殊处理。

## 文件保存

结果将保存为 Markdown 文件，文件名格式为：
- `github_trending_YYYY-MM-DD.md`

如果同名文件已存在，将自动添加序号：
- `github_trending_YYYY-MM-DD_1.md`
- `github_trending_YYYY-MM-DD_2.md`
- ...

## 注意事项

1. 确保网络连接正常，或配置正确的代理
2. GitHub 页面结构可能会变化，如果遇到解析错误，可能需要更新解析逻辑
3. 请遵守 GitHub 的使用条款和爬虫政策

## 许可证

[MIT](LICENSE) © RusianHu
