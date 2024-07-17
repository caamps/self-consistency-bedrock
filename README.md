# Projeto: Resolução de Questões de Raciocínio Lógico com Amazon Bedrock Prompt Flows

## Descrição

Este projeto tem como objetivo utilizar o Amazon Bedrock Prompt Flows para aplicar a técnica de Self Consistency na resolução de questões de raciocínio lógico de múltipla escolha. O Amazon Bedrock Prompt Flows oferece a capacidade de usar modelos fundacionais (FMs) para construir workflows, interliando prompts e outros serviços AWS para criar soluções completas.

## Conceitos Básicos

### Flow
Um prompt flow consiste em uma coleção de nodes e conexões entre esses nodes. Quando um prompt flow é invocado, o input é enviado através de cada node até alcançar um node de output. A resposta da invocação retorna o output final.

### Node
Um node é um passo dentro de um prompt flow. Para cada node, você configura seu nome, descrição, input, output e quaisquer configurações adicionais. A configuração de um node varia conforme seu tipo.

### Conexões
Existem dois tipos de conexões usadas em Prompt Flows:
- **Conexão de Dados**: Transfere dados de um node fonte para um node alvo.
- **Conexão Condicional**: Transfere dados se uma condição específica for cumprida.

### Flow Builder
Ferramenta visual na console do Amazon Bedrock para construir e editar prompt flows. Você arrasta e solta nodes na interface e configura inputs e outputs para definir seu flow.

## Técnica de Self Consistency

Self Consistency é utilizada para ajudar a IA a resolver problemas que envolvem planejamento e raciocínio lógico. A técnica induz a geração de múltiplos Chain-of-Thought, gerando diferentes respostas. Com base na distribuição dessas respostas, escolhe-se qual tem a maior probabilidade de estar correta.

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
- `packages`: Pasta contendo os pacotes para deploy das funções Lambda.
- `template.py`: Código em python utilizando o boto3 para deploy da solução. Obs: No momento de desenvolvimento desse projeto, o Bedrock Prompt Flows está em preview e ainda não está integrado com o CloudFormation. Por isso a escolha do boto3. 

## Instruções de Uso

1. **Configuração do Ambiente**:
   - Certifique-se de ter acesso à conta AWS, com permissão o suficiente para criar e alterar os recursos necessários.
   - Instale o AWS CLI e configure suas credenciais usando `aws configure` se ainda não estiver configurado.
   - Certifique-se de ter o Python instalado juntamente com o boto3 (`pip install boto3`).

2. **Execução do Script template.py:**:
   - O script `template.py` usa boto3 para criar recursos do projeto. Execute o script a partir da linha de comando.
   - `python template.py`

3. **Execução**:
   - Acesse o Amazon Bedrock Prompt Flows pelo console da AWS. Na interface, existe um "chat" em que é possível realizar o teste da solução. 

## Testes
O modelo de self consistency ajuda na acertividade das respostas, mas está muito longe de ser uma técnica perfeita. No geral, os resultados dos testes foram bem abrangentes: Desde respostas unânimes e corretas, a respostas unânimes e incorretas. O que podemos tomar como vantagem dessa técnica sob a de Chain-of-Thought simples são os casos em que a resposta foi correta, mas não unânime. No teste abaixo, por exemplo, a alternativa correta é a letra (E). 

![image](https://github.com/user-attachments/assets/5a09a04e-5e50-4d6c-9358-376ae359892d)

---

**Contato**: Davi Campos (davi08.sc@gmail.com)
