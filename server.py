import sys
import grpc
from grpc_reflection.v1alpha import reflection
from concurrent.futures import ThreadPoolExecutor

import calculator_pb2 as pb
import calculator_pb2_grpc as rpc


class CalculatorService(rpc.CalculatorServicer):
    def calculate(self, request, context):
        response = 0

        if request.op == 0:
            response = request.num1 + request.num2
        elif request.op == 1:
            response = request.num1 - request.num2
        elif request.op == 2:
            response = request.num1 * request.num2
        elif request.op == 3:
            response = request.num1 / request.num2
        else:
            context.set_code(grpc.StatusCode.UNIMPLEMENTED)
            context.set_details("Invalid operation")

        return pb.CalculationResponse(result=response)


if __name__ == '__main__':
    server = grpc.server(ThreadPoolExecutor())
    rpc.add_CalculatorServicer_to_server(CalculatorService(), server)

    names = (
        pb.DESCRIPTOR.services_by_name['Calculator'].full_name,
        reflection.SERVICE_NAME,
    )
    reflection.enable_server_reflection(names, server)

    server.add_insecure_port(f'[::]:{sys.argv[1]}')
    server.start()

    print(f"Server started on 0.0.0.0:{sys.argv[1]} ...")
    server.wait_for_termination()
