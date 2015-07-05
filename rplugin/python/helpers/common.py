from os.path import join, dirname, realpath


def root_dir():
    return join(dirname(realpath(__file__)), '../../../')


class Editor():
    """
    Wrapper for nvim.
    """
    def __init__(self):
        pass
    def __init__(self, vim):
        self.vim = vim
        self.buffer_to_cursor = {}
        self.buffer_to_view = {}

    def get_current_file_path(self):
        return self.vim.eval("expand('%:p')")

    def get_current_file_type(self):
        return self.vim.eval('&filetype')

    def save_current_buffer(self):
        self.vim.command("w")

    def edit_file(self, path):
        self.vim.command("silent e! {}".format(path))

    def jump_to(self, path):
        fname = self.get_current_file_path()
        fcursor = self.get_cursor()
        self.buffer_to_cursor[fname] = fcursor
        self.buffer_to_view[fname] = self.get_view()

        self.edit_file(path)

        if path in self.buffer_to_cursor:
            self.set_cursor(self.buffer_to_cursor[path])
        if path in self.buffer_to_view:
            self.set_view(self.buffer_to_view[path])

    def get_cursor(self):
        """
        :return: 1-indexed current cursor position.
        """
        row, col = self.vim.current.window.cursor
        return row, col + 1

    def set_cursor(self, row_col):
        self.vim.current.window.cursor = (row_col[0], row_col[1] - 1)

    def get_view(self):
        return self.vim.eval('winsaveview()')

    def set_view(self, view_dict):
        self.vim.eval('winrestview({})'.format(view_dict))

    def get_selection(self):
        buf = self.vim.current.buffer
        row1, col1 = buf.mark('<')
        row2, col2 = buf.mark('>')
        lines = buf[row1 - 1:row2]
        if len(lines) == 1:
            lines[0] = lines[0][col1:col2 + 1]
        else:
            lines[0] = lines[0][col1:]
            lines[-1] = lines[-1][:col2 + 1]
        return lines

    def get_lines(self):
        """
        All lines in current buffer.
        """
        buf = self.vim.current.buffer
        return buf

    def is_current_buffer_modified(self):
        return self.vim.eval('&modified') == 1

    def echo_text(self, string):
        self.vim.command("echo '{}'".format(string.replace("'", r"''")))

    def execute(self, command):
        self.vim.command('silent !' + command)

    def preview_file_right_split(self, filename, buffer_id="preview"):
        win_prev = self.vim.current.window

        w = self.find_window_by_buffer_id(buffer_id)
        if w is None:
            self.vim.command('silent :only')
            self.vim.command('silent :vert belowright vs ' + filename)
            b_new = self.vim.current.buffer
            self.vim.command('set nomodifiable readonly nobuflisted')
            self.assign_id_to_buffer(b_new, buffer_id)
        else:
            self.vim.current.window = w
            self.vim.command('silent e! ' + filename)
            self.vim.command('set nomodifiable readonly nobuflisted')

        self.vim.current.window = win_prev

    def find_buffer_by_id(self, id_str):
        for b in self.vim.buffers:
            if 'buffer_id' in b.vars and b.vars['buffer_id'] == id_str:
                return b
        return None

    def find_window_by_buffer_id(self, id_str):
        for w in self.vim.windows:
            if 'buffer_id' in w.buffer.vars \
                    and w.buffer.vars['buffer_id'] == id_str:
                return w
        return None

    def assign_id_to_buffer(self, buf, id_str):
        buf.vars['buffer_id'] = id_str

    def create_new_buffer(self, id_str):
        b = self.vim.current.buffer
        self.vim.command('silent :enew')
        new_buf = self.vim.current.buffer
        self.vim.current.buffer = b
        self.assign_id_to_buffer(new_buf, id_str)
        return new_buf

    def threadsafe_call(self, *args, **kwargs):
        self.vim.session.threadsafe_call(*args, **kwargs)

    def debug_text_right_split(self, content, buffer_id="debug"):
        b = self.find_buffer_by_id(buffer_id)
        if b is None:
            b = self.create_new_buffer(buffer_id)

        b.options['modifiable'] = True
        b.options['readonly'] = False

        b[:] = content.split()

        b.options['buftype'] = 'nofile'
        b.options['modifiable'] = False
        b.options['readonly'] = True
        b.options['buflisted'] = False

        win = self.vim.current.window

        self.vim.command('silent :only')
        self.vim.command('silent :vert belowright sb ' + str(b.number))

        self.vim.current.window = win

    def call(self, func_name, arg_str):
        return self.vim.eval(r'{}("{}")'.format(
            func_name, str(arg_str).replace('"', r'\"')))
