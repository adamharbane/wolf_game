import grpc
import game_engine_pb2
import game_engine_pb2_grpc

# Adresse du moteur de jeu
GAME_ENGINE_HOST = 'localhost:50051'

def send_move(player_id, game_id, row, col):
    """Appelle le moteur de jeu via gRPC pour exécuter un déplacement"""
    try:
        with grpc.insecure_channel(GAME_ENGINE_HOST) as channel:
            stub = game_engine_pb2_grpc.GameEngineStub(channel)
            request = game_engine_pb2.MoveRequest(
                player_id=player_id,
                game_id=game_id,
                row=row,
                col=col
            )
            response = stub.Move(request)
            return response.result
    except grpc.RpcError as e:
        print(f"[gRPC] Erreur lors de send_move : {e}")
        return "KO"
    except Exception as e:
        print(f"[gRPC] Erreur inattendue : {e}")
        return "KO"

def get_game_status(game_id):
    """Exemple d'appel pour obtenir le statut de la partie"""
    try:
        with grpc.insecure_channel(GAME_ENGINE_HOST) as channel:
            stub = game_engine_pb2_grpc.GameEngineStub(channel)
            request = game_engine_pb2.GameStatusRequest(game_id=game_id)
            response = stub.GetGameStatus(request)
            return {
                "status": response.status,
                "round": response.current_round
            }
    except grpc.RpcError as e:
        print(f"[gRPC] Erreur lors de get_game_status : {e}")
        return None
