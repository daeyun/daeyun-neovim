import neovim
import python_vim_util
from python_vim_util import PythonVimUtil as vim_helper
from plugins import switch_file


@neovim.plugin
class DaeyunNeovim(object):
    def __init__(self, vim):
        self.vim = vim
        python_vim_util.vim = vim

    @neovim.command('SwitchFile', sync=True, nargs='*')
    def switch_file(self, args):
        switch_file.main(vim_helper, args)

    @neovim.autocmd('BufEnter', sync=True)
    def buf_enter(self):
        pass
