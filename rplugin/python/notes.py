import os
import subprocess
import time
from os.path import dirname, join, basename, exists
from subprocess import PIPE

import neovim
from helpers import common


@neovim.plugin
class Notes(object):
    def __init__(self, vim):
        self.vim = vim
        self.editor = common.Editor(vim)

    @neovim.function('ShowDebugMsg', sync=True)
    def show_debug_msg(self, args):
        self.editor.debug_text_right_split(args[0])

    @neovim.function('ShowFilePreview', sync=True)
    def show_file_preview(self, args):
        self.editor.preview_file_right_split(args[0])

    @neovim.command('NotesMarkdownToPdf', sync=False, nargs='*')
    def notes_markdown_to_pdf(self, args):
        in_file = self.editor.get_current_file_path()

        if not os.path.isfile(in_file):
            return

        file_dir = dirname(in_file)
        name, ext = os.path.splitext(basename(in_file))

        if ext != '.md':
            return

        datadir = join(common.root_dir())
        outdir = join(file_dir, 'build')

        if not exists(outdir):
            os.makedirs(outdir)

        outfile_tex = join(outdir, name+'.tex')

        def compile_pdf():
            command = ['latexmk', '-pdf',
                       '-output-directory='+outdir,
                       '-pdflatex="pdflatex -interaction=nonstopmode"',
                       outfile_tex]
            self.exec_or_show_error(command, lambda: self.editor.call(
                'ShowFilePreview', outfile_tex), cwd=file_dir)

        command = ['pandoc', in_file,
                   '-o', outfile_tex,
                   '--template', 'notes',
                   '--data-dir', datadir]
        self.exec_or_show_error(command, compile_pdf())

    def wait_until(self, cond_f, timeout=3, interval=0.1):
        start_time = time.time()
        while not cond_f():
            elapsed_time = time.time() - start_time
            if elapsed_time > timeout:
                return False
            time.sleep(interval)
        return True

    def exec_or_show_error(self, command, success_callback, timeout=8,
                           cwd=None):
        proc = subprocess.Popen(command, stdout=PIPE, stderr=PIPE, cwd=cwd)

        if not self.wait_until(lambda: proc.poll() is not None, timeout):
            proc.kill()
            return

        out, err = proc.communicate()

        debug_msg = """
            returncode: {}
            stderr: {}
            stderr: {}
            """.format(proc.returncode, out, err)

        if proc.returncode == 0:
            success_callback()
        else:
            self.editor.call('ShowDebugMsg', debug_msg)
