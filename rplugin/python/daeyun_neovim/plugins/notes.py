import os
import threading
import subprocess
from subprocess import Popen
import neovim

@neovim.plugin
class DaeyunNeovim(object):
    def __init__(self, vim):
        self.vim = vim

    @neovim.command('hihi', sync=True, nargs='*')
    def notes_markdown_to_pdf(self, args):
        pass

    @neovim.command('AsyncHello', sync=True)
    def hello():
        pass


def async_exec(command, on_done):
    def run_in_thread(on_done, command):
        proc = Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        out, err = proc.communicate()
        callback_args = {
            'out': out,
            'err': err,
            'returncode': proc.returncode,
        }
        on_done(callback_args)
        return

    thread = threading.Thread(target=run_in_thread, args=(on_done, command))
    thread.start()
    return thread


def markdown_to_pdf(v, args):
    filename = v.get_current_file_path()
    dirname = os.path.dirname(filename)

    name, ext = os.path.splitext(filename)

    if ext != '.md':
        return

    name = os.path.basename(name)

    datadir = os.path.join(os.path.dirname(os.path.realpath(__file__)),
                           '../../../../')

    outdir = os.path.join(dirname, 'build')

    if not os.path.exists(outdir):
        os.makedirs(outdir)

    outfile = os.path.join(dirname, 'build', name+'.tex')

    command = ['pandoc', filename,
               '-o', outfile,
               '--template', 'notes',
               '--data-dir', datadir]

    def on_done(args):
        if args['returncode'] == 0 and os.path.exists(outfile):
            v.threadsafe_call(v.preview_file_right_split, outfile)
        else:
            v.threadsafe_call(v.debug_text_right_split, args['stderr'])

    async_exec(command, on_done)
