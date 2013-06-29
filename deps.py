import ast
import sys
import os.path
import pkgutil
from collections import defaultdict

class Node(object):
    @classmethod
    def new_nonleaf(cls):
        return Node(False, defaultdict(Node.new_nonleaf))

    def __init__(self, isleaf, children_dict):
        self.children = children_dict
        self.isleaf = isleaf

    def __key(self):
        return (self.children, self.isleaf)

    def __eq__(self, other):
        return self.__key() == other.__key()

    def __hash__(self):
        return hash(self.__key())

    def to_dict(self):
        return {
            'children': { k: v.to_dict() for k, v in self.children.iteritems() },
            'isleaf': str(self.isleaf),
        }

    def leaves(self):
        for k, child in self.children.iteritems():
            if child.isleaf:
                yield k
            for l in child.leaves():
                yield k + '.' + l

    def add_path(self, path):   # path.in.this.form
        if len(path) == 0: return
        components = path.split('.')
        node = self
        for component in components:
            node = node.children[component]
        node.isleaf = True  # set leaf

    def remove_path_and_children(self, path):
        if len(path) == 0: return
        components = path.split('.')
        prev = None
        node = self
        for component in components:
            prev = node
            node = node.children[component]
        if components[-1] in prev.children:
            del prev.children[components[-1]]

    def print_tree(self):
        self.print_tree_prefix('')

    def print_tree_prefix(self, prefix):
        for k, v in self.children.iteritems():
            if v.isleaf is True:
                print '%s%s [leaf]' % (prefix, k)
            else:
                print '%s%s' % (prefix, k)
            v.print_tree_prefix('  ' + prefix)

class DepVisitor(ast.NodeVisitor):
    def __init__(self, deptree):
        self.deptree = deptree

    def visit_Import(self, node):
        for alias in node.names:
            self.deptree.add_path(alias.name)

    def visit_ImportFrom(self, node):
        for alias in node.names:
            impt = '%s.%s' % (node.module, alias.name)
            self.deptree.add_path(impt)

# This treats all directories as packages
def __modules_with_root_module_path(path):
    modules = []
    if os.path.isfile(path) and os.path.splitext(path)[1] == '.py' and os.path.basename(path) != '__init__.py':
        name = os.path.splitext(os.path.basename(path))[0]
        modules.append(name)
    elif os.path.isdir(path):
        pkg_name = os.path.basename(path)
        modules.append(pkg_name)
        for ff in os.listdir(path):
            modules.extend(['.'.join([pkg_name, m]) for m in __modules_with_root_module_path(os.path.join(path, ff))])
    return modules

def paths_to_root_modules(rootpath):
    # Note: does not follow symbolic links
    if os.path.isfile(rootpath) and os.path.splitext(rootpath)[1] == '.py':
        return [rootpath]
    if os.path.exists(os.path.join(rootpath, '__init__.py')):
        return [rootpath]
    if os.path.isfile(rootpath) or os.path.islink(rootpath):
        return []

    module_paths = []
    for ff in os.listdir(rootpath):
        subpath = os.path.join(rootpath, ff)
        module_paths.extend(paths_to_root_modules(subpath))
    return module_paths

def modules_defined_in(path):
    rootpaths = paths_to_root_modules(path)
    modules = []
    for r in rootpaths:
        modules.extend(__modules_with_root_module_path(r))
    return modules

def root_modules_defined_in(path):
    rootpaths = paths_to_root_modules(path)
    rootmodules = []
    for r in rootpaths:
        rootmodules.append(os.path.splitext(os.path.basename(r))[0])
    return rootmodules

def add_imports_for_file_to_tree(filename, deptree):
    with open(filename) as ff:
        root = ast.parse(ff.read())
        visitor = DepVisitor(deptree)
        visitor.visit(root)

def import_tree_for_project(projectroot):
    import_tree = Node.new_nonleaf()
    for ff in py_files_in_dir(projectroot):
        add_imports_for_file_to_tree(ff, import_tree)
    return import_tree

def external_import_tree_for_project(projectroot):
    import_tree = import_tree_for_project(projectroot)
    internal_modules = root_modules_defined_in(projectroot)
    for m in internal_modules:
        import_tree.remove_path_and_children(m)

    return import_tree

def py_files_in_dir(rootdir):
    for root, dirs, files in os.walk(rootdir):
        for ff in files:
            if os.path.splitext(ff)[1] == '.py':
                yield os.path.join(root, ff)
