# --------------------------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for license information.
# --------------------------------------------------------------------------------------------

"""
Script to build all modules that can be used to install a fully self-contained instance of the CLI.
"""

from __future__ import print_function

import os
import sys
import tempfile
import subprocess


def _error_exit(msg):
    print('ERROR: '+msg, file=sys.stderr)
    sys.exit(1)


def _print_status(msg=''):
    print('-- '+msg)


def _get_tmp_dir():
    return tempfile.mkdtemp()


def _get_tmp_file():
    return tempfile.mkstemp()[1]


def _exec_command(command_list, cwd=None, stdout=None):
    """Returns True if the command was executed successfully"""
    try:
        _print_status('Executing {}'.format(command_list))
        subprocess.check_call(command_list, stdout=stdout, cwd=cwd)
        return True
    except subprocess.CalledProcessError as err:
        print(err, file=sys.stderr)
        return False


def _build_package(path_to_package, dist_dir):
    cmd_success = _exec_command(['python', 'setup.py', 'bdist_wheel', '-d', dist_dir], cwd=path_to_package)
    if not cmd_success:
        _error_exit('Error building {}.'.format(path_to_package))


def build_packages(clone_root, dist_dir):
    packages_to_build = [
        os.path.join(clone_root, 'src/common_modules/azdos-cli-common'),
        os.path.join(clone_root, 'src/common_modules/azdos-cli-admin-common'),
        os.path.join(clone_root, 'src/common_modules/azdos-cli-build-common'),
        os.path.join(clone_root, 'src/common_modules/azdos-cli-code-common'),
        os.path.join(clone_root, 'src/common_modules/azdos-cli-package-common'),
        os.path.join(clone_root, 'src/common_modules/azdos-cli-team-common'),
        os.path.join(clone_root, 'src/common_modules/azdos-cli-work-common'),
        os.path.join(clone_root, 'src/command_modules/azdos-cli-admin'),
        os.path.join(clone_root, 'src/command_modules/azdos-cli-build'),
        os.path.join(clone_root, 'src/command_modules/azdos-cli-code'),
        os.path.join(clone_root, 'src/command_modules/azdos-cli-package'),
        os.path.join(clone_root, 'src/command_modules/azdos-cli-team'),
        os.path.join(clone_root, 'src/command_modules/azdos-cli-work'),
        os.path.join(clone_root, 'src/azdos-cli'),
    ]

    for p in packages_to_build:
        setup_path = os.path.join(p, 'setup.py')
        if os.path.isfile(setup_path):
            _build_package(p, dist_dir)
        else:
            print('Failed to find file: ' + setup_path)
            exit(1)


if __name__ == '__main__':
    if len(sys.argv) == 1:
        raise ValueError('Please provide temporary path for local built packages')
    dist_dir = sys.argv[1]
    clone_root = sys.argv[2]
    build_packages(clone_root, dist_dir)
    print("package were built to {}".format(dist_dir))
    print("Done.")
