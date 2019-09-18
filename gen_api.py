import glob
import os
import os.path as osp
from subprocess import Popen, PIPE
import shlex
import sys

HOME = os.path.expanduser('~')
BIN = os.path.join(HOME, 'bin')
PROTOC_JS_PATH = os.path.join(BIN, 'protoc')

def check_grpc_plugin_installed():
    try:
        from grpc.tools import protoc
        del protoc
    except ImportError as ex:
        ex.msg += (
            '\nTo run this script to build API, `grpc-tools` is required.\n'
            'Please install `grpc-tools` through `$ pip install grpc-tools`.'
        )
        raise ex

def hotfix_for_generated_grpc_file(fn):
    import re
    regex = re.compile('^(import \w*_pb2 as \w*__pb2)')
    with open(fn, 'r') as f:
        content = f.readlines()

    for i, line in enumerate(content):
        content[i] = regex.sub('{}\g<1>'.format('from . '), line)

    with open(fn, 'w') as f:
        f.write(''.join(content))


def hotfix_for_generated_pb2_file(fn):
    import re
    regex = re.compile('^(import \w*_pb2 as \w*__pb2)')
    with open(fn, 'r') as f:
        content = f.readlines()

    for i, line in enumerate(content):
        content[i] = regex.sub('{}\g<1>'.format('from . '), line)

    with open(fn, 'w') as f:
        f.write(''.join(content))


def gen_proto_api():
    this_dir = os.path.abspath(os.path.dirname(__file__))
    check_grpc_plugin_installed()
    dir_src = osp.join(this_dir, 'src', 'api', 'protos')
    dir_out = osp.join(this_dir, 'src', 'api', 'protos')
    proto_files = glob.glob(os.path.join(dir_src, '*.proto'))

    if len(proto_files) == 0:
        raise RuntimeError('No .proto file is available in given directory.')

    # NOTE: files required by GO should locate in `/usr/local/include`
    # https://github.com/grpc-ecosystem/grpc-gateway/issues/574#issuecomment-376018797
    from grpc_tools import _proto
    DIR_PROTOC_INCLUDE = _proto.__path__._path[0]
    GOPATH = os.environ['GOPATH']
    GOPATH_SRC = osp.normpath(osp.join(GOPATH, 'src'))
    DIR_GW_GOOGLEAPIS = osp.normpath(osp.join(GOPATH, 'src/github.com/grpc-ecosystem/grpc-gateway/third_party/googleapis'))
    gateway_flag = (
        '-I. -I{DIR_PROTOC_INCLUDE} -I{GOPATH_SRC} -I{DIR_GW_GOOGLEAPIS}'.format(
            DIR_PROTOC_INCLUDE=DIR_PROTOC_INCLUDE, GOPATH_SRC=GOPATH_SRC, DIR_GW_GOOGLEAPIS=DIR_GW_GOOGLEAPIS
    ))

    cmds = [
    # (
    #     'python -m grpc.tools.protoc -I {dir_src} --python_out={proto_out} '
    #     '--grpc_python_out={grpc_out} {proto_files}'.format(
    #         dir_src=dir_src, proto_out=dir_out, grpc_out=dir_out,
    #         proto_files=' '.join(proto_files)
    # )),
    (
        'python -m grpc.tools.protoc {gateway_flag} -I {dir_src} --python_out={proto_out} '
        '--grpc_python_out={grpc_out} {proto_files}'.format(
            dir_src=dir_src, proto_out=dir_out, grpc_out=dir_out,
            proto_files=' '.join(proto_files), gateway_flag=gateway_flag
    )),
    # (
    #     # using protc-js to generate client code for javascript
    #     '{protoc_js} -I {dir_src} --js_out=import_style=common.js:{proto_out} '
    #     '--grpc-web_out=import_style=commonjs,mode=grpcwebtext:{grpc_out} {proto_files}'.format(
    #         protoc_js=PROTOC_JS_PATH, dir_src=dir_src, proto_out=dir_out,
    #         grpc_out=dir_out, proto_files=' '.join(proto_files)
    #     )
    # )
    ]

    generated_files = []

    for cmd in cmds:
        try:
            proc = Popen(shlex.split(cmd, posix='win' not in sys.platform))
            proc.wait()
        except KeyboardInterrupt:
            proc.kill()

    generated_files = glob.glob(os.path.join(dir_out, '*grpc.py'))
    for fn in generated_files:
        hotfix_for_generated_grpc_file(fn)

    generated_files = glob.glob(os.path.join(dir_out, '*pb2.py'))
    for fn in generated_files:
        hotfix_for_generated_pb2_file(fn)


if __name__ == '__main__':
    gen_proto_api()
