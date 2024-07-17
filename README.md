# Projeto: Resolução de Questões de Raciocínio Lógico com Amazon Bedrock Prompt Flows

## Descrição

Este projeto tem como objetivo utilizar o Amazon Bedrock Prompt Flows para aplicar a técnica de Self Consistency na resolução de questões de raciocínio lógico de múltipla escolha. O Amazon Bedrock Prompt Flows oferece a capacidade de usar modelos fundacionais (FMs) suportados para construir fluxos de trabalho, vinculando prompts, modelos fundacionais e outros serviços AWS para criar soluções completas.

## Conceitos Básicos

### Flow
Um prompt flow é um constructo que consiste em um nome, descrição, permissões, uma coleção de nodes e conexões entre esses nodes. Quando um prompt flow é invocado, o input é enviado através de cada node até alcançar um node de output. A resposta da invocação retorna o output final.

### Node
Um node é um passo dentro de um prompt flow. Para cada node, você configura seu nome, descrição, input, output e quaisquer configurações adicionais. A configuração de um node varia conforme seu tipo.

### Conexões
Existem dois tipos de conexões usadas em Prompt Flows:
- **Conexão de Dados**: Transfere dados de um node fonte para um node alvo.
- **Conexão Condicional**: Transfere dados se uma condição específica for cumprida.

### Expressões
Definem como extrair um input do input total que entra em um node.

### Flow Builder
Ferramenta visual na console do Amazon Bedrock para construir e editar prompt flows. Você arrasta e solta nodes na interface e configura inputs e outputs para definir seu flow.

### Termos Importantes
- **Whole Input**: Todo o input enviado de um node anterior para o node atual.
- **Upstream**: Nodes que ocorrem anteriormente no prompt flow.
- **Downstream**: Nodes que ocorrem posteriormente no prompt flow.
- **Input e Output**: Nodes podem ter múltiplos inputs e outputs, conectados através de expressões e conexões.

## Técnica de Self Consistency

Self Consistency é utilizada para ajudar a IA a resolver problemas que envolvem planejamento e raciocínio lógico. A técnica induz a geração de múltiplas respostas para aumentar a precisão da solução.

### Processo
1. O flow recebe a pergunta a ser respondida.
2. A pergunta é enviada a uma função Lambda que acessa uma base de dados com 10 perguntas e respostas comentadas.
3. A função escolhe 3 pares pergunta-resposta aleatoriamente e os concatena em um prompt no modelo few-shot CoT.
4. Este processo ocorre 5 vezes, gerando 5 "paths" diferentes.
5. Os prompts gerados são passados por um iterator no prompt flow.
6. Cada "path" é enviado a um node de tipo prompt, utilizando o modelo Claude 3.5 Sonnet para responder à pergunta.
7. Um collector coleta os outputs dos diferentes paths e envia a outra função Lambda que computa e retorna as respostas finais.

## Estrutura do Repositório

- `questions.json`: Arquivo com o dataset de perguntas e respostas.
- `definition.json`: Arquivo com a definição JSON do flow para deploy.
- `create-prompts.py`: Primeira função Lambda para criação de prompts.
- `evaluate-results.py`: Segunda função Lambda para avaliação dos resultados.

## Instruções de Uso

1. **Configuração do Ambiente**:
   - Certifique-se de ter acesso ao Amazon Bedrock e permissões adequadas para criar e gerenciar prompt flows.
   - Configure as funções Lambda (`create_prompts.py` e `evaluate_results.py`) no AWS Lambda.

2. **Deploy do Flow**:
   - Utilize o `definition.json` para configurar o prompt flow no Amazon Bedrock.

3. **Execução**:
   - Invoque o prompt flow com as perguntas de raciocínio lógico contidas no `questions.json`.

4. **Avaliação dos Resultados**:
   - A função `evaluate_results.py` processará as respostas geradas e fornecerá a resposta final com base na técnica de Self Consistency.

---

**Contato**: Davi Campos (davi08.sc@gmail.com)
