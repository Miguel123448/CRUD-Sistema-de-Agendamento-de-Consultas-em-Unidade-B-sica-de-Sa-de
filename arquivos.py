import os
import json

def carregar_dados (caminho):
    if os.path.exits(caminho):
        with open(caminho, "r", encoding="utf-8") as arquivo:
            return json.load(arquivo)
    return 0

def salvar_dados(caminho,dados):
    with open(caminho,"w", encoding = "utf-8") as arquivo:
        json.dump(dados,arquivo, indent=4, ensure_ascii=False)
