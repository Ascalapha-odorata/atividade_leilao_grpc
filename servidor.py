import grpc
from concurrent import futures
import time
import threading
import leilao_pb2
import leilao_pb2_grpc

class LeiloeiroServicer(leilao_pb2_grpc.ServicoLeilaoServicer):
    def __init__(self, descricao, lance_minimo, duracao_segundos):
        self.descricao = descricao
        self.maior_lance = lance_minimo
        self.vencedor = "Nenhum"
        self.tempo_fim = time.time() + duracao_segundos
        self.encerrado = False
        
        self.lock = threading.Lock() # Protege contra concorrência (RE3)
        self.listeners = []         # Lista de streams para notificar clientes (RF4)

    def _tempo_restante(self):
        restante = int(self.tempo_fim - time.time())
        return max(0, restante)

    def _verificar_encerramento(self):
        if time.time() >= self.tempo_fim and not self.encerrado:
            self.encerrado = True
            notif = leilao_pb2.NotificacaoLeilao(
                tipo=leilao_pb2.LEILAO_ENCERRADO,
                valor=self.maior_lance,
                participante=self.vencedor,
                mensagem=f"Leilão encerrado! Vencedor: {self.vencedor} com R${self.maior_lance:.2f}"
            )
            self._notificar_todos(notif)

    def _notificar_todos(self, notificacao):
        for queue in self.listeners:
            queue.append(notificacao)

    def ConsultarLeilao(self, request, context):
        self._verificar_encerramento()
        with self.lock:
            return leilao_pb2.EstadoLeilao(
                descricao=self.descricao,
                maior_lance=self.maior_lance,
                vencedor_atual=self.vencedor,
                tempo_restante_segundos=self._tempo_restante(),
                encerrado=self.encerrado
            )

    def DarLance(self, request, context):
        self._verificar_encerramento()
        
        with self.lock:
            if self.encerrado:
                return leilao_pb2.LanceResponse(
                    aceito=False,
                    mensagem="Leilão já está encerrado.",
                    maior_lance_atual=self.maior_lance
                )
            
            if request.valor > self.maior_lance:
                self.maior_lance = request.valor
                self.vencedor = request.id_participante
                
                notif = leilao_pb2.NotificacaoLeilao(
                    tipo=leilao_pb2.NOVO_MAIOR_LANCE,
                    valor=self.maior_lance,
                    participante=self.vencedor,
                    mensagem=f"Novo maior lance: R${self.maior_lance:.2f} por {self.vencedor}"
                )
                self._notificar_todos(notif)
                
                return leilao_pb2.LanceResponse(
                    aceito=True,
                    mensagem="Lance aceito com sucesso!",
                    maior_lance_atual=self.maior_lance
                )
            else:
                return leilao_pb2.LanceResponse(
                    aceito=False,
                    mensagem=f"Lance recusado. Deve ser maior que R${self.maior_lance:.2f}",
                    maior_lance_atual=self.maior_lance
                )

    def AcompanharLeilao(self, request, context):
        print(f"[SERVIDOR] Participante {request.id_participante} conectou ao stream.")
        minha_fila = []
        self.listeners.append(minha_fila)

        try:
            while True:
                self._verificar_encerramento()
                if minha_fila:
                    notif = minha_fila.pop(0)
                    yield notif
                time.sleep(0.2)
        except Exception:
            print(f"[SERVIDOR] Participante {request.id_participante} desconectou.")
        finally:
            if minha_fila in self.listeners:
                self.listeners.remove(minha_fila)

def executar():
    servidor = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    leiloeiro = LeiloeiroServicer(
        descricao="Notebook Dell XPS 15",
        lance_minimo=1000.0,
        duracao_segundos=300 # 5 minutos para teste
    )
    leilao_pb2_grpc.add_ServicoLeilaoServicer_to_server(leiloeiro, servidor)
    
    servidor.add_insecure_port('0.0.0.0:50051')
    servidor.start()
    print("[SERVIDOR] Leiloeiro rodando na porta 50051...")
    servidor.wait_for_termination()

if __name__ == '__main__':
    executar()