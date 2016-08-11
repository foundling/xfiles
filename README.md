![superdir_header](https://github.com/foundling/superdir/blob/master/superdir_logo.png)

`superdir` is a command-line tool for Linux, BSD, and OSX that generates a directory tree from a reasonable, consistently-indented flat file representation.  It is MIT-licensed.

## Installation:

````bash
pip install superdir
````

## Usage:

````bash
superdir SCHEMA_FILE [OUTPUT_DIR]
````

## Contributing

See here for the [contributors guide](https://github.com/foundling/superdir/blob/master/CONTRIBUTING.md). 


## Motivation:

Between learning to build new things and writing about how to build things, I inevitably end up creating a lot of temporary directory structures.  `superdir` is a quick and visually intuitive way to generate these temporary structures without having to dive into code, much less debug that code.  Just copy a file structure that you find in a tutorial, put it in a file, pipe it to `superdir`, and off you go.

## Behavior:

- `superdir` uses the level of indentation in your flat-file representation to create a file hierarchy at the output directory.
- If no output directory is specified, a generic one is created with the date appended.
- `superdir` creates the directory structure from the schema only if it passes validation.
- By default, lines that end with '`/`' are treated as directories. Everything else is treated as a file. 
- Comments should be prefixed by '`#`'.
- Comments and blank lines are ignored.
- If an `OUTPUT_DIR` argument is **not** given, the schema must contain a single top-level directory.
- If an `OUTPUT_DIR` argument is given, the schema file may contain multiple top-level directories.
- If the `OUTPUT_DIR` already exists, it won't be overwritten. 

## superdir in action!

````bash
$ cat schema.txt

# Flat-file example of a directory structure
superdir/
    docs/
    superdir/
        superdir.py
        validator.py
        tree.py
    test/
        superdir_test.py
        validator_test.py
        tree_test.py
    README.md
    LICENSE.md
    test/

$ superdir schema.txt new_project 
$ tree
new_project
└── superdir/
    └── docs/
    └── superdir/
        └── superdir.py
        └── validator.py
        └── tree.py
    └── test/
        └── superdir_test.py
        └── validator_test.py
        └── tree_test.py
    └── README.md
    └── LICENSE.md
$ cat schema.txt | superdir another_new_project
$ tree another_new_project
another_new_project
└── superdir/
    └── docs/
    └── superdir/
        └── superdir.py
        └── validator.py
        └── tree.py
    └── test/
        └── superdir_test.py
        └── validator_test.py
        └── tree_test.py
    └── README.md
    └── LICENSE.md
````
