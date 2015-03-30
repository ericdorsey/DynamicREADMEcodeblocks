### Dynamic README codeblock generator

Inserts complete contents of files (examples used `Auto.sh` and [`timed_process_killer.sh`](https://github.com/bcambl/timed-process-killer) below) as codeblocks in a new file `output/new.md`.

#### Dependencies

* [jinja2 templating library](http://jinja.pocoo.org/docs/dev/)

If you don't have it already:


`$ sudo pip install jinja2`

#### Structure of this repo


```
├── README.md (this file)
├── dynreadme.py (Python file to run to create /output/new.md)
├── output
│   └── new.md (new .md file created at run)
├── scripts
│   ├── Auto.sh (script which becomes part of code
│   │            block in output/new.md)
│   └── timed_process_killer.sh
└── templates
    └── master_README.md (the shell for new.md, 
                          gets populated with script 
                          contents from each file in
                          /scripts)
```

#### Usage

**Caveats**: The code is pretty fragile right now -- ie, there is no exception handling built in. Please open an issue to report errors. 

* In the `templates/master_README.md` put a reference to each script you want to become a code block on a line by itself, surrounded by `{{ }}`, so for example, for `scripts/Auto.sh` enter a line that says `{{Auto}}` into `templates/master_README.md`. 

  * *Do not* include the file extension, or put spaces around the file name (ie, `{{this}}`, not `{{ this }}` or `{{this.sh}}`). Also, file names in `scripts/` cannot have `-`'s (dashes) in them -- not the filename itself in `scripts/` nor the `{{ }}` tag in `templates/master_README.md`. `jinja2` breaks on dashes in the file names.
  * Ensure that there is a one for one match of each file in `scripts/`, and for `{{}}` tags inside `master_README.md`. In other words, for every file in `scripts/` there shoudl also be  `{{filename}}` tag inside `master_README.md`.

*  Run `dynreadme.py`

```
$ python dynreadme.py
Generating codeblock for Auto.sh
Generating codeblock for timed_process_killer.sh
```

* Newly generated file `new.md` is in `output/`.

___
#### Tested

OS|Python version
--|--
OSX 10.10.2|2.7.6