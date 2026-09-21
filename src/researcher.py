import json
import datetime
import time
import urllib.parse
import xml.etree.ElementTree as ET
import requests
from google import genai
from google.genai import types
from src.config import GEMINI_API_KEY, MODELOS_TEXTO, MAX_PAUTAS
from src.editorial_manual import MANUAL_EDITORIAL

class RadarEditorial:
    def __init__(self):
        if not GEMINI_API_KEY:
            raise ValueError("GEMINI_API_KEY não configurada")
        self.client = genai.Client(api_key=GEMINI_API_KEY)

    def _coletar_noticias(self):
        consultas = [
            "inteligência artificial trabalho negócios Brasil",
            "empresas mercado economia Brasil",
            "carreira produtividade trabalho Brasil",
            "investimentos patrimônio imóveis Brasil",
            "direito trabalhista empresarial decisões Brasil",
            "tecnologia automação negócios Brasil",
        ]

        noticias = []
        vistos = set()

        for consulta in consultas:
            try:
                q = urllib.parse.quote(consulta)
                url = (
                    "https://news.google.com/rss/search?"
                    f"q={q}&hl=pt-BR&gl=BR&ceid=BR:pt-419"
                )
                resp = requests.get(
                    url,
                    timeout=15,
                    headers={"User-Agent": "Mozilla/5.0"}
                )
                resp.raise_for_status()

                root = ET.fromstring(resp.content)
                for item in root.findall(".//item")[:8]:
                    titulo = (item.findtext("title") or "").strip()
                    link = (item.findtext("link") or "").strip()
                    data = (item.findtext("pubDate") or "").strip()
                    fonte_el = item.find("source")
                    fonte = (fonte_el.text or "").strip() if fonte_el is not None else ""

                    chave = titulo.lower()
                    if not titulo or chave in vistos:
                        continue
                    vistos.add(chave)
                    noticias.append({
                        "titulo": titulo,
                        "url": link,
                        "data": data,
                        "fonte": fonte,
                    })
            except Exception as exc:
                print(f"Falha ao coletar RSS para '{consulta}': {exc}")

        return noticias[:40]

    def pesquisar(self, historico):
        hoje = datetime.datetime.now().strftime("%d/%m/%Y")
        historico_resumido = json.dumps(historico[-80:], ensure_ascii=False)
        noticias = self._coletar_noticias()

        if not noticias:
            raise RuntimeError("Não foi possível coletar notícias públicas para o radar.")

        fontes_contexto = json.dumps(noticias, ensure_ascii=False)

        prompt = f"""
Hoje é {hoje}. Você é um editor de pautas para uma marca pessoal brasileira.

{MANUAL_EDITORIAL}

HISTÓRICO RECENTE A EVITAR:
{historico_resumido}

NOTÍCIAS PÚBLICAS COLETADAS AGORA:
{fontes_contexto}

A pesquisa factual já foi feita fora do modelo. Use APENAS os itens acima como base
para fatos atuais. Não invente acontecimentos, números, fontes ou URLs.

Além das notícias, você pode sugerir no máximo 1 pauta AUTORAL/ATEMPORAL baseada no
Manual Editorial Uassi, desde que não dependa de um fato atual não fornecido acima.

REFERÊNCIAS EDITORIAIS
@tiohuli e @rob.correa são referências de estilo e território editorial. Eles servem
como inspiração de temas, perguntas, formatos e estruturas — nunca de redação.
Não afirme que um conteúdo específico deles foi publicado ou validado sem evidência
fornecida no contexto.

Para cada candidato, avalie:
- relevância;
- conexão com os pilares;
- ângulo não óbvio;
- possibilidade de reflexão própria;
- utilidade para vídeo curto, carrossel ou post estático;
- novidade em relação ao histórico.

Selecione NO MÁXIMO {MAX_PAUTAS} pautas, apenas se merecerem nota >= 7.

IMPORTANTE:
- Não copie ou faça paráfrase próxima de outros criadores.
- Se o ângulo exigir opinião pessoal ainda não registrada, use "PRECISA DE VALIDAÇÃO".
- "formato" deve ser VIDEO_CURTO, CARROSSEL ou POST_ESTATICO.
- Evite ganchos sensacionalistas e fórmulas clichês.
- Para pautas factuais, preserve a URL exata fornecida no contexto.

Retorne APENAS JSON válido:
[
  {{
    "pilar": "...",
    "tema": "...",
    "titulo": "...",
    "por_que_importa": "...",
    "angulo": "...",
    "formato": "VIDEO_CURTO",
    "gancho": "...",
    "nota": 9,
    "validacao": "AUTOMÁTICA ou PRECISA DE VALIDAÇÃO",
    "origem_editorial": "NOTICIA/TENDENCIA ou AUTORAL",
    "sinal_validacao": "descrição curta e objetiva ou SEM MÉTRICA PÚBLICA",
    "url": "https://..."
  }}
]
"""

        erros = []

        for modelo in MODELOS_TEXTO:
            try:
                print(f"Tentando modelo: {modelo}")
                response = self.client.models.generate_content(
                    model=modelo,
                    contents=prompt,
                    config=types.GenerateContentConfig(
                        response_mime_type="application/json",
                        temperature=0.25,
                    ),
                )

                if not response.text:
                    raise ValueError("modelo retornou resposta vazia")

                data = json.loads(response.text)
                if not isinstance(data, list):
                    raise ValueError("resposta JSON não é uma lista")

                qualificadas = [
                    p for p in data
                    if isinstance(p, dict) and p.get("nota", 0) >= 7
                ]
                return sorted(
                    qualificadas,
                    key=lambda x: x.get("nota", 0),
                    reverse=True
                )[:MAX_PAUTAS]

            except Exception as exc:
                erro = f"{modelo}: {type(exc).__name__}: {exc}"
                erros.append(erro)
                print(f"Falha com {erro}")
                time.sleep(2)

        raise RuntimeError(
            "Todos os modelos Gemini falharam. " + " | ".join(erros)
        )
