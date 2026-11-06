
# Registro de Uso de Inteligência Artificial

Este projeto utilizou ferramentas de IA generativa como apoio técnico e pedagógico para acelerar o estudo, o design do contrato e a estruturação do código da POC em gRPC, conforme permitido nas diretrizes do trabalho.

## 🤖 Ferramentas Utilizadas
- **Assistente IA (Gemini)**: Utilizado para estruturação do contrato Protocol Buffers (`leilao.proto`), suporte na criação da lógica assíncrona/threads para o *Server Streaming* no servidor gRPC, e resolução de erros de ambiente (`PEP 668` e `venv`).

## 🔍 Tarefas em que a IA auxiliou:
1. **Modelagem gRPC**: Definição inicial dos serviços unários (`ConsultarLeilao`, `DarLance`) e de streaming (`AcompanharLeilao`).
2. **Resolução de Problemas**: Orientação sobre o isolamento de pacotes Python no Linux moderno usando ambientes virtuais (`python3 -m venv`).
3. **Documentação**: Apoio na formatação do roteiro da Fase 1 e estruturação inicial do `README.md`.

*Nota: Todo o código gerado foi analisado, testado e validado criticamente pela equipe no laboratório.*
