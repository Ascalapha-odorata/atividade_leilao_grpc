import grpc
import threading
import sys
import time
import leilao_pb2
import leilao_pb2_grpc

def escutar_notificacoes(stub, id_cliente):
    try:
        stream = stub.AcompanharLeilao(leilao_pb2.AcompanharRequest(id_participante=id_cliente))
        for notif in stream:
            print(f"\n📢 [NOTIFICAÇÃO] {notif.mensagem}")
            print(f"{id_cliente}> ", end="", flush=True)
    except grpc.RpcError as e:
        print(f"\n⚠️ [DESCONECTADO] Conexão com o Leiloeiro perdida: {e.code()}")

def main():
    if len(sys.argv) < 3:
        print("Uso: python cliente.py <IP_DO_SERVIDOR> <SEU_NOME>")
        sys.exit(1)

    ip_servidor = sys.argv[1]
    id_cliente = sys.argv[2]

    channel = grpc.insecure_channel(f'{ip_servidor}:50051')
    stub = leilao_pb2_grpc.ServicoLeilaoStub(channel)

    t = threading.Thread(target=escutar_notificacoes, args=(stub, id_cliente), daemon=True)
    t.start()

    time.sleep(0.5)

    while True:
        print(f"\n--- Menu ({id_cliente}) ---")
        print("1. Consultar Leilão")
        print("2. Dar Lance")
        print("3. Sair")
        opcao = input(f"{id_cliente}> ")

        if opcao == '1':
            res = stub.ConsultarLeilao(leilao_pb2.ConsultaRequest())
            print(f"\nItem: {res.descricao}")
            print(f"Maior Lance: R${res.maior_lance:.2f} ({res.vencedor_atual})")
            print(f"Tempo Restante: {res.tempo_restante_segundos}s")
            print(f"Encerrado: {res.encerrado}")

        elif opcao == '2':
            try:
                valor = float(input("Digite o valor do lance: R$ "))
                res = stub.DarLance(leilao_pb2.LanceRequest(id_participante=id_cliente, valor=valor))
                print(f"-> Resposta: {res.mensagem}")
            except ValueError:
                print("Valor inválido.")

        elif opcao == '3':
            break

if __name__ == '__main__':
    main()