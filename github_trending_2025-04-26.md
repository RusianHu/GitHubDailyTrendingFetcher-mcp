## GitHub 今日热门仓库 Top 5

### 1. [kortix-ai /   suna](https://github.com/kortix-ai/suna)
**About:** Suna - Open Source Generalist AI Agent
**README:**
```markdown
Suna - Open Source Generalist AI Agent
(that acts on your behalf)
Suna is a fully open source AI assistant that helps you accomplish real-world tasks with ease. Through natural conversation, Suna becomes your digital companion for research, data analysis, and everyday challenges—combining powerful capabilities with an intuitive interface that understands what you need and delivers results.
Suna's powerful toolkit includes seamless browser automation to navigate the web and extract data, file management for document creation and editing, web crawling and extended search capabilities, command-line execution for system tasks, website deployment, and integration with various APIs and services. These capabilities work together harmoniously, allowing Suna to solve your complex problems and automate workflows through simple conversations!
Table of Contents
Suna Architecture
Backend API
Frontend
Agent Docker
Supabase Database
Run Locally / Self-Hosting
Requirements
Prerequisites
Installation Steps
Acknowledgements
License
Project Architecture
Suna consists of four main components:
Backend API
Python/FastAPI service that handles REST endpoints, thread management, and LLM integration with Anthropic, and others via LiteLLM.
Frontend
Next.js/React application providing a responsive UI with chat interface, dashboard, etc.
Agent Docker
Isolated execution environment for every agent - with browser automation, code interpreter, file system access, tool integration, and security features.
Supabase Database
Handles data persistence with authentication, user management, conversation history, file storage, agent state, analytics, and real-time subscriptions.
Use Cases
Competitor Analysis
(
Watch
) -
"Analyze the market for my next company in the healthcare industry, located in the UK. Give me the major players, their market size, strengths, and weaknesses, and add their website URLs. Once done, generate a PDF report."
VC List
(
Watch
) -
"Give me the list of the most important VC Funds in the United States based on Assets Under Management. Give me website URLs, and if possible an email to reach them out."
Looking for Candidates
(
Watch
) -
"Go on LinkedIn, and find me 10 profiles available - they are not working right now - for a junior software engineer position, who are located in Munich, Germany. They should have at least one bachelor's degree in Computer Science or anything related to it, and 1-year of experience in any field/role."
Planning Company Trip
(
Watch
) -
"Generate me a route plan for my company. We should go to California. We'll be in 8 people. Compose the trip from the departure (Paris, France) to the activities we can do considering that the trip will be 7 days long - departure on the 21st of Apr 2025. Check the weather forecast and temperature for the upcoming days, and based on that, you can plan our activities (outdoor vs indoor)."
Working on Excel
(
Watch
) -
"My company asked me to set up an Excel spreadsheet with all the information about Italian lottery games (Lotto, 10eLotto, and Million Day). Based on that, generate and send me a spreadsheet with all the basic information (public ones)."
Automate Event Speaker Prospecting
(
Watch
) -
"Find 20 AI ethics speakers from Europe who've spoken at conferences in the past year. Scrapes conference sites, cross-references LinkedIn and YouTube, and outputs contact info + talk summaries."
Summarize and Cross-Reference Scientific Papers
(
Watch
) -
"Research and compare scientific papers talking about Alcohol effects on our bodies during the last 5 years. Generate a report about the most important scientific papers talking about the topic I wrote before."
Research + First Contact Draft
(
Watch
) -
"Research my potential customers (B2B) on LinkedIn. They should be in the clean tech industry. Find their websites and their email addresses. After that, based on the company profile, generate a personalized first contact email where I present my company which is offering consulting services to cleantech companies to maximize their profits and reduce their costs."
SEO Analysis
(
Watch
) -
"Based on my website suna.so, generate an SEO report analysis, find top-ranking pages by keyword clusters, and identify topics I'm missing."
Generate a Personal Trip
(
Watch
) -
"Generate a personal trip to London, with departure from Bangkok on the 1st of May. The trip will last 10 days. Find an accommodation in the center of London, with a rating on Google reviews of at least 4.5. Find me interesting outdoor activities to do during the journey. Generate a detailed itinerary plan."
Recently Funded Startups
(
Watch
) -
"Go on Crunchbase, Dealroom, and TechCrunch, filter by Series A funding rounds in the SaaS Finance Space, and build a report with company data, founders, and contact info for outbound sales."
Scrape Forum Discussions
(
Watch
) -
"I need to find the best beauty centers in Rome, but I want to find them by using open forums that speak about this topic. Go on Google, and scrape the forums by looking for beauty center discussions located in Rome. Then generate a list of 5 beauty centers with the best comments about them."
Run Locally / Self-Hosting
Suna can be self-hosted on your own infrastructure. Follow these steps to set up your own instance.
Requirements
You'll need the following components:
A Supabase project for database and authentication
Redis database for caching and session management
Daytona sandbox for secure agent execution
Python 3.11 for the API backend
API keys for LLM providers (Anthropic)
Tavily API key for enhanced search capabilities
Firecrawl API key for web scraping capabilities
Prerequisites
Supabase
:
Create a new
Supabase project
Save your project's API URL, anon key, and service role key for later use
Install the
Supabase CLI
Redis
: Set up a Redis instance using one of these options:
Upstash Redis
(recommended for cloud deployments)
Local installation:
Mac
:
brew install redis
Linux
: Follow distribution-specific instructions
Windows
: Use WSL2 or Docker
Docker Compose (included in our setup):
If you're using our Docker Compose setup, Redis is included and configured automatically
No additional installation is needed
Save your Redis connection details for later use (not needed if using Docker Compose)
Daytona
:
Create an account on
Daytona
Generate an API key from your account settings
Go to
Images
Click "Add Image"
Enter
adamcohenhillel/kortix-suna:0.0.20
as the image name
Set
/usr/bin/supervisord -n -c /etc/supervisor/conf.d/supervisord.conf
as the Entrypoint
LLM API Keys
:
Obtain an API key
Anthropic
While other providers should work via
LiteLLM
, Anthropic is recommended – the prompt needs to be adjusted for other providers to output correct XML for tool calls.
Search API Key
(Optional):
For enhanced search capabilities, obtain an
Tavily API key
For web scraping capabilities, obtain a
Firecrawl API key
RapidAPI API Key
(Optional):
To enable API services like LinkedIn, and others, you'll need a RapidAPI key
Each service requires individual activation in your RapidAPI account:
Locate the service's
base_url
in its corresponding file (e.g.,
"https://linkedin-data-scraper.p.rapidapi.com"
in
backend/agent/tools/data_providers/LinkedinProvider.py
)
Visit that specific API on the RapidAPI marketplace
Subscribe to the service (many offer free tiers with limited requests)
Once subscribed, the service will be available to your agent through the API Services tool
Installation Steps
Clone the repository
:
git clone https://github.com/kortix-ai/suna.git
cd
suna
Configure backend environment
:
cd
backend
cp .env.example .env
#
Create from example if available, or use the following template
Edit the
.env
file and fill in your credentials:
NEXT_PUBLIC_URL=
"
http://localhost:3000
"
#
Supabase credentials from step 1
SUPABASE_URL=your_supabase_url
SUPABASE_ANON_KEY=your_supabase_anon_key
SUPABASE_SERVICE_ROLE_KEY=your_supabase_service_role_key
#
Redis credentials from step 2
REDIS_HOST=your_redis_host
REDIS_PORT=6379
REDIS_PASSWORD=your_redis_password
REDIS_SSL=True
#
Set to False for local Redis without SSL
#
Daytona credentials from step 3
DAYTONA_API_KEY=your_daytona_api_key
DAYTONA_SERVER_URL=
"
https://app.daytona.io/api
"
DAYTONA_TARGET=
"
us
"
#
Anthropic
ANTHROPIC_API_KEY=
#
OpenAI API:
OPENAI_API_KEY=your_openai_api_key
#
Optional but recommended
TAVILY_API_KEY=your_tavily_api_key
#
For enhanced search capabilities
FIRECRAWL_API_KEY=your_firecrawl_api_key
#
For web scraping capabilities
RAPID_API_KEY=
Set up Supabase database
:
#
Login to Supabase CLI
supabase login
#
Link to your project (find your project reference in the Supabase dashboard)
supabase link --project-ref your_project_reference_id
#
Push database migrations
supabase db push
Then, go to the Supabase web platform again -> choose your project -> Project Settings -> Data API -> And in the "Exposed Schema" ass "basejump" if not already there
Configure frontend environment
:
cd
../frontend
cp .env.example .env.local
#
Create from example if available, or use the following template
Edit the
.env.local
file:
NEXT_PUBLIC_SUPABASE_URL=your_supabase_url
NEXT_PUBLIC_SUPABASE_ANON_KEY=your_supabase_anon_key
NEXT_PUBLIC_BACKEND_URL="http://localhost:8000/api"  # Use this for local development
NEXT_PUBLIC_URL="http://localhost:3000"
Note: If you're using Docker Compose, use the container name instead of localhost:
NEXT_PUBLIC_BACKEND_URL="http://backend:8000/api"  # Use this when running with Docker Compose
Install dependencies
:
#
Install frontend dependencies
cd
frontend
npm install
#
Install backend dependencies
cd
../backend
pip install -r requirements.txt
Start the application
:
In one terminal, start the frontend:
cd
frontend
npm run dev
In another terminal, start the backend:
cd
backend
python api.py
5-6.
Docker Compose Alternative
:
Before running with Docker Compose, make sure your environment files are properly configured:
In
backend/.env
, set all the required environment variables as described above
For Redis configuration, use
REDIS_HOST=redis
instead of localhost
The Docker Compose setup will automatically set these Redis environment variables:
REDIS_HOST=redis
REDIS_PORT=6379
REDIS_PASSWORD=
REDIS_SSL=False
In
frontend/.env.local
, make sure to set
NEXT_PUBLIC_BACKEND_URL="http://backend:8000/api"
to use the container name
Then run:
export
GITHUB_REPOSITORY=
"
your-github-username/repo-name
"
docker compose -f docker-compose.ghcr.yaml up
If you're building the images locally instead of using pre-built ones:
docker compose up
The Docker Compose setup includes a Redis service that will be used by the backend automatically.
Access Suna
:
Open your browser and navigate to
http://localhost:3000
Sign up for an account using the Supabase authentication
Start using your self-hosted Suna instance!
Acknowledgements
Main Contributors
Adam Cohen Hillel
Dat-lequoc
Marko Kraemer
Technologies
Daytona
- Secure agent execution environment
Supabase
-
Playwright
- Browser automation
OpenAI
- LLM provider
Anthropic
- LLM provider
Tavily
- Search capabilities
Firecrawl
- Web scraping capabilities
RapidAPI
- API services
License
Kortix Suna is licensed under the Apache License, Version 2.0. See
LICENSE
for the full license text.
```

