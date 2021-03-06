import grpc
from concurrent import futures
import MongoUtils

import DbAction_pb2
import DbAction_pb2_grpc

class CustomReplicationServicer(DbAction_pb2_grpc.ReplicationServicer):

    def __init__(self):
        super().__init__()
        self.mongo_service = MongoUtils.MongoService()

    def propogate(self, request_iterator, context):
        print(' started proceesing ')
        for db_action in request_iterator:
            self.mongo_service.update(db_action)
        print(' completed proceesing ')
        response = DbAction_pb2.ExecutionResponse(status='COMPLETED')
        return response


def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    DbAction_pb2_grpc.add_ReplicationServicer_to_server(CustomReplicationServicer(), server)
    server.add_insecure_port('[::]:50085')
    server.start()
    print(' server up and running ')
    server.wait_for_termination()

if __name__ == '__main__':
    serve()


