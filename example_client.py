"""
GitHub Trending MCP 客户端示例
"""
import asyncio
from fastmcp import Client

async def main():
    # 创建 MCP 客户端
    # 使用 Python 模块方式运行
    client = Client("python -m github_trending_mcp")

    # 连接到服务
    await client.connect()

    try:
        # 获取代理状态
        proxy_status = await client.invoke("get_proxy_status")
        print("代理状态:", proxy_status)

        # 调用主要工具获取 GitHub 热门仓库
        # 这里我们获取前 3 个仓库，启用代理，并保存到文件
        result = await client.invoke(
            "get_github_trending",
            {
                "repo_limit": 3,
                "use_proxy": True,
                "save_to_file": True
            }
        )

        # 打印结果
        print("\n获取结果:")
        print(result)

    finally:
        # 关闭连接
        await client.close()

if __name__ == "__main__":
    asyncio.run(main())
