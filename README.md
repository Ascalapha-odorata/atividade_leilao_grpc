# 🏛️ Sistema de Leilão Distribuído com gRPC

Trabalho prático da disciplina de Sistemas Distribuídos e Computação Paralela

Prova de Conceito (POC) de comunicação e integração de sistemas distribuídos utilizando gRPC (Protocol Buffers sobre HTTP/2).

---

## 👥 Integrantes e Divisão de Tarefas
* **Lorena Gaiotti**: Configuração do ambiente virtual Python (`venv`), gerenciamento de dependências e modelagem do contrato gRPC (`leilao.proto`).
* **Priscilla de Souza Jardim**: Implementação da lógica do Servidor/Leiloeiro (`servidor.py`), tratamento de exclusão mútua local com `threading.Lock` e *Server Streaming* de notificações.
* **Isabel Cavalcante Motta**: Implementação da lógica do Cliente/Participante (`cliente.py`), interface de linha de comando (CLI) interativa e condução dos testes em múltiplas máquinas e cenários de falha.

---

## 📋 Arquitetura da POC e Paradigma de Comunicação

O projeto explora a comunicação entre processos por meio do paradigma **Chamada Remota de Procedimento (RPC)** com a tecnologia **gRPC**:

* **Contrato Estrito**: A interface do serviço e os tipos de dados são formalmente definidos no arquivo `leilao.proto` usando **Protocol Buffers**.
* **Transporte**: Executado sobre **HTTP/2**, permitindo multiplexação de requisições sobre uma única conexão TCP.
* **Padrões de Comunicação Utilizados**:
  * **Unário (Requisição/Resposta)**:
    * `ConsultarLeilao`: O cliente solicita o estado atual do leilão (item, tempo restante, maior lance).
    * `DarLance`: O participante envia um lance e recebe a confirmação síncrona de aceite ou recusa.
  * **Server Streaming (Notificação Push)**:
    * `AcompanharLeilao`: O cliente estabelece um fluxo contínuo de escuta. Sempre que um novo maior lance é aceito ou o leilão expira, o servidor envia eventos em tempo real a todos os participantes conectados.

---

## 📄 Formato das Mensagens (`leilao.proto`)

```protobuf
syntax = "proto3";

package leilao;

service ServicoLeilao {
  rpc ConsultarLeilao (ConsultaRequest) returns (EstadoLeilao);
  rpc DarLance (LanceRequest) returns (LanceResponse);
  rpc AcompanharLeilao (AcompanharRequest) returns (stream NotificacaoLeilao);
}

message ConsultaRequest {}

message AcompanharRequest {
  string id_participante = 1;
}

message EstadoLeilao {
  string descricao = 1;
  double maior_lance = 2;
  string vencedor_atual = 3;
  int64 tempo_restante_segundos = 4;
  bool encerrado = 5;
}

message LanceRequest {
  string id_participante = 1;
  double valor = 2;
}

message LanceResponse {
  bool aceito = 1;
  string mensagem = 2;
  double maior_lance_atual = 3;
}

enum TipoNotificacao {
  NOVO_MAIOR_LANCE = 0;
  LEILAO_ENCERRADO = 1;
}

message NotificacaoLeilao {
  TipoNotificacao tipo = 1;
  double valor = 2;
  string participante = 3;
  string mensagem = 4;
}
