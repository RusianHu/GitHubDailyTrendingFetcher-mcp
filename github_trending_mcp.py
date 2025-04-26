import requests
from bs4 import BeautifulSoup
import time
import os
from datetime import datetime
from typing import Dict, List, Optional, Union
from pydantic import BaseModel, Field
import json
from fastmcp import FastMCP, Context

# 创建 FastMCP 服务实例
mcp = FastMCP(name="GitHub Trending MCP")

# 保存文件开关 - 设置为 True 即启用 结果保存到本地文件的功能，False 禁用保存
SAVE_TO_FILE = True

# 从环境变量获取代理配置
def get_proxy_config():
    """从环境变量获取代理配置"""
    proxy_host = os.environ.get("PROXY_HOST", "127.0.0.1")
    proxy_port = os.environ.get("PROXY_PORT", "10808")
    proxy_protocol = os.environ.get("PROXY_PROTOCOL", "socks5")
    
    return {
        'http': f'{proxy_protocol}://{proxy_host}:{proxy_port}',
        'https': f'{proxy_protocol}://{proxy_host}:{proxy_port}'
    }

# 定义请求模型
class TrendingRequest(BaseModel):
    repo_limit: int = Field(default=5, description="要获取的仓库数量")
    use_proxy: bool = Field(default=False, description="是否使用代理")
    save_to_file: bool = Field(default=True, description="是否保存结果到文件")

# 定义仓库模型
class Repository(BaseModel):
    name: str
    link: str
    about: str
    readme: str = ""

@mcp.tool()
async def get_github_trending(request: TrendingRequest, ctx: Context) -> str:
    """
    获取 GitHub 当日热门仓库，包括名称、链接、描述和README内容。
    
    参数:
    - repo_limit: 要获取的仓库数量，默认为5
    - use_proxy: 是否使用代理，默认为False
    - save_to_file: 是否保存结果到文件，默认为True
    
    返回:
    - Markdown 格式的热门仓库信息
    """
    # 记录开始
    await ctx.info(f"开始获取 GitHub 热门仓库，数量: {request.repo_limit}，代理状态: {'启用' if request.use_proxy else '禁用'}")
    
    # 获取代理配置
    proxy_config = get_proxy_config() if request.use_proxy else None
    
    # 获取仓库列表
    await ctx.info("正在获取仓库列表...")
    repositories = await get_trending_repositories(request.repo_limit, proxy_config, ctx)
    
    # 生成输出内容
    output_content = f"## GitHub 今日热门仓库 Top {request.repo_limit}\n\n"
    
    if not repositories:
        await ctx.warning("无法获取热门仓库信息")
        output_content += "无法获取热门仓库信息。\n"
    else:
        await ctx.info(f"找到 {len(repositories)} 个仓库，正在获取 README...")
        
        # 获取每个仓库的 README
        for i, repo in enumerate(repositories):
            await ctx.info(f"正在获取 {repo['name']} 的 README ({i+1}/{len(repositories)})...")
            await ctx.report_progress(progress=i, total=len(repositories))
            
            # 加入一点延迟避免请求过快
            time.sleep(1)
            readme = await get_readme_content(repo['link'], proxy_config, ctx)
            
            # 添加到输出内容
            output_content += f"### {i+1}. [{repo['name']}]({repo['link']})\n"
            output_content += f"**About:** {repo['about']}\n"
            output_content += "**README:**\n```markdown\n"
            output_content += readme + "\n"
            output_content += "```\n\n"
        
        # 完成进度报告
        await ctx.report_progress(progress=len(repositories), total=len(repositories))
    
    # 添加输出长度信息
    output_length = len(output_content)
    output_content += f"---\n**总输出文本长度:** {output_length}"
    
    # 保存到文件
    if request.save_to_file:
        file_path = await save_to_file(output_content, ctx)
        output_content += f"\n\n报告已保存到: {file_path}"
    
    await ctx.info("GitHub 热门仓库获取完成")
    return output_content

