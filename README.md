
# Addon (mitmproxy): Protobuf decoder for Google Analytics 4

### Feature: decodificar os dados em formato binário presentes em requests do Google Analytics 4 (GA4) realizadas pelo serviço de analytics do Firebase SDK. O Firebase Analytics utiliza o Protocol Buffers para realizar o encode dos dados.

![Decoding Protobuf](https://drive.google.com/uc?id=1P6Flic105VVGMGPnLuvfF0jFLzDsvNGT)

---


## Dependências:
- [mitmproxy](https://mitmproxy.org/)
- [python 3.13](https://www.python.org/)


## Instalação:
Todos os comandos a seguir devem ser executados na raiz do projeto.
### Ambiente virtual e dependências
Clone o repositório e, preferencialmente, crie um ambiente virtual.

Para isso, execute no terminal o comando:

> `python -m venv venv`

Em seguida, ative o ambiente virtual com o comando:

> `source venv/bin/activate`

Com o ambiente virtual ativo, instale as dependências com o comando:

> `pip install -r requirements.txt`

Após instalado todas as dependências, desative e ative novamente o ambiente virtual. É necessário apenas para que as dependências funcionem nos imports do script.
```bash
deactivate
source venv/bin/activate
```

## Como utilizar:

Com o ambiente virtual ativo e as dependências instaladas, você é capaz de utilizar o mitmproxy executando o script *decode_protobuf.py*.

Execute um dos comandos abaixo de acordo com o front-end de sua preferência:

**mitmproxy** is an interactive, SSL/TLS-capable intercepting proxy with a console interface for HTTP/1, HTTP/2, and WebSockets.

> `mitmdproxy -s decode_protobuf.py`

**mitmweb** is a web-based interface for mitmproxy.

> `mitmweb -s decode_protobuf.py`

**mitmdump** is the command-line version of mitmproxy. Think tcpdump for HTTP.

> `mitmdump -s decode_protobuf.py`

---

### Protocol Buffer Compiler [Optional]:
Não é necessário compilar o arquivo .proto que contém as definições de serviços e messagens.
Mas caso queria compilar o arquivo .proto para atualizar os serviçoes e messagens, utilize o protocol buffer compile (protoc).

Acesse a página do [Protocol Buffer Compiler](https://protobuf.dev/installation/) e siga as orientações para baixar a versão mais recente.

Após instalar o protoc e editar/atualizar o arquivo *appanalytics.proto*, exclua o arquivo *appanalytics_pb2.py*.
Execute o seguinte comando para compilar:

> `protoc --python_out=. appanalytics.proto`

Após executar o comando, o arquivo *appanalytics_pb2.py* será criado novamente na raiz do projeto.

O comando anterior teve o argumento *-I* omitido, porque por padrâo aponta para o diretório atual. O argumento *--python_out* também aponta para o diretório atual com o valor '.'.

O arquivo appanalytics.proto é o arquivo presente na raiz do projeto (diretório atual).

### Links úteis:

- [Protocol Buffers Documentation](https://protobuf.dev/): Protocol Buffers are language-neutral, platform-neutral extensible mechanisms for serializing structured data.
- [GA4 Recommended events](https://developers.google.com/analytics/devguides/collection/ga4/reference/events?client_type=gtag): description of GA4 events and parameters.

### Authors
- [@JanioPG](https://github.com/JanioPG)
