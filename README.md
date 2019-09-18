# A repository for testing gRPC with gRPC-gateway

## Installation
- Install [`Go` runtime](https://golang.org/)

- Install required packages of [`grpc-gateway`](https://github.com/grpc-ecosystem/grpc-gateway)
    ```bash
    $ go get -u github.com/grpc-ecosystem/grpc-gateway/protoc-gen-grpc-gateway
    $ go get -u github.com/grpc-ecosystem/grpc-gateway/protoc-gen-swagger
    $ go get -u github.com/golang/protobuf/protoc-gen-go
    ```

- Install requirements for Python
    ```bash
    $ pip install -r requirements.txt
    ```

## Usage
- Run code generator (generate `.py` files from `.proto`)
    ```bash
    $ python gen_api.py
    ```

- Run server
    ```bash
    $ python -m src.api.server
    ```

- Run client
    ```bash
    $ python -m src.api.client
    # you will get a response as the following content:
    # Greeter client received: Hello, you
    ```

- Or you can check the response by sending a request as a URL
    - open this link in browser: http://localhost:8000/v1/hello
    
    - Or send a request via `curl`
    ```bash
    $ curl -X POST -s http://localhost:8000/v1/hello
    # you will get a response as the following content (it is binary data):
    # ↑♦      ♦ @   ♣ @   ♠    □♥     ♦     ?  ♠
    ```
