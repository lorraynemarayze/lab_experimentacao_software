"""
    Script para coletar os 1000 repositórios em Java com mais estrelas do GitHub
    e exportar os dados para CSV
"""

import csv  #importação para exportar CSV
import json
from github_api import run_query
from data import build_repo_query, build_pr_query, processar_dados_repositorio
from itertools import chain


token = '{COLOQUE_SEU_TOKEN_AQUI}'

result = [] #Lista que irá armazenar todos os prs coletados da API
repoNameWithOwnerList = [
    "freeCodeCamp/freeCodeCamp",
    "codecrafters-io/build-your-own-x",
    "sindresorhus/awesome",
    "EbookFoundation/free-programming-books",
    "public-apis/public-apis",
    "kamranahmedse/developer-roadmap",
    "jwasham/coding-interview-university",
    "donnemartin/system-design-primer",
    "996icu/996.ICU",
    "vinta/awesome-python",
    "awesome-selfhosted/awesome-selfhosted",
    "practical-tutorials/project-based-learning",
    "facebook/react",
    "vuejs/vue",
    "TheAlgorithms/Python",
    "torvalds/linux",
    "ossu/computer-science",
    "trekhleb/javascript-algorithms",
    "tensorflow/tensorflow",
    "trimstray/the-book-of-secret-knowledge",
    "getify/You-Dont-Know-JS",
    "CyC2018/CS-Notes",
    "ohmyzsh/ohmyzsh",
    "Significant-Gravitas/AutoGPT",
    "microsoft/vscode",
    "twbs/bootstrap",
    "flutter/flutter",
    "jackfrued/Python-100-Days",
    "github/gitignore",
    "jlevy/the-art-of-command-line",
    "AUTOMATIC1111/stable-diffusion-webui",
    "avelino/awesome-go",
    "ollama/ollama",
    "Snailclimb/JavaGuide",
    "huggingface/transformers",
    "airbnb/javascript",
    "n8n-io/n8n",
    "ytdl-org/youtube-dl",
    "vercel/next.js",
    "f/awesome-chatgpt-prompts",
    "yangshun/tech-interview-handbook",
    "golang/go",
    "labuladong/fucking-algorithm",
    "Genymobile/scrcpy",
    "yt-dlp/yt-dlp",
    "Chalarangelo/30-seconds-of-code",
    "langflow-ai/langflow",
    "facebook/react-native",
    "microsoft/PowerToys",
    "electron/electron",
    "kubernetes/kubernetes",
    "krahets/hello-algo",
    "langchain-ai/langchain",
    "justjavac/free-programming-books-zh_CN",
    "langgenius/dify",
    "nodejs/node",
    "ripienaar/free-for-dev",
    "d3/d3",
    "open-webui/open-webui",
    "mrdoob/three.js",
    "axios/axios",
    "excalidraw/excalidraw",
    "rust-lang/rust",
    "microsoft/TypeScript",
    "denoland/deno",
    "goldbergyoni/nodebestpractices",
    "facebook/create-react-app",
    "godotengine/godot",
    "microsoft/terminal",
    "deepseek-ai/DeepSeek-V3",
    "microsoft/generative-ai-for-beginners",
    "fatedier/frp",
    "rustdesk/rustdesk",
    "angular/angular",
    "papers-we-love/papers-we-love",
    "Hack-with-Github/Awesome-Hacking",
    "iptv-org/iptv",
    "tauri-apps/tauri",
    "mui/material-ui",
    "ant-design/ant-design",
    "shadcn-ui/ui",
    "Anduin2017/HowToCook",
    "nvbn/thefuck",
    "ryanmcdermott/clean-code-javascript",
    "neovim/neovim",
    "iluwatar/java-design-patterns",
    "mtdvio/every-programmer-should-know",
    "puppeteer/puppeteer",
    "microsoft/Web-Dev-For-Beginners",
    "tailwindlabs/tailwindcss",
    "PanJiaChen/vue-element-admin",
    "fastapi/fastapi",
    "comfyanonymous/ComfyUI",
    "supabase/supabase",
    "jaywcjlove/awesome-mac",
    "openai/whisper",
    "storybookjs/storybook",
    "2dust/v2rayN",
    "nvm-sh/nvm",
    "ggml-org/llama.cpp",
    "gin-gonic/gin",
    "ChatGPTNextWeb/NextChat",
    "florinpop17/app-ideas",
    "bitcoin/bitcoin",
    "django/django",
    "opencv/opencv",
    "sveltejs/svelte",
    "gohugoio/hugo",
    "mermaid-js/mermaid",
    "gothinkster/realworld",
    "animate-css/animate.css",
    "laravel/laravel",
    "macrozheng/mall",
    "home-assistant/core",
    "3b1b/manim",
    "oven-sh/bun",
    "tonsky/FiraCode",
    "microsoft/markitdown",
    "bregman-arie/devops-exercises",
    "spring-projects/spring-boot",
    "doocs/advanced-java",
    "MunGell/awesome-for-beginners",
    "immich-app/immich",
    "microsoft/ML-For-Beginners",
    "tensorflow/models",
    "microsoft/playwright",
    "DopplerHQ/awesome-interview-questions",
    "google-gemini/gemini-cli",
    "nomic-ai/gpt4all",
    "syncthing/syncthing",
    "netdata/netdata",
    "anuraghazra/github-readme-stats",
    "clash-verge-rev/clash-verge-rev",
    "ruanyf/weekly",
    "FortAwesome/Font-Awesome",
    "vitejs/vite",
    "louislam/uptime-kuma",
    "typicode/json-server",
    "elastic/elasticsearch",
    "hoppscotch/hoppscotch",
    "unionlabs/union",
    "junegunn/fzf",
    "coder/code-server",
    "sdmg15/Best-websites-a-programmer-should-visit",
    "hacksider/Deep-Live-Cam",
    "rasbt/LLMs-from-scratch",
    "vuejs/awesome-vue",
    "nestjs/nest",
    "d2l-ai/d2l-zh",
    "punkpeye/awesome-mcp-servers",
    "thedaviddias/Front-End-Checklist",
    "redis/redis",
    "abi/screenshot-to-code",
    "ventoy/Ventoy",
    "moby/moby",
    "browser-use/browser-use",
    "Shubhamsaboo/awesome-llm-apps",
    "pallets/flask",
    "swisskyrepo/PayloadsAllTheThings",
    "grafana/grafana",
    "enaqx/awesome-react",
    "tesseract-ocr/tesseract",
    "josephmisiti/awesome-machine-learning",
    "Developer-Y/cs-video-courses",
    "strapi/strapi",
    "hakimel/reveal.js",
    "binary-husky/gpt_academic",
    "protocolbuffers/protobuf",
    "modelcontextprotocol/servers",
    "sherlock-project/sherlock",
    "astral-sh/uv",
    "base/node",
    "ocornut/imgui",
    "awesomedata/awesome-public-datasets",
    "apache/superset",
    "localsend/localsend",
    "openai/openai-cookbook",
    "Stirling-Tools/Stirling-PDF",
    "expressjs/express",
    "PKUFlyingPig/cs-self-learning",
    "twitter/the-algorithm",
    "obsproject/obs-studio",
    "caddyserver/caddy",
    "fffaraz/awesome-cpp",
    "ansible/ansible",
    "chartjs/Chart.js",
    "zed-industries/zed",
    "Eugeny/tabby",
    "nektos/act",
    "lobehub/lobe-chat",
    "danielmiessler/SecLists",
    "AppFlowy-IO/AppFlowy",
    "leonardomso/33-js-concepts",
    "webpack/webpack",
    "jesseduffield/lazygit",
    "infiniflow/ragflow",
    "xtekky/gpt4free",
    "lydiahallie/javascript-questions",
    "apache/echarts",
    "juliangarnier/anime",
    "kelseyhightower/nocode",
    "All-Hands-AI/OpenHands",
    "TheAlgorithms/Java",
    "scikit-learn/scikit-learn",
    "keras-team/keras",
    "chrislgarry/Apollo-11",
    "labmlai/annotated_deep_learning_paper_implementations",
    "bradtraversy/design-resources-for-developers",
    "prakhar1989/awesome-courses",
    "sindresorhus/awesome-nodejs",
    "resume/resume.github.com",
    "socketio/socket.io",
    "dair-ai/Prompt-Engineering-Guide",
    "FuelLabs/sway",
    "facebook/docusaurus",
    "reduxjs/redux",
    "lodash/lodash",
    "NationalSecurityAgency/ghidra",
    "atom/atom",
    "localstack/localstack",
    "h5bp/Front-end-Developer-Interview-Questions",
    "prometheus/prometheus",
    "openinterpreter/open-interpreter",
    "alacritty/alacritty",
    "firecrawl/firecrawl",
    "rust-lang/rustlings",
    "ryanoasis/nerd-fonts",
    "jquery/jquery",
    "hiyouga/LLaMA-Factory",
    "tldr-pages/tldr",
    "vllm-project/vllm"    
] #Lista que irá armazenar os 'nameWithOwner' dos repositórios coletados


