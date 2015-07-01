import os
import re

test_pattern = re.compile(r'^test[_\-]?(.+?)$|^(.+?)[_\-]?test$')


def main(v, args):
    fullpath = v.get_current_file_path()
    preext, ext = os.path.splitext(fullpath)
    basename = os.path.basename(preext)
    dirname = os.path.dirname(preext)

    hdr_ext = set(['.h', '.hpp'])
    src_ext = set(['.cc', '.c', '.cpp'])

    if len(args) > 0 and args[0] == 'test':
        for name in [basename+'_test', basename+'Test', 'test_'+basename]:
            preext = os.path.join(dirname, name)
            for target in (preext+ext for ext in src_ext):
                if os.path.isfile(target):
                    v.jump_to(target)
                    return

    else:
        if ext in hdr_ext:
            target_ext = src_ext
        elif ext in src_ext:
            target_ext = hdr_ext
        else:
            return

        test_name = test_pattern.match(basename)
        if test_name:
            test_name = next(x for x in test_name.groups() if x is not None)
            preext = os.path.join(dirname, test_name)

        for target in (preext+ext for ext in target_ext):
            if os.path.isfile(target):
                v.jump_to(target)
                return