async def get_trending_repositories(limit: int, proxies: Optional[Dict[str, str]], ctx: Context) -> List[Dict[str, str]]:
    """获取 GitHub Trending 仓库列表"""
    url = "https://github.com/trending"
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }
    try:
        await ctx.debug(f"请求 URL: {url}")
        response = requests.get(url, headers=headers, timeout=10, proxies=proxies)
        response.raise_for_status()  # 检查请求是否成功
        
        soup = BeautifulSoup(response.text, 'html.parser')
        repo_list = soup.find_all('article', class_='Box-row')
        
        repositories = []
        for i, repo_element in enumerate(repo_list):
            if i >= limit:
                break
            try:
                # 获取名称和链接
                title_element = repo_element.find('h2', class_='h3')
                if not title_element:
                    title_element = repo_element.find('h1', class_='h3')  # 兼容旧版或不同布局
                
                if title_element and title_element.find('a'):
                    a_tag = title_element.find('a')
                    repo_name = a_tag.text.strip().replace('\n', '').replace('  ', ' ')
                    repo_link_relative = a_tag['href']
                    repo_link = f"https://github.com{repo_link_relative}"
                else:
                    continue  # 跳过无法解析名称和链接的条目
                
                # 获取 About 描述
                about_element = repo_element.find('p', class_='col-9')
                repo_about = about_element.text.strip() if about_element else "N/A"
                
                repositories.append({
                    'name': repo_name,
                    'link': repo_link,
                    'about': repo_about
                })
            except Exception as e:
                await ctx.error(f"解析仓库 {i+1} 时出错: {e}")
                continue  # 解析单个仓库出错时继续下一个
        
        return repositories
    
    except requests.exceptions.RequestException as e:
        await ctx.error(f"获取热门页面时出错: {e}")
        return []
    except Exception as e:
        await ctx.error(f"解析热门页面时发生意外错误: {e}")
        return []

async def get_readme_content(repo_link: str, proxies: Optional[Dict[str, str]], ctx: Context) -> str:
    """获取仓库的 README 内容"""
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }
    try:
        # 请求仓库主页
        await ctx.debug(f"请求仓库页面: {repo_link}")
        response = requests.get(repo_link, headers=headers, timeout=15, proxies=proxies)
        response.raise_for_status()
        
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # 查找 README 区域 (GitHub 结构可能变化，需要适配)
        # 尝试多种可能的选择器
        readme_element = soup.find('div', id='readme')  # 优先查找 ID
        if not readme_element:
            readme_element = soup.find('article', class_='markdown-body')  # 查找 Markdown 主体
        
        if readme_element:
            # 尝试提取 Markdown 原文或纯文本
            readme_text = readme_element.get_text(separator='\n', strip=True)
            return readme_text if readme_text else "README content not found or empty."
        else:
            # 尝试查找 README 文件链接，然后获取其原始内容
            readme_file_link_element = soup.find('a', title=lambda t: t and t.lower().startswith('readme'))
            if readme_file_link_element:
                readme_file_url = f"https://github.com{readme_file_link_element['href']}"
                # 为了简化，这里返回提示信息
                return f"README found as file, check: {readme_file_url}"
            else:
                return "README section not found."
    
    except requests.exceptions.RequestException as e:
        await ctx.error(f"从 {repo_link} 获取 README 时出错: {e}")
        return f"Error fetching README from {repo_link}: {e}"
    except Exception as e:
        await ctx.error(f"从 {repo_link} 获取 README 时发生意外错误: {e}")
        return f"An unexpected error occurred while fetching README from {repo_link}: {e}"

async def save_to_file(content: str, ctx: Context) -> str:
    """保存内容到文件"""
    try:
        # 生成带有日期的文件名
        current_date = datetime.now().strftime("%Y-%m-%d")
        base_file_name = f"github_trending_{current_date}.md"
        # 获取脚本所在目录的路径
        script_dir = os.path.dirname(os.path.abspath(__file__))
        
        # 处理同名文件
        file_path = os.path.join(script_dir, base_file_name)
        counter = 1
        
        # 如果文件已存在，则添加序号
        while os.path.exists(file_path):
            file_name = f"github_trending_{current_date}_{counter}.md"
            file_path = os.path.join(script_dir, file_name)
            counter += 1
        
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(content)
        
        await ctx.info(f"报告已保存到: {file_path}")
        return file_path
    
    except Exception as e:
        await ctx.error(f"保存报告到文件时出错: {e}")
        return f"保存文件失败: {e}"

@mcp.tool()
async def get_proxy_status() -> Dict[str, Union[bool, Dict[str, str]]]:
    """
    获取当前代理配置状态
    
    返回:
    - 包含代理配置信息的字典
    """
    proxy_config = get_proxy_config()
    return {
        "proxy_available": True,
        "proxy_config": proxy_config
    }

# 主程序入口
if __name__ == "__main__":
    mcp.run()
