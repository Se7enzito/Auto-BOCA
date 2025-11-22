import os
import shutil
import requests
import urllib3

from urllib.parse import urljoin
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Configs
DESTINO = os.path.join(os.getcwd(), "docs")
RESULTADOS = os.path.join(os.getcwd(), "respostas")
os.makedirs(RESULTADOS, exist_ok=True)
os.makedirs(DESTINO, exist_ok=True)

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# Manipulação do BOCA
def fazer_login(meu_usuario, minha_senha) -> webdriver:
    opts = Options()
    opts.headless = False
    driver = webdriver.Chrome(options=opts)

    driver.get("https://bocajr.dcomp.ufsj.edu.br/index.php")

    driver.find_element(By.NAME, "name").send_keys(meu_usuario)
    driver.find_element(By.NAME, "password").send_keys(minha_senha)

    driver.find_element(By.NAME, "Submit").click()
    
    print("✅ Login realizado com sucesso!")

    return driver
    
def baixar_exercicios(driver) -> None:
    driver.get("https://bocajr.dcomp.ufsj.edu.br/team/problem.php")
    print("✅ Página de problemas carregada!")

    links_pdf = driver.find_elements(By.XPATH, "//a[contains(text(), '.pdf')]")
    print(f"🔗 {len(links_pdf)} PDFs encontrados.")

    session = requests.Session()
    for cookie in driver.get_cookies():
        session.cookies.set(cookie['name'], cookie['value'])

    for link in links_pdf:
        pdf_href = link.get_attribute("href")
        pdf_url = urljoin(driver.current_url, pdf_href)
        texto = link.text.strip()
        if not texto.lower().endswith(".pdf"):
            texto += ".pdf"
        caminho_arquivo = os.path.join(DESTINO, texto)

        print(f"⬇️  Baixando {texto} ...")
        resp = session.get(pdf_url, verify=False)
        if resp.status_code == 200:
            with open(caminho_arquivo, "wb") as f:
                f.write(resp.content)
            print(f"   ✅ Salvo em {caminho_arquivo}")
        else:
            print(f"   ⚠️  Erro ao baixar ({resp.status_code})")

    print("\n🎉 Todos os PDFs foram baixados com sucesso!")
    print(f"📂 Pasta: {DESTINO}")
    
def enviar_exercicios(driver, exercicios) -> None:
    driver.get("https://bocajr.dcomp.ufsj.edu.br/team/run.php")
    print("✅ Página de submissão carregada!")

    for exercicio in exercicios:
        problem = exercicio["problem"]
        language = exercicio["language"]
        arquivo = exercicio["arquivo"]

        print(f"\n📤 Enviando exercício {problem} ({arquivo})...")

        try:
            select_problem = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.NAME, "problem"))
            )
            select_problem.send_keys(problem)

            select_language = driver.find_element(By.NAME, "language")
            select_language.send_keys(language)

            input_file = driver.find_element(By.NAME, "sourcefile")
            input_file.send_keys(os.path.abspath(arquivo))

            confirmation_input = driver.find_element(By.NAME, "confirmation")
            driver.execute_script("arguments[0].value = 'confirm';", confirmation_input)

            driver.find_element(By.NAME, "Submit").click()

            WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.XPATH, "//b[contains(text(),'Run ID')]"))
            )
            print("   ✅ Envio realizado com sucesso!")

        except Exception as e:
            print(f"   ⚠️ Erro ao enviar {arquivo}: {e}")
            
def limpar_pastas() -> None:
    for pasta in [DESTINO, RESULTADOS]:
        print(f"\n🧹 Limpando pasta {pasta} ...")

        if not os.path.exists(pasta):
            print("⚠️  A pasta não existe, nada a limpar.")
            return

        for item in os.listdir(pasta):
            caminho_item = os.path.join(pasta, item)
            try:
                if os.path.isfile(caminho_item) or os.path.islink(caminho_item):
                    os.remove(caminho_item)
                elif os.path.isdir(caminho_item):
                    shutil.rmtree(caminho_item)
                print(f"   🗑️  Removido: {item}")
            except Exception as e:
                print(f"   ⚠️  Erro ao remover {item}: {e}")

        print("✅ Pasta limpa com sucesso!\n")
        
# Remoção texto atividades

# Geração dos Códigos
def obter_mapeamento_problemas_por_docs() -> dict:
    arquivos = sorted(os.listdir(DESTINO))
    mapeamento = {}
    indice = 1

    for arquivo in arquivos:
        if not os.path.isfile(os.path.join(DESTINO, arquivo)):
            continue

        nome = arquivo.split(".")[0].strip()
        
        if nome and nome not in mapeamento:
            mapeamento[nome] = str(indice)
            indice += 1

    if not mapeamento:
        print("⚠️ Nenhum arquivo encontrado em docs/ para mapear problemas!")
    else:
        print("📘 Mapeamento de problemas baseado em arquivos:")
        for letra, valor in mapeamento.items():
            print(f"  {letra} → {valor}")

    return mapeamento

def obter_linguagem_codigo(nome_arquivo: str) -> str:
    sufix = nome_arquivo.split(".")[-1].lower()

    LANGUAGES = {
        "c": "1",
        "cpp": "2",
        "cc": "2",
        "java": "3",
        "kt": "4",
        "py": "5"
    }

    return LANGUAGES.get(sufix, "5")

def gerar_exercicios() -> list:
    # TODO: Base código exercicios
    # exercicios = [
    #     {"problem": "1", "language": LANGUAGES["Python3"], "arquivo": "resposta/A.py"},
    #     {"problem": "2", "language": LANGUAGES["C++20"], "arquivo": "resposta/B.cpp"},
    # ]
    exercicios = []
    
    mapeamento = obter_mapeamento_problemas_por_docs()
    
    # TODO: Gerar arquivos
    # TODO: Pegar os arquivos e descobrir a extensão deles
    
    for exercicio in mapeamento.keys():
        payload = {}
        
        arquivo = exercicio + ".pdf"
        
        if not os.path.isfile(os.path.join(DESTINO, arquivo)):
            continue
        
        payload["problem"] = mapeamento[exercicio]
        
        print(arquivo)
    
    return exercicios

# TODO: Criar LLM para avaliar os códigos gerados pela IA

# Função Principal
def app():
    usuario = "dupla1"
    senha = "3cP9i"
    
    driver = fazer_login(usuario, senha)
    
    baixar_exercicios(driver)
    
    # exercicios = gerar_exercicios()
    
    input("Pressione enter para fechar o programa...")
    
    limpar_pastas()

if __name__ == "__main__":
    app()