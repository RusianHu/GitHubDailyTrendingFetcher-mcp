from setuptools import setup, find_packages

setup(
    name="github-trending-mcp",
    version="1.0.0",
    description="GitHub Trending MCP - 获取 GitHub 热门仓库的 MCP 服务",
    author="RusianHu",
    author_email="hu_bo_cheng@qq.com",
    packages=find_packages(),
    install_requires=[
        "fastmcp>=0.1.0",
        "aiohttp>=3.8.0",
        "beautifulsoup4>=4.9.3",
        "pydantic>=1.8.0",
    ],
    entry_points={
        "console_scripts": [
            "github-trending-mcp=github_trending_mcp:run",
        ],
    },
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
    ],
    python_requires=">=3.8",
)
