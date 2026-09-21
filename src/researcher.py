import json
import datetime
import time
from google import genai
from google.genai import types
from src.config import GEMINI_API_KEY, MODELOS_TEXTO, MAX_PAUTAS
from src.editorial_manual import MANUAL_EDITORIAL

class RadarEditorial:
    def __init__(self):
        if not GEMINI_API_KEY:
            raise ValueError("GEMINI_API_KEY não configurada")
        self.client = genai.Client(api_key=GEMINI_API_KEY)

    def pesquisar(self, historico):
        hoje = datetime.datetime.now().strftime("%d/%m/%Y")
        historico_resumido = json.dumps(historico[-80:], ensure_ascii=False)

        prompt = f"""
Hoje é {hoje}. Você é um editor e pesquisador de pautas para uma marca pessoal brasileira.

{MANUAL_EDITORIAL}

HISTÓRICO RECENTE A EVITAR:
{historico_resumido}

PESQUISA EM DUAS FRENTES

FRENTE A — FATOS E TENDÊNCIAS
Use Google Search para encontrar notícias, pesquisas, casos, movimentos empresariais,
tendências ou fatos publicados preferencialmente nas últimas 24-72 horas.
Busque variedade entre negócios, dinheiro, trabalho/carreira, IA/tecnologia,
Direito com consequência prática e temas sociais/culturais não eleitorais.

FRENTE B — REFERÊNCIAS EDITORIAIS
Pesquise conteúdos públicos recentes e também conteúdos recorrentes dos criadores
de referência, inicialmente @tiohuli e @rob.correa, além de outros perfis semelhantes
que possam ser descobertos.

Não copie o conteúdo. Identifique:
- tema;
- tese central;
- formato;
- pergunta que sustenta o conteúdo;
- motivo provável de interesse da audiência;
- sinais públicos de validação, quando realmente verificáveis.

Se não houver métrica ou evidência suficiente para chamar de validado,
trate apenas como REFERÊNCIA EDITORIAL.

Quando um tema de referência couber nos pilares, reconstrua a pauta do zero:
use fatos/fontes independentes quando aplicável e adapte o ângulo ao Manual Editorial Uassi.

Não force equilíbrio entre pilares. Se um assunto for fraco, descarte.
Não selecione pauta apenas porque é recente ou porque outro criador publicou.

Para cada candidato, avalie:
- relevância atual;
- conexão com os pilares;
- existência de um ângulo não óbvio;
- possibilidade de gerar reflexão própria;
- utilidade para vídeo curto ou carrossel;
- novidade em relação ao histórico;
- existência de sinal de validação editorial.

Selecione NO MÁXIMO {MAX_PAUTAS} pautas, apenas se merecerem nota >= 7.

IMPORTANTE:
- Não invente fatos, números, métricas, URLs ou opiniões.
- Prefira fonte primária ou veículo confiável para fatos.
- Política partidária/eleitoral não é foco desta automação.
- Se o ângulo exigir opinião pessoal ainda não registrada, use "PRECISA DE VALIDAÇÃO".
- "formato" deve ser um entre: VIDEO_CURTO, CARROSSEL, POST_ESTATICO.
- O gancho não deve ser sensacionalista nem usar fórmulas clichês.
- Se a pauta vier de criador de referência, cite o perfil apenas como origem editorial,
  nunca como fonte factual quando o fato depender de verificação externa.
- Nunca reproduza redação, roteiro, legenda ou sequência distintiva de outro criador.

Retorne APENAS JSON válido neste formato:
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
    "origem_editorial": "NOTICIA/TENDENCIA ou @perfil ou AUTORAL",
    "sinal_validacao": "descrição curta e objetiva ou SEM MÉTRICA PÚBLICA",
    "url": "https://..."
  }}
]
"""
        for modelo in MODELOS_TEXTO:
            try:
                response = self.client.models.generate_content(
                    model=modelo,
                    contents=prompt,
                    config=types.GenerateContentConfig(
                        tools=[types.Tool(google_search=types.GoogleSearch())],
                        response_mime_type="application/json",
                        temperature=0.25,
                    ),
                )
                data = json.loads(response.text)
                if isinstance(data, list):
                    return sorted(data, key=lambda x: x.get("nota", 0), reverse=True)[:MAX_PAUTAS]
            except Exception as exc:
                print(f"Falha com {modelo}: {exc}")
                time.sleep(2)
        return []