### 2. [lapce /   lapce](https://github.com/lapce/lapce)
**About:** Lightning-fast and Powerful Code Editor written in Rust
**README:**
```markdown
Lapce
Lightning-fast And Powerful Code Editor
Lapce (IPA: /læps/) is written in pure Rust with a UI in
Floem
. It is designed with
Rope Science
from the
Xi-Editor
which makes for lightning-fast computation, and leverages
Wgpu
for rendering. More information about the features of Lapce can be found on the
main website
and user documentation can be found on
GitBook
.
Features
Built-in LSP (
Language Server Protocol
) support to give you intelligent code features such as: completion, diagnostics and code actions
Modal editing support as first class citizen (Vim-like, and toggleable)
Built-in remote development support inspired by
VSCode Remote Development
. Enjoy the benefits of a "local" experience, and seamlessly gain the full power of a remote system. We also have
Lapdev
which can help manage your remote dev environments.
Plugins can be written in programming languages that can compile to the
WASI
format (C, Rust,
AssemblyScript
)
Built-in terminal, so you can execute commands in your workspace, without leaving Lapce.
Installation
You can find pre-built releases for Windows, Linux and macOS
here
, or
installing with a package manager
.
If you'd like to compile from source, you can find the
guide
.
Contributing
Lapdev
, developed by the Lapce team, is a cloud dev env service similar to GitHub Codespaces. By clicking the button above, you'll be taken to a fully set up Lapce dev env where you can browse the code and start developing. All dependencies are pre-installed, so you can get straight to code.
Guidelines for contributing to Lapce can be found in
CONTRIBUTING.md
.
Feedback & Contact
The most popular place for Lapce developers and users is on the
Discord server
.
Or, join the discussion on
Reddit
where we are just getting started.
There is also a
Matrix Space
, which is linked to the content from the Discord server.
License
Lapce is released under the Apache License Version 2, which is an open source license. You may contribute to this project, or use the code as you please as long as you adhere to its conditions. You can find a copy of the license text here:
LICENSE
.
```

