from __future__ import print_function

import grpc

from .protos import helloworld_pb2, helloworld_pb2_grpc


def run():
    channel = grpc.insecure_channel('localhost:8000')
    stub = helloworld_pb2_grpc.GreeterStub(channel)
    response = stub.SayHello(helloworld_pb2.HelloRequest(name='you'))
    print("Greeter client received: " + response.message)


if __name__ == '__main__':
    run()
