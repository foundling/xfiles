import json
import pdb

from utils import chomp, clean, is_empty, is_comment, is_dir, get_indent, get_filename, get_dirname, new_node,  find_ancestor, validate_schema, walk_tree

''' 
    Generates a directory tree from a reasonable, consistently-indented flat file representation. 

    Rules:
        - The indentation level must be consistent throughout the schema file. 
        - Lines that end with a '/' are directories. Everything else is a file. 
        - If a command-line argument for the root directory is not given, the schema must contain a single top-level directory.
        - If a command-line argument for the root directory is given, multiple top-level directories are allowed.
        - Blank lines (lines of length 0 after being stripped of whitespace) and comments (lines starting with '#' after being stripped of whitespace) are ignored.
        - Indentation must be preceded by a directory.

'''

def build_tree(schema, indent_size, OUTPUT_DIR):
    ''' parse the indentation level on each line to build a tree structure that can be walked to produce a directory structure. '''

    # virtual root has the top level dir in its child list, solving the uniformity issue
    virtual_root = new_node(parent=None, name='virtual_root', children=[])
    root = new_node(parent=virtual_root, name=OUTPUT_DIR, children=[])
    virtual_root['children'].append(root)
    indent = -1

    parent_node = virtual_root

    for line in schema:

        new_indent = get_indent(line, indent_size)

        # indent - we change the parent node to point to the parent root's last child
        # then we append children to new parent node's children 
        if new_indent > indent:
        
            parent_node = parent_node['children'][-1]

            if is_dir(line):
                parent_node['children'].append( new_node(parent=parent_node, name=get_dirname(line), children=[]) )
            else: 
                parent_node['children'].append( new_node(parent=parent_node, name=get_filename(line), children=None) )


        # unindent
        elif new_indent < indent:

            depth = indent - new_indent
            parent_node = find_ancestor(parent_node, depth)

            if is_dir(line):
                parent_node['children'].append( new_node(parent=parent_node, name=get_dirname(line), children=[]) )
            else: 
                parent_node['children'].append( new_node(parent=parent_node, name=get_filename(line), children=None) )


        # no change - add to parent's child array
        else:
            if is_dir(line):
                parent_node['children'].append( new_node(parent=parent_node, name=get_dirname(line), children=[]) )
            else: 
                parent_node['children'].append( new_node(parent=parent_node, name=get_filename(line), children=None) )

            # We haven't changed levels, so:
            # 1. append whatever it is to the child array of the current node
            # 2. leave the node pointer alone

        indent = new_indent
    return virtual_root

def main():

    SCHEMA_FILE = 'test.txt'
    OUTPUT_DIR = 'test_output'

    schema_lines = open(SCHEMA_FILE).readlines()
    schema = clean(schema_lines)

    indent_size = validate_schema(schema)
    tree = build_tree(schema, indent_size, OUTPUT_DIR)
    print len(tree['children'][0]['children'])
    print tree['children'][0]['name'] 
    print tree['children'][0]['children'][0]['name'] 
    print tree['children'][0]['children'][1]['name'] 
    print tree['children'][0]['children'][1]['children'][0]['name'] 
    print tree['children'][0]['children'][1]['children'][1]['children'] 

if __name__ == '__main__':
    main()

'''

dir1/
app/
    file1.txt
    dir2/
#    app/
#    README.txt
#    LICENSE.txt
#    docs/
#    test/

'''