### 3. [rowboatlabs /   rowboat](https://github.com/rowboatlabs/rowboat)
**About:** AI-powered multi-agent builder
**README:**
```markdown
Let AI build multi-agent workflows for you in minutes
Quickstart
|
Docs
|
Website
|
Discord
✨
Start from an idea -> copilot builds your multi-agent workflows
E.g. "Build me an assistant for a food delivery company to handle delivery status and missing items. Include the necessary tools."
🌐
Connect MCP servers
Add the MCP servers in settings -> import the tools into Rowboat.
📞
Integrate into your app using the HTTP API or Python SDK
Grab the project ID and generated API key from settings and use the API.
Powered by OpenAI's Agents SDK, Rowboat is the fastest way to build multi-agents!
Quick start
Set your OpenAI key
export
OPENAI_API_KEY=your-openai-api-key
Clone the repository and start Rowboat docker
git clone git@github.com:rowboatlabs/rowboat.git
cd
rowboat
docker-compose up --build
Access the app at
http://localhost:3000
.
Demo
Create a multi-agent assistant with MCP tools by chatting with Rowboat
Integrate with Rowboat agents
There are 2 ways to integrate with the agents you create in Rowboat
HTTP API
You can use the API directly at
http://localhost:3000/api/v1/
See
API Docs
for details
curl --location
'
http://localhost:3000/api/v1/<PROJECT_ID>/chat
'
\
--header
'
Content-Type: application/json
'
\
--header
'
Authorization: Bearer <API_KEY>
'
\
--data
'
{
"messages": [
{
"role": "user",
"content": "tell me the weather in london in metric units"
}
],
"state": null
}
'
Python SDK
You can use the included Python SDK to interact with the Agents
pip install rowboat
See
SDK Docs
for details. Here is a quick example:
from
rowboat
import
Client
,
StatefulChat
from
rowboat
.
schema
import
UserMessage
,
SystemMessage
# Initialize the client
client
=
Client
(
host
=
"http://localhost:3000"
,
project_id
=
"<PROJECT_ID>"
,
api_key
=
"<API_KEY>"
)
# Create a stateful chat session (recommended)
chat
=
StatefulChat
(
client
)
response
=
chat
.
run
(
"What's the weather in London?"
)
print
(
response
)
# Or use the low-level client API
messages
=
[
SystemMessage
(
role
=
'system'
,
content
=
"You are a helpful assistant"
),
UserMessage
(
role
=
'user'
,
content
=
"Hello, how are you?"
)
]
# Get response
response
=
client
.
chat
(
messages
=
messages
)
print
(
response
.
messages
[
-
1
].
content
)
Refer to
Docs
to learn how to start building agents with Rowboat.
```

