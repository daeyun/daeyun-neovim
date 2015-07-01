vim = None
buffer_to_cursor = {}
buffer_to_view = {}


class PythonVimUtil(object):
    @staticmethod
    def get_current_file_path():
        return vim.eval("expand('%:p')")

    @staticmethod
    def get_current_file_type():
        return vim.eval('&filetype')

    @staticmethod
    def save_current_buffer():
        vim.command("w")

    @staticmethod
    def edit_file(path):
        vim.command("silent e! {}".format(path))

    @staticmethod
    def jump_to(path):
        fname = PythonVimUtil.get_current_file_path()
        fcursor = PythonVimUtil.get_cursor()
        buffer_to_cursor[fname] = fcursor
        buffer_to_view[fname] = PythonVimUtil.get_view()

        PythonVimUtil.edit_file(path)

        if path in buffer_to_cursor:
            PythonVimUtil.set_cursor(buffer_to_cursor[path])
        if path in buffer_to_view:
            PythonVimUtil.set_view(buffer_to_view[path])

    @staticmethod
    def get_cursor():
        """
        :return: 1-indexed current cursor position.
        """
        row, col = vim.current.window.cursor
        return row, col + 1

    @staticmethod
    def set_cursor(row_col):
        vim.current.window.cursor = (row_col[0], row_col[1] - 1)

    @staticmethod
    def get_view():
        return vim.eval('winsaveview()')

    @staticmethod
    def set_view(view_dict):
        vim.eval('winrestview({})'.format(view_dict))

    @staticmethod
    def get_selection():
        buf = vim.current.buffer
        row1, col1 = buf.mark('<')
        row2, col2 = buf.mark('>')
        lines = buf[row1 - 1:row2]
        if len(lines) == 1:
            lines[0] = lines[0][col1:col2 + 1]
        else:
            lines[0] = lines[0][col1:]
            lines[-1] = lines[-1][:col2 + 1]
        return lines

    @staticmethod
    def get_lines():
        """
        All lines in current buffer.
        """
        buf = vim.current.buffer
        return buf

    @staticmethod
    def is_current_buffer_modified():
        return vim.eval('&modified') == 1

    @staticmethod
    def echo_text(string):
        vim.command("echo '{}'".format(string.replace("'", r"''")))
