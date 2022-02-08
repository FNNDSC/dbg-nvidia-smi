#!/usr/bin/env python
import sys
import shutil
import argparse
import subprocess as sp
from pathlib import Path
from chris_plugin import chris_plugin

examples = f"""
    singularity exec --nv docker://fnndsc/dbg-nvidia-smi {sys.argv[0]} /tmp

    docker run --rm --gpus all ghcr.io/fnndsc/dbg-nvidia-smi {sys.argv[0]} /tmp

    podman run --rm --security-opt=no-new-privileges --cap-drop=ALL \
            --security-opt label=type:nvidia_container_t \
            ghcr.io/fnndsc/dbg-nvidia-smi {sys.argv[0]} /tmp
"""

parser = argparse.ArgumentParser(
    description='ChRIS fs plugin wrapper for nvidia-smi',
    formatter_class=argparse.ArgumentDefaultsHelpFormatter
)
parser.add_argument('-q', '--query-gpu', type=str, dest='query_gpu',
                    default='index,name,memory.total,driver_version',
                    help='Information about GPU.')


@chris_plugin(
    title='NVIDIA-SMI Wrapper',
    category='Troubleshooting',
    min_gpu_limit=1,
    max_gpu_limit=9999,  # required by CUBE @ b3b9996
    parser=parser
)
def main(options: argparse.Namespace, outputdir: Path):
    if not shutil.which('nvidia-smi'):
        print(
            'nvidia-smi not found. Make sure your container runtime\n'
            'is configured with container support, e.g.\n\n'
            + examples
        )
        sys.exit(1)

    output_file = outputdir / 'gpus.csv'
    cmd = [
        'nvidia-smi', '--format=csv',
        f'--filename={output_file}', f'--query-gpu={options.query_gpu}'
    ]
    print(' '.join(cmd))
    sp.run(cmd, check=True)


if __name__ == '__main__':
    main()
