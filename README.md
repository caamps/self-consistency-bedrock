# Framework de Self Consistency para LLMs utilizando o Amazon Bedrock
### Self Consistency 
É uma técnica avançada de engenharia de prompt que se baseia em gerar um número n de diferentes Chain-of-Thought visando resolver um problema e considerar a resposta mais comum como a correta. 

### Amazon Bedrock Prompt flows 
É um recurso do Amazon Bedrock que facilita a criação de workflows envolvendo foundation models (FMs) e outros recursos AWS, permitindo o desenvolvimento de uma solução completa. A ferramenta conta com um editor visual que agiliza o processo. 

### Geral
A ideia do projeto é utilizar o Amazon Bedrock Prompt Flows para aplicar a técnica de Self Consistency. O caso de uso é a resolução de questões de raciocínio lógico de múltipla escolha, como as de vestibulares.
Primeiramente, o flow recebe a pergunta a ser respondida. Essa pergunta é, então, enviada a uma função lambda. Essa função tem acesso a uma base de dados com 10 perguntas do mesmo estilo e suas devidas respostas comentadas passo a passo. O algorítmo escolhe 3 desses 10 pares pergunta-resposta aleatoriamente, e os concatena em um prompt no modelo few-shot CoT. Esse processo acontece 5 vezes, gerando 5 diferentes "paths" para o modelo completar. 