### 4. [ocrmypdf /   OCRmyPDF](https://github.com/ocrmypdf/OCRmyPDF)
**About:** OCRmyPDF adds an OCR text layer to scanned PDF files, allowing them to be searched
**README:**
```markdown
OCRmyPDF adds an OCR text layer to scanned PDF files, allowing them to be searched or copy-pasted.
ocrmypdf
#
it's a scriptable command line program
-l eng+fra
#
it supports multiple languages
--rotate-pages
#
it can fix pages that are misrotated
--deskew
#
it can deskew crooked PDFs!
--title
"
My PDF
"
#
it can change output metadata
--jobs 4
#
it uses multiple cores by default
--output-type pdfa
#
it produces PDF/A by default
input_scanned.pdf
#
takes PDF input (or images)
output_searchable.pdf
#
produces validated PDF output
See the release notes for details on the latest changes
.
Main features
Generates a searchable
PDF/A
file from a regular PDF
Places OCR text accurately below the image to ease copy / paste
Keeps the exact resolution of the original embedded images
When possible, inserts OCR information as a "lossless" operation without disrupting any other content
Optimizes PDF images, often producing files smaller than the input file
If requested, deskews and/or cleans the image before performing OCR
Validates input and output files
Distributes work across all available CPU cores
Uses
Tesseract OCR
engine to recognize more than
100 languages
Keeps your private data private.
Scales properly to handle files with thousands of pages.
Battle-tested on millions of PDFs.
For details: please consult the
documentation
.
Motivation
I searched the web for a free command line tool to OCR PDF files: I found many, but none of them were really satisfying:
Either they produced PDF files with misplaced text under the image (making copy/paste impossible)
Or they did not handle accents and multilingual characters
Or they changed the resolution of the embedded images
Or they generated ridiculously large PDF files
Or they crashed when trying to OCR
Or they did not produce valid PDF files
On top of that none of them produced PDF/A files (format dedicated for long time storage)
...so I decided to develop my own tool.
Installation
Linux, Windows, macOS and FreeBSD are supported. Docker images are also available, for both x64 and ARM.
Operating system
Install command
Debian, Ubuntu
apt install ocrmypdf
Windows Subsystem for Linux
apt install ocrmypdf
Fedora
dnf install ocrmypdf
macOS (Homebrew)
brew install ocrmypdf
macOS (MacPorts)
port install ocrmypdf
macOS (nix)
nix-env -i ocrmypdf
LinuxBrew
brew install ocrmypdf
FreeBSD
pkg install py-ocrmypdf
Ubuntu Snap
snap install ocrmypdf
For everyone else,
see our documentation
for installation steps.
Languages
OCRmyPDF uses Tesseract for OCR, and relies on its language packs. For Linux users, you can often find packages that provide language packs:
#
Display a list of all Tesseract language packs
apt-cache search tesseract-ocr
#
Debian/Ubuntu users
apt-get install tesseract-ocr-chi-sim
#
Example: Install Chinese Simplified language pack
#
Arch Linux users
pacman -S tesseract-data-eng tesseract-data-deu
#
Example: Install the English and German language packs
#
brew macOS users
brew install tesseract-lang
You can then pass the
-l LANG
argument to OCRmyPDF to give a hint as to what languages it should search for. Multiple languages can be requested.
OCRmyPDF supports Tesseract 4.1.1+. It will automatically use whichever version it finds first on the
PATH
environment variable. On Windows, if
PATH
does not provide a Tesseract binary, we use the highest version number that is installed according to the Windows Registry.
Documentation and support
Once OCRmyPDF is installed, the built-in help which explains the command syntax and options can be accessed via:
ocrmypdf --help
Our
documentation is served on Read the Docs
.
Please report issues on our
GitHub issues
page, and follow the issue template for quick response.
Feature demo
#
Add an OCR layer and convert to PDF/A
ocrmypdf input.pdf output.pdf
#
Convert an image to single page PDF
ocrmypdf input.jpg output.pdf
#
Add OCR to a file in place (only modifies file on success)
ocrmypdf myfile.pdf myfile.pdf
#
OCR with non-English languages (look up your language's ISO 639-3 code)
ocrmypdf -l fra LeParisien.pdf LeParisien.pdf
#
OCR multilingual documents
ocrmypdf -l eng+fra Bilingual-English-French.pdf Bilingual-English-French.pdf
#
Deskew (straighten crooked pages)
ocrmypdf --deskew input.pdf output.pdf
For more features, see the
documentation
.
Requirements
In addition to the required Python version, OCRmyPDF requires external program installations of Ghostscript and Tesseract OCR. OCRmyPDF is pure Python, and runs on pretty much everything: Linux, macOS, Windows and FreeBSD.
Press & Media
Going paperless with OCRmyPDF
Converting a scanned document into a compressed searchable PDF with redactions
c't 1-2014, page 59
: Detailed presentation of OCRmyPDF v1.0 in the leading German IT magazine c't
heise Open Source, 09/2014: Texterkennung mit OCRmyPDF
heise Durchsuchbare PDF-Dokumente mit OCRmyPDF erstellen
Excellent Utilities: OCRmyPDF
LinuxUser Texterkennung mit OCRmyPDF und Scanbd automatisieren
Y Combinator discussion
Business enquiries
OCRmyPDF would not be the software that it is today without companies and users choosing to provide support for feature development and consulting enquiries. We are happy to discuss all enquiries, whether for extending the existing feature set, or integrating OCRmyPDF into a larger system.
License
The OCRmyPDF software is licensed under the Mozilla Public License 2.0 (MPL-2.0). This license permits integration of OCRmyPDF with other code, included commercial and closed source, but asks you to publish source-level modifications you make to OCRmyPDF.
Some components of OCRmyPDF have other licenses, as indicated by standard SPDX license identifiers or the DEP5 copyright and licensing information file. Generally speaking, non-core code is licensed under MIT, and the documentation and test files are licensed under Creative Commons ShareAlike 4.0 (CC-BY-SA 4.0).
Disclaimer
The software is distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
```

