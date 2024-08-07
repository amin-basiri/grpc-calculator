import sys
import grpc

import calculator_pb2 as pb
import calculator_pb2_grpc as rpc


class ClientError(Exception):
    pass


class Client:
    def __init__(self, addr):
        self.chan = grpc.insecure_channel(addr)
        self.stub = rpc.CalculatorStub(self.chan)
        print('connected to %s', addr)

    def close(self):
        self.chan.close()

    def calculate(self, num1: float, num2: float, op):
        request = pb.CalculationRequest(
            num1=num1,
            num2=num2,
            op=op,
        )

        try:
            response = self.stub.calculate(request, timeout=3)
        except grpc.RpcError as err:
            print('start: %s (%s)', err, err.__class__.__mro__)
            raise ClientError(f'{err.code()}: {err.details()}') from err
        return response.result


if __name__ == '__main__':

    client = Client(sys.argv[1])

    try:
        result = client.calculate(
            num1=float(sys.argv[2]),
            op=sys.argv[3],
            num2=float(sys.argv[4]),
        )
        print(f'Result: {result}')
    except ClientError as err:
        raise SystemExit(f'error: {err}')
