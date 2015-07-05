import common
import shutil
import time
from os.path import join, isdir, isfile
from nose.tools import eq_ as eq, ok_ as ok


class TestNotes():
    def setup(self):
        self.vim = common.setup()
        self.resources_dir = common.resources_dir()

        self.build_dir = join(self.resources_dir, 'build')
        shutil.rmtree(self.build_dir, ignore_errors=True)

    def teardown(self):
        common.teardown(self.vim)
        shutil.rmtree(self.build_dir, ignore_errors=True)

    def test_does_nothing(self):
        eq(1, len(self.vim.buffers))
        self.vim.command('NotesMarkdownToPdf')
        eq(1, len(self.vim.buffers))

    def test_creates_directory(self):
        ok(not isdir(self.build_dir))

        mkd_file = join(self.resources_dir, 'mkd_math_simple.md')
        self.vim.command('edit {}'.format(mkd_file))
        self.vim.command('NotesMarkdownToPdf')

        ok(common.wait_until(lambda: isdir(self.build_dir)))

    def test_creates_tex(self):
        mkd_file = join(self.resources_dir, 'mkd_math_simple.md')
        self.vim.command('edit {}'.format(mkd_file))
        self.vim.command('NotesMarkdownToPdf')

        ok(common.wait_until(lambda: isfile(join(self.build_dir,
                                                 'mkd_math_simple.tex'))))

    def test_opens_window(self):
        self.vim.command('edit {}'.format(join(self.resources_dir,
                                               'mkd_math_simple.md')))

        eq(1, len(self.vim.windows))
        eq(1, len(self.vim.buffers))

        self.vim.command('NotesMarkdownToPdf')

        ok(common.wait_until(lambda: 2 == len(self.vim.windows),
                             timeout=5,
                             interval=0.3))
        eq(2, len(self.vim.buffers))

    def test_does_nothing_with_unsaved_file(self):
        self.vim.command('edit {}'.format(join(self.resources_dir,
                                               'mkd_math_nonexistent.md')))

        eq(1, len(self.vim.windows))
        eq(1, len(self.vim.buffers))

        self.vim.command('NotesMarkdownToPdf')
        time.sleep(2)

        ok(not isdir(self.build_dir))
        eq(1, len(self.vim.buffers))
        eq(1, len(self.vim.windows))