after = None #Cursor de paginação que será usado para navegar entre as páginas de resultados. Começa com None (primeira página), depois vai receber o endCursor da página anterior

repo_num_pages = 23
repo_ammount_per_page = 10

pr_num_pages = 20
pr_ammount_per_page = 10

filtered_repo_names_with_owner = []
if len(repoNameWithOwnerList) == 0:
    # Ajustado para coletar 1000 repositórios - API autoriza 10 repositórios por consulta
    print(f"Os {repo_num_pages * repo_ammount_per_page} repositórios serão coletados em {repo_num_pages} páginas diferentes, cada uma com {repo_ammount_per_page} repositórios.")


    for i in range(repo_num_pages): #Loop de paginação: irá executar 100 vezes para obter 100 páginas
        query = build_repo_query(after_cursor=after, first=repo_ammount_per_page)  #Constrói a query GraphQL com o cursor atual e quantidade definida
        print(f'Coletando repositórios da página {i + 1}')
        
        try:
            query_result = run_query(query, token) #Executa a query GraphQL usando o token de autenticação
            
            #Verifica se a resposta contém erros
            if 'errors' in query_result:
                print(f"Erro na consulta: {query_result['errors']}")
                break
            
        except Exception as e:
            print(f"Erro ao fazer consulta: {e}")
            break

        nodes = query_result['data']['search']['nodes'] #Extrai os dados dos repositórios da resposta JSON
        repoNameWithOwnerList.extend([repo['nameWithOwner'] for repo in nodes]) # Adiciona apenas o atributo nameWithOwner de cada repositório à lista principal
        
        print(f"Coletados {len(nodes)} repositórios. Total até agora: {len(repoNameWithOwnerList)}")

        page_info = query_result['data']['search']['pageInfo']
        if not page_info['hasNextPage']:   # Verifica se há próxima página disponível
            print("Não há mais páginas disponíveis.") 
            break
        after = page_info['endCursor']
        
