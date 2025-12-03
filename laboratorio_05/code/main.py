"""
Comparação entre GraphQL e REST API do GitHub
Mede tempo de resposta e tamanho dos dados retornados
"""

import json
import csv
import sys
from github_api import run_graphql_query, fetch_prs_rest_multiple, fetch_repo_rest_simple
from data import (
    build_pr_query_graphql, 
    build_simple_repo_query_graphql,
    processar_prs_graphql, 
    processar_prs_rest,
    processar_repo_simples_graphql,
    processar_repo_simples_rest
)

# Configure seu token do GitHub aqui
TOKEN = '{COLOQUE_SEU_TOKEN_AQUI}'

# Repositórios para testar (pode adicionar mais)
repoNameWithOwnerList = [
    "freeCodeCamp/freeCodeCamp",
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

# Converte a lista de strings "owner/name" para formato de dicionários
REPOSITORIES = []
for repo_string in repoNameWithOwnerList[:100]:
    owner, name = repo_string.split('/')
    REPOSITORIES.append({"owner": owner, "name": name})

def comparar_apis_simples(owner: str, name: str, token: str):
    """
    Compara GraphQL vs REST para buscar dados básicos do repositório (consulta simples).
    Retorna dicionário com métricas de comparação.
    """
    print(f"\n[TESTE SIMPLES] Analisando: {owner}/{name}")
    
    resultado = {
        'tipo_teste': 'simples',
        'repositorio': f"{owner}/{name}",
    }
    
    print("  [GraphQL] Executando query simples...")
    try:
        query = build_simple_repo_query_graphql(owner, name)
        graphql_result = run_graphql_query(query, token)
        
        repo_data = processar_repo_simples_graphql(graphql_result['data'])
        
        resultado['graphql_tempo_segundos'] = round(graphql_result['time'], 3)
        resultado['graphql_tamanho_bytes'] = graphql_result['size']
        resultado['graphql_tamanho_kb'] = round(graphql_result['size'] / 1024, 2)
        resultado['graphql_requisicoes'] = 1
        resultado['repo_id'] = repo_data.get('id', '')
        resultado['repo_name'] = repo_data.get('name', '')
        resultado['repo_language'] = repo_data.get('language', '')
        resultado['repo_size'] = repo_data.get('size', 0)
        
    except Exception as e:
        print(f"    ✗ Erro no GraphQL: {e}")
    
    print("  [REST] Executando query simples...")
    try:
        rest_result = fetch_repo_rest_simple(owner, name, token)
        
        repo_data = processar_repo_simples_rest(rest_result['data'])
        
        resultado['rest_tempo_segundos'] = round(rest_result['time'], 3)
        resultado['rest_tamanho_bytes'] = rest_result['size']
        resultado['rest_tamanho_kb'] = round(rest_result['size'] / 1024, 2)
        resultado['rest_requisicoes'] = rest_result['requests']
        
    except Exception as e:
        print(f"    ✗ Erro no REST: {e}")
    
    # Calcular diferenças
    if resultado.get('graphql_tempo_segundos') and resultado.get('rest_tempo_segundos'):
        resultado['diferenca_tempo_segundos'] = round(
            resultado['rest_tempo_segundos'] - resultado['graphql_tempo_segundos'], 3
        )
        resultado['diferenca_tempo_percentual'] = round(
            ((resultado['rest_tempo_segundos'] / resultado['graphql_tempo_segundos']) - 1) * 100, 2
        )
        
        resultado['diferenca_tamanho_bytes'] = (
            resultado['rest_tamanho_bytes'] - resultado['graphql_tamanho_bytes']
        )
        resultado['diferenca_tamanho_kb'] = round(
            resultado['diferenca_tamanho_bytes'] / 1024, 2
        )
        resultado['diferenca_tamanho_percentual'] = round(
            ((resultado['rest_tamanho_bytes'] / resultado['graphql_tamanho_bytes']) - 1) * 100, 2
        )
    
    return resultado


def comparar_apis_complexas(owner: str, name: str, token: str, num_prs: int = 100):
    """
    Compara GraphQL vs REST para buscar PRs de um repositório (consulta complexa).
    Retorna dicionário com métricas de comparação.
    """
    print(f"\n[TESTE COMPLEXO] Analisando: {owner}/{name}")
    
    resultado = {
        'tipo_teste': 'complexo',
        'repositorio': f"{owner}/{name}",
        'num_prs_solicitados': num_prs,
    }
    
    print("  [GraphQL] Executando query complexa...")
    try:
        query = build_pr_query_graphql(owner, name, first=num_prs)
        graphql_result = run_graphql_query(query, token)
        
        prs_graphql = processar_prs_graphql(graphql_result['data'])
        
        resultado['graphql_tempo_segundos'] = round(graphql_result['time'], 3)
        resultado['graphql_tamanho_bytes'] = graphql_result['size']
        resultado['graphql_tamanho_kb'] = round(graphql_result['size'] / 1024, 2)
        resultado['graphql_num_prs'] = len(prs_graphql)
        resultado['graphql_requisicoes'] = 1
        
    except Exception as e:
        print(f"    ✗ Erro no GraphQL: {e}")
    
    
    print("  [REST] Executando queries complexas...")
    try:
        # Calcular quantas páginas precisamos (REST limita 100 por página)
        max_pages = (num_prs + 99) // 100  # arredonda para cima
        
        rest_result = fetch_prs_rest_multiple(owner, name, token, per_page=100, max_pages=max_pages)
        
        prs_rest = processar_prs_rest(rest_result['data'])
        
        resultado['rest_tempo_segundos'] = round(rest_result['time'], 3)
        resultado['rest_tamanho_bytes'] = rest_result['size']
        resultado['rest_tamanho_kb'] = round(rest_result['size'] / 1024, 2)
        resultado['rest_num_prs'] = len(prs_rest)
        resultado['rest_requisicoes'] = rest_result['requests']
        
    except Exception as e:
        print(f"    ✗ Erro no REST: {e}")
    
    # Calcular diferenças
    if resultado.get('graphql_tempo_segundos') and resultado.get('rest_tempo_segundos'):
        resultado['diferenca_tempo_segundos'] = round(
            resultado['rest_tempo_segundos'] - resultado['graphql_tempo_segundos'], 3
        )
        resultado['diferenca_tempo_percentual'] = round(
            ((resultado['rest_tempo_segundos'] / resultado['graphql_tempo_segundos']) - 1) * 100, 2
        )
        
        resultado['diferenca_tamanho_bytes'] = (
            resultado['rest_tamanho_bytes'] - resultado['graphql_tamanho_bytes']
        )
        resultado['diferenca_tamanho_kb'] = round(
            resultado['diferenca_tamanho_bytes'] / 1024, 2
        )
        resultado['diferenca_tamanho_percentual'] = round(
            ((resultado['rest_tamanho_bytes'] / resultado['graphql_tamanho_bytes']) - 1) * 100, 2
        )

    
    return resultado


def exportar_csv(resultados: list, filename: str = "comparacao_graphql_rest.csv"):
    """
    Exporta os resultados para CSV.
    """
    if not resultados:
        print("Nenhum resultado para exportar.")
        return
    
    fieldnames = [
        'tipo_teste',
        'repositorio',
        'num_prs_solicitados',
        'graphql_tempo_segundos',
        'graphql_tamanho_bytes',
        'graphql_tamanho_kb',
        'graphql_num_prs',
        'graphql_requisicoes',
        'rest_tempo_segundos',
        'rest_tamanho_bytes',
        'rest_tamanho_kb',
        'rest_num_prs',
        'rest_requisicoes',
        'diferenca_tempo_segundos',
        'diferenca_tempo_percentual',
        'diferenca_tamanho_bytes',
        'diferenca_tamanho_kb',
        'diferenca_tamanho_percentual',
        'repo_id',
        'repo_name',
        'repo_language',
        'repo_size'
    ]
    
    with open(filename, 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames, extrasaction='ignore')
        writer.writeheader()
        writer.writerows(resultados)
    
    print(f"\nResultados exportados para: {filename}")

def exportar_json(resultados: list, filename: str = "comparacao_graphql_rest.json"):
    """
    Exporta os resultados para JSON.
    """
    
    if not resultados:
        print("Nenhum resultado para exportar.")
        return
    
    with open(filename, 'w', encoding='utf-8') as jsonfile:
        json.dump(resultados, jsonfile, ensure_ascii=False, indent=4)

def main():
    """
    Função principal que executa a comparação para todos os repositórios.
    Executa tanto o teste simples quanto o teste complexo.
    """
    if TOKEN == '{COLOQUE_SEU_TOKEN_AQUI}':
        print("ERRO: Configure seu token do GitHub na variável TOKEN")
        print("Gere um token em: https://github.com/settings/tokens")
        sys.exit(1)
    
    print("="*60)
    print("EXPERIMENTO: GraphQL vs REST")
    print("="*60)
    print(f"Total de repositórios para analisar: {len(REPOSITORIES)}")
    print(f"Testes por repositório: 2 (simples + complexo)")
    print(f"PRs por repositório (teste complexo): 100")
    print("="*60)
    
    resultados = []
    
    for repo in REPOSITORIES:
        try:
            # Teste 1: Consulta SIMPLES (apenas dados básicos do repositório)
            resultado_simples = comparar_apis_simples(
                owner=repo['owner'],
                name=repo['name'],
                token=TOKEN
            )
            resultados.append(resultado_simples)
            
            # Teste 2: Consulta COMPLEXA (PRs com dados detalhados)
            resultado_complexo = comparar_apis_complexas(
                owner=repo['owner'],
                name=repo['name'],
                token=TOKEN,
                num_prs=100
            )
            resultados.append(resultado_complexo)
            
        except Exception as e:
            print(f"\n✗ Erro ao processar {repo['owner']}/{repo['name']}: {e}")
            continue
    
    # Exportar resultados
    print("\n" + "="*60)
    print("EXPORTANDO RESULTADOS")
    print("="*60)
    exportar_csv(resultados)
    exportar_json(resultados)
    
    # Resumo
    print("\n" + "="*60)
    print("RESUMO")
    print("="*60)
    print(f"Total de testes realizados: {len(resultados)}")
    
    simples = [r for r in resultados if r.get('tipo_teste') == 'simples']
    complexos = [r for r in resultados if r.get('tipo_teste') == 'complexo']
    
    print(f"  - Testes simples: {len(simples)}")
    print(f"  - Testes complexos: {len(complexos)}")
    print("="*60)
    

if __name__ == "__main__":
    main()
