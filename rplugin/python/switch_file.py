import neovim

@neovim.plugin
class SwitchFile(object):
    def __init__(self, vim):
        self.vim = vim
        self.vim_util = NvimUtil(vim)

    #@neovim.command('SwitchFile', sync=True, nargs='*')
    #def switch_file(self, args):
        #switch_file.main(vim_helper, args)

    @neovim.command('NotesMarkdownToPdf', sync=True, nargs='*')
    def notes_markdown_to_pdf(self, args):
        notes.markdown_to_pdf(self.vim_util, args)

    #@neovim.autocmd('BufEnter', sync=True)
    #def buf_enter(self):
        #pass