cont = 1

# Agora coleta PRs de cada repositório
for repo in repoNameWithOwnerList:
    cont += 1
    owner, name = repo.split("/")
    prs = []
    current_page = 1
    print(f"\nColetando PRs do {cont}º repositório: {repo}")

    pr_after = None
    while current_page <= pr_num_pages:
        print(f"repositório {repo}: coletando página {current_page} de PRs")
        current_page += 1
        
        try:
            pr_query = build_pr_query(owner, name, after_cursor=pr_after, first=pr_ammount_per_page)
            pr_result = run_query(pr_query, token)
        except Exception as e:
            print(f"Erro ao fazer consulta na pagina {current_page} para {repo}: {e}")
            continue

        if "errors" in pr_result:
            print(f"Erro nos PRs de {repo}: {pr_result['errors']}")
            continue

        prs.extend(pr_result["data"]["repository"]["pullRequests"]["nodes"])

        pr_page_info = pr_result["data"]["repository"]["pullRequests"]["pageInfo"]
        if pr_page_info["hasNextPage"]:
            pr_after = pr_page_info["endCursor"]
        else:
            break

    if len(prs) >= 100:
        filtered_repo_names_with_owner.append(repo)
        
    result.append({"name": repo, "pullRequests": prs})

print("\n\nRepositórios coletados com Sucesso\n\n")

print(f"Total de repositórios coletados: {len(result)}")

processados = [processar_dados_repositorio(repo) for repo in result[:100]]
processados = list(chain.from_iterable(processados))  

print("\n\n\n")
print(f"Repositórios processados: {len(processados)}")

csv_filename = 'repositorios_github_dados.csv'

# Função para salvar CSV
def salvar_csv(dados, filename):
    print(f"\nSalvando dados em {csv_filename}...")
    with open(filename, "w", newline="") as csvfile:
        campos = dados[0].keys()  # usa as chaves como cabeçalho
        writer = csv.DictWriter(csvfile, fieldnames=campos)
        writer.writeheader()
        writer.writerows(dados)
        
def salvar_json(dados, filename):
    print(f"\nSalvando dados em {filename}...")
    with open(filename, "w") as jsonfile:
        json.dump(dados, jsonfile, indent=4)
        
def salvar_lista_em_arquivo(lista, nome_arquivo):
    with open(nome_arquivo, 'w', encoding='utf-8') as f:
        for item in lista:
            f.write(str(item) + '\n')

salvar_csv(processados, csv_filename)
salvar_json(processados, 'repositorios_github_dados.json')
salvar_lista_em_arquivo(filtered_repo_names_with_owner, 'repositorios_filtrados.txt')
print(processados)
