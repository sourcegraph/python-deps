from deps import *
import argparse

def debug():
    import pdb, traceback, code, sys
    def handle_exception(tp, val, tb):  # open up debugger on exception
        traceback.print_tb(tb)
        print 'ERROR:', val
        pdb.post_mortem(tb)
    sys.excepthook = handle_exception

def get_args():
    parser = argparse.ArgumentParser(description='Grab dependencies from a setup.py file')
    parser.add_argument('rootdir', help='path to root project directory')
    parser.add_argument('--debug', action='store_true', help='enable if you want to enable debugging stacktrace')
    parser.add_argument('--all', action='store_true', help='enable if you want to print all deps, not just external')
    return parser.parse_args()

if __name__ == '__main__':
    args = get_args()
    if args.debug:
        print '##### DEBUG ENABLED #####'
        debug()

    deps = external_import_tree_for_project(args.rootdir)

    # deps.print_tree()
    for k in deps.children.keys():
        print k