### 5. [aquasecurity /   trivy](https://github.com/aquasecurity/trivy)
**About:** Find vulnerabilities, misconfigurations, secrets, SBOM in containers, Kubernetes, code repositories, clouds and more
**README:**
```markdown
📖 Documentation
Trivy (
pronunciation
) is a comprehensive and versatile security scanner.
Trivy has
scanners
that look for security issues, and
targets
where it can find those issues.
Targets (what Trivy can scan):
Container Image
Filesystem
Git Repository (remote)
Virtual Machine Image
Kubernetes
Scanners (what Trivy can find there):
OS packages and software dependencies in use (SBOM)
Known vulnerabilities (CVEs)
IaC issues and misconfigurations
Sensitive information and secrets
Software licenses
Trivy supports most popular programming languages, operating systems, and platforms. For a complete list, see the
Scanning Coverage
page.
To learn more, go to the
Trivy homepage
for feature highlights, or to the
Documentation site
for detailed information.
Quick Start
Get Trivy
Trivy is available in most common distribution channels. The full list of installation options is available in the
Installation
page. Here are a few popular examples:
brew install trivy
docker run aquasec/trivy
Download binary from
https://github.com/aquasecurity/trivy/releases/latest/
See
Installation
for more
Trivy is integrated with many popular platforms and applications. The complete list of integrations is available in the
Ecosystem
page. Here are a few popular examples:
GitHub Actions
Kubernetes operator
VS Code plugin
See
Ecosystem
for more
Canary builds
There are canary builds (
Docker Hub
,
GitHub
,
ECR
images and
binaries
) as generated every push to main branch.
Please be aware: canary builds might have critical bugs, it's not recommended for use in production.
General usage
trivy
<
target
>
[--scanners
<
scanner1,scanner
2>
]
<
subject
>
Examples:
trivy image python:3.4-alpine
Result
trivy-image.mov
trivy fs --scanners vuln,secret,misconfig myproject/
Result
trivy-fs.mov
trivy k8s --report summary cluster
Result
FAQ
How to pronounce the name "Trivy"?
tri
is pronounced like
tri
gger,
vy
is pronounced like en
vy
.
Want more? Check out Aqua
If you liked Trivy, you will love Aqua which builds on top of Trivy to provide even more enhanced capabilities for a complete security management offering.
You can find a high level comparison table specific to Trivy users
here
.
In addition check out the
https://aquasec.com
website for more information about our products and services.
If you'd like to contact Aqua or request a demo, please use this form:
https://www.aquasec.com/demo
Community
Trivy is an
Aqua Security
open source project.
Learn about our open source work and portfolio
here
.
Contact us about any matter by opening a GitHub Discussion
here
Please ensure to abide by our
Code of Conduct
during all interactions.
```

---
**总输出文本长度:** 25164