#!/usr/bin/env python
import sys
import shutil
import argparse
import os
import subprocess as sp
from pathlib import Path
from chris_plugin import chris_plugin


from importlib_metadata import distribution
dist = distribution('dbg-nvidia-smi')

__version__ = dist.version
__name__    = dist.name

DISPLAY_TITLE = r"""
     _ _                             _     _ _                            _
    | | |                           (_)   | (_)                          (_)
  __| | |__   __ _ ______ _ ____   ___  __| |_  __ _ ______ ___ _ __ ___  _
 / _` | '_ \ / _` |______| '_ \ \ / / |/ _` | |/ _` |______/ __| '_ ` _ \| |
| (_| | |_) | (_| |      | | | \ V /| | (_| | | (_| |      \__ \ | | | | | |
 \__,_|_.__/ \__, |      |_| |_|\_/ |_|\__,_|_|\__,_|      |___/_| |_| |_|_|
              __/ |
             |___/


"""

package_argSynopsisCore = """

        [--nvidia-smi]
        Call `nvidia-smi` without any query parameters. This is probably
        what you might be expecting to see.

        [--query-gpu <query>]
        Default is "index,name,memory.total,driver_version" -- the parameters
        of the GPU to query, saved in csv format.

        [--man]
        Show this help.

        [--report <filename>]
        The report filename. Default is 'gpus.csv'.
        NOTE THIS IS A FILE INSIDE THE CONTAINER SPACE! If you want to access
        this from the host, be sure to use an appropriate volume mount.

        [--cat]
        If specified, then "cat" the report file, i.e. echo to terminal.

"""

examples = f"""
    singularity exec --nv docker://fnndsc/dbg-nvidia-smi                    \\
        {sys.argv[0]} /tmp --cat

    # note the "--gpus all" for the docker case
    docker run --rm --gpus all ghcr.io/fnndsc/dbg-nvidia-smi                \\
        {sys.argv[0]} /tmp  --cat

    podman run --rm --security-opt=no-new-privileges --cap-drop=ALL         \\
        --security-opt label=type:nvidia_container_t                        \\
        ghcr.io/fnndsc/dbg-nvidia-smi                                       \\
        {sys.argv[0]} /tmp  --cat
"""

desc = f"""

    DESCRIPTION

                    Report on available GPU(s) using
                            -- nvidia-smi --

    This is a rather simple ChRIS FS plugin container that wraps around
    `nvidia-smi` to provide information on GPU(s) visibility to this
    container -- and hence to other containers running on this host.

    Since this is an FS type plugin, it requires one positional argument
    denoting an "output" directory. The report from this plugin is stored
    in a file, typically called 'gpus.csv' in the output directory.

    Note that the entrypoint is "nvidia-smi-wrapper".


    ARGUMENTS """ + package_argSynopsisCore + """

    EXAMPLES

""" + examples

def synopsis():
    return(DISPLAY_TITLE + desc)


parser = argparse.ArgumentParser(
    description='ChRIS fs plugin wrapper about nvidia-smi',
    formatter_class=argparse.ArgumentDefaultsHelpFormatter
)
parser.add_argument('-q', '--query-gpu',
                    type    = str,
                    dest    = 'query_gpu',
                    default = 'index,name,memory.total,driver_version',
                    help    = 'Return information about GPU(s) available to the container.')
parser.add_argument("--cat",
                    help    = "cat",
                    dest    = 'cat',
                    action  = 'store_true',
                    default = False)
parser.add_argument("--man", "-x",
                    help    = "man",
                    dest    = 'man',
                    action  = 'store_true',
                    default = False)
parser.add_argument("--nvidia-smi",
                    help    = "nvidia_smi",
                    dest    = 'nvidia_smi',
                    action  = 'store_true',
                    default = False)
parser.add_argument('--report',
                    type    = str,
                    dest    = 'report',
                    default = 'gpus.csv',
                    help    = 'Report filename.')
parser.add_argument('--version',
                    help    = 'if specified, print version number',
                    dest    = 'b_version',
                    action  = 'store_true',
                    default = False)

@chris_plugin(
    title           = 'NVIDIA-SMI Wrapper',
    category        = 'Troubleshooting',
    min_gpu_limit   = 1,
    max_gpu_limit   = 9999,  # required by CUBE @ b3b9996
    parser          = parser
)
def main(options: argparse.Namespace, outputdir: Path):

    if options.man:
        print(synopsis())
        sys.exit(1)

    if options.b_version:
        print("Name:    %s\nVersion: %s" % (__name__, __version__))
        sys.exit(1)

    if not shutil.which('nvidia-smi'):
        print(
            'nvidia-smi not found. Make sure your container runtime\n'
            'is configured with container support, e.g.\n\n'
            + examples
        )
        sys.exit(1)

    output_file = outputdir / options.report
    if options.nvidia_smi:
        cmd = ['nvidia-smi', f'--filename={output_file}']
    else:
        cmd = [
        'nvidia-smi', '--format=csv',
        f'--filename={output_file}', f'--query-gpu={options.query_gpu}'
    ]
    print(' '.join(cmd))
    sp.run(cmd, check=True)

    if options.cat:
        with open(output_file, 'r') as f:
            print(f.read())

if __name__ == '__main__':
    main()
