# Especificação — Criador Automático da Nova Linha Editorial

## Objetivo
Receber pautas já aprovadas pelo Radar Editorial e transformá-las em peças finais prontas para publicação.

## Entradas
Cada pauta aprovada deve conter:
- id;
- título-base;
- tema;
- pilar;
- ângulo;
- formato final aprovado;
- fonte factual;
- observações do usuário;
- status de aprovação.

## Saídas

### CARROSSEL
Padrão:
- 5 slides;
- máximo de 7;
- proporção recomendada 4:5;
- slide 1 obrigatoriamente com capa visual;
- pelo menos mais 1 slide com imagem, arte, gráfico simples ou composição visual;
- demais slides podem ser tipográficos, desde que mantenham hierarquia e consistência.

Estrutura-base de 5 slides:
1. Capa — imagem/arte + título.
2. Contexto — texto curto e claro.
3. Ideia central — desenvolvimento.
4. Reforço visual — imagem/arte/dado visual + texto curto.
5. Fechamento — conclusão + CTA discreto.

O sistema pode usar 6 ou 7 slides apenas quando a pauta realmente exigir.

### POST_ESTATICO
- uma única arte;
- ideia forte;
- título ou frase principal;
- apoio visual quando fizer sentido;
- legenda pronta.

### VIDEO_CURTO
O criador não publica o vídeo.
Entrega apenas:
- roteiro;
- gancho;
- desenvolvimento;
- fechamento;
- legenda;
- fonte.
A postagem é manual.

## Estilo visual
A automação deve trabalhar com um conjunto pequeno de templates consistentes, não gerar layouts aleatórios a cada publicação.

Templates iniciais:
- T1: editorial com foto + bloco tipográfico;
- T2: minimalista tipográfico;
- T3: dado/estatística + elemento gráfico;
- T4: imagem documental + comentário;
- T5: citação/ideia curta com grande destaque visual.

## Imagens
Prioridade:
1. imagem diretamente relacionada ao fato/tema quando houver fonte adequada;
2. imagem editorial/licenciada de banco permitido;
3. imagem gerada;
4. fallback minimalista sem fotografia quando não houver imagem boa.

Nunca usar imagem de baixa qualidade apenas para cumprir quota visual.

## Legenda
- linguagem direta;
- contextualizar a pauta;
- incluir fonte quando factual;
- evitar CTA artificial;
- evitar fórmulas genéricas de engajamento.

## Organização semanal
Sábado:
- radar envia pautas;
- usuário aprova/rejeita/muda formato.

Após aprovação:
- criador gera os materiais aprovados.

Até segunda-feira:
- carrosséis e estáticos devem estar finalizados;
- vídeos devem estar com roteiro pronto;
- pacote fica disponível para o publicador.

## Integração futura com o Publicador
O gerador deve produzir um manifesto por peça, por exemplo:

{
  "id": "2026-09-21-pauta-01",
  "formato": "CARROSSEL",
  "caption": "...",
  "assets": [
    "slide_01.jpg",
    "slide_02.jpg",
    "slide_03.jpg",
    "slide_04.jpg",
    "slide_05.jpg"
  ],
  "source_url": "...",
  "status": "READY_TO_PUBLISH"
}

O publicador deve ler apenas peças com status READY_TO_PUBLISH.

## Regras de segurança editorial
- não inventar opinião pessoal;
- não publicar pauta que esteja marcada como PRECISA_DE_VALIDACAO;
- não copiar texto de criadores de referência;
- não publicar fato sem fonte;
- manter histórico para evitar duplicação.
