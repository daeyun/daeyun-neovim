import os
import sys
import neovim
import tempfile
import time
import subprocess
from subprocess import Popen, PIPE
from os.path import join, dirname, realpath
import random
import string


def init_vim(path):
    vim = neovim.attach('socket', path=path)
    if sys.version_info >= (3, 0):
        vim = vim.with_hook(neovim.DecodeHook())
    return vim


def root_dir():
    return join(dirname(realpath(__file__)), '../../../')


def resources_dir():
    return join(dirname(realpath(__file__)), 'resources')


def wait_until(cond_f, timeout=3, interval=0.1):
    start_time = time.time()
    while not cond_f():
        elapsed_time = time.time() - start_time
        if elapsed_time > timeout:
            return False
        time.sleep(interval)
    return True


def setup():
    """
    Returns tuple (vim, process).
    """
    socket_file = '/tmp/nvim_' + next(tempfile._get_candidate_names())
    log_file = join(root_dir(), 'logs', 'test.log')

    os.system(
        "NVIM_LISTEN_ADDRESS={} "
        "NNVIM_PYTHON_LOG_LEVEL=DEBUG "
        "NVIM_PYTHON_LOG_FILE={} "
        "nvim --headless "
        "-c 'set noswapfile' -i NONE &".format(socket_file, log_file)
    )

    if not wait_until(lambda: os.path.exists(socket_file)):
        raise RuntimeError('Socket file not available: {}' .format(socket_file))

    vim = init_vim(socket_file)
    vim._socket_file = socket_file
    return vim


def teardown(vim):
    vim.quit()
    os.remove(vim._socket_file)
