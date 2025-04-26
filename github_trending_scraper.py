import requests
from bs4 import BeautifulSoup
import time
import os
from datetime import datetime

# 代理开关 - 设置为 True 启用代理，False 禁用代理
USE_PROXY = False

# 保存文件开关 - 设置为 True 即启用 结果保存到本地文件的功能，False 禁用保存
SAVE_TO_FILE = True

# 代理配置 - 当 USE_PROXY 为 True 时使用
PROXY_CONFIG = {
    'http': 'socks5://127.0.0.1:10808',
    'https': 'socks5://127.0.0.1:10808'
}

# 全局变量：要获取的仓库数量
REPO_LIMIT = 5

def get_trending_repositories(limit=REPO_LIMIT):
    """获取 GitHub Trending 仓库列表"""
    url = "https://github.com/trending"
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }
    try:
        # 根据代理开关决定是否使用代理
        proxies = PROXY_CONFIG if USE_PROXY else None
        response = requests.get(url, headers=headers, timeout=10, proxies=proxies)
        response.raise_for_status() # 检查请求是否成功
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
                    title_element = repo_element.find('h1', class_='h3') # 兼容旧版或不同布局

                if title_element and title_element.find('a'):
                    a_tag = title_element.find('a')
                    repo_name = a_tag.text.strip().replace('\n', '').replace('  ', ' ')
                    repo_link_relative = a_tag['href']
                    repo_link = f"https://github.com{repo_link_relative}"
                else:
                    continue # 跳过无法解析名称和链接的条目

                # 获取 About 描述
                about_element = repo_element.find('p', class_='col-9')
                repo_about = about_element.text.strip() if about_element else "N/A"

                repositories.append({
                    'name': repo_name,
                    'link': repo_link,
                    'about': repo_about
                })
            except Exception as e:
                print(f"Error parsing repository {i+1}: {e}")
                continue # 解析单个仓库出错时继续下一个

        return repositories

    except requests.exceptions.RequestException as e:
        print(f"Error fetching trending page: {e}")
        return []
    except Exception as e:
        print(f"An unexpected error occurred while parsing trending page: {e}")
        return []


def get_readme_content(repo_link):
    """获取仓库的 README 内容"""
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }
    try:
        # 请求仓库主页
        # 根据代理开关决定是否使用代理
        proxies = PROXY_CONFIG if USE_PROXY else None
        response = requests.get(repo_link, headers=headers, timeout=15, proxies=proxies)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')

        # 查找 README 区域 (GitHub 结构可能变化，需要适配)
        # 尝试多种可能的选择器
        readme_element = soup.find('div', id='readme') # 优先查找 ID
        if not readme_element:
            readme_element = soup.find('article', class_='markdown-body') # 查找 Markdown 主体

        if readme_element:
            # 尝试提取 Markdown 原文或纯文本
            # 这里简单提取整个区域的文本，可能包含非 README 内容，精确提取较复杂
            readme_text = readme_element.get_text(separator='\n', strip=True)
            # 如果需要 Markdown 原文，解析逻辑会更复杂
            # readme_markdown = str(readme_element) # 获取 HTML 结构
            return readme_text if readme_text else "README content not found or empty."
        else:
            # 尝试查找 README 文件链接，然后获取其原始内容
            readme_file_link_element = soup.find('a', title=lambda t: t and t.lower().startswith('readme'))
            if readme_file_link_element:
                readme_file_url = f"https://github.com{readme_file_link_element['href']}"
                # 进一步请求 README 文件页面并解析原始内容链接，或者直接访问 raw 链接
                # 为了简化，这里返回提示信息
                return f"README found as file, check: {readme_file_url}"
            else:
                return "README section not found."

    except requests.exceptions.RequestException as e:
        return f"Error fetching README from {repo_link}: {e}"
    except Exception as e:
        return f"An unexpected error occurred while fetching README from {repo_link}: {e}"


# --- 主程序 ---
if __name__ == "__main__":
    proxy_status = "启用" if USE_PROXY else "禁用"
    print(f"代理状态: {proxy_status}")
    print("Fetching GitHub Trending Repositories...")
    top_repos = get_trending_repositories()
    output_content = f"## GitHub 今日热门仓库 Top {REPO_LIMIT}\n\n"

    if not top_repos:
        print("Could not fetch trending repositories.")
        output_content += "无法获取热门仓库信息。\n"
    else:
        print(f"Found {len(top_repos)} repositories. Fetching READMEs...")
        for i, repo in enumerate(top_repos):
            print(f"Fetching README for {repo['name']} ({i+1}/{REPO_LIMIT})...")
            # 加入一点延迟避免请求过快
            time.sleep(1)
            readme = get_readme_content(repo['link'])

            output_content += f"### {i+1}. [{repo['name']}]({repo['link']})\n"
            output_content += f"**About:** {repo['about']}\n"
            output_content += "**README:**\n```markdown\n"
            output_content += readme + "\n"
            output_content += "```\n\n"

    output_length = len(output_content)
    output_content += f"---\n**总输出文本长度:** {output_length}"

    print("\n--- Final Output ---")
    print(output_content)

    # 根据保存开关决定是否保存到文件
    if SAVE_TO_FILE:
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

        try:
            with open(file_path, "w", encoding="utf-8") as f:
                f.write(output_content)
            print(f"\n报告已保存到: {file_path}")
        except Exception as e:
            print(f"\n保存报告到文件时出错: {e}")
    else:
        print("\n文件保存功能已禁用。设置 SAVE_TO_FILE = True 以启用保存。")