### Dynamic README codeblock generator

Inserts complete contents of files as as dynamically generated subsections, or parts (`Markdown code blocks`), of a newly generated Markdown file (`output/new.md`).

Allows a static, master template, `master_README.md`, to have dynamically generated subsections which are populated by the full contents of each file in `scripts/`.

Each file in `scripts/` becomes a `Markdown code block` in the new `outout/new.md`.

ie:
___

Some static content.


```
Full contents of one of the files in scripts/
```

More static content.

```
Full contents of another file in scripts/
```

___

## Dependencies

* Python 2.7.x ish (*Python3 compatibility is next*)
* [jinja2 templating library](http://jinja.pocoo.org/docs/dev/) -- if you don't have it already: `$ pip install jinja2`

## Structure of this repo


```
.
├── LICENSE.txt
├── README.md
├── dynreadme.py
├── output
│   └── new.md
├── scripts
│   ├── Auto.sh
│   ├── script-with-dashes.py
│   ├── test.echo.sh
│   └── timed_process_killer.sh
└── templates
    ├── master_README.md
    └── master_README_temp.md
```

* `README.md`: 
  * This file.
* `dynreadme.py`: 
  * When run, creates `output/new.md`, combining static content from `templates/master_README.md` as well as the file contents of each file in `scripts/`
* `output/new.md`: 
  * The new, dynamically created Markdown file. You can delete it because it gets created on every run of `dynreadme.py`.
* All the example files in `scripts/`: `Auto.sh`, `timed_process_killer.sh`, `test.echo.sh`, `script-with-dashes.py`: 
  * The contents of each of these files end up as `code blocks` within the new `output/new.md` file. You would replace these with your own files. 
* `templates/master_README.md`: 
  * This is the **master template**. This is where you add all your static content, and add your `{{ variables }}` which represent each file in `scripts/` (sections of your README you want to be replaced with full file contents from each file in `scripts/`). Each `{{ variable }}` gets dynamically populated with the contents of one of the files from `scripts/`. 
* `templates/master_README_temp.md`: 
  * This is a utility template created by `dynreadme.py` to accomodate the per-iteration adding of special prefixes needed for files with a `.` or `-` in their name. **You don't need to enter anything in this file.** You can delete it because it gets created on every run of `dynreadme.py`.


## Usage

In the `templates/master_README.md` put a reference to each file in `scripts/` whose contents you want to become a `code block` in the final `output/new.md` on a line by itself, surrounded by `{{ }}`. These become the `master_README.md` variables.

For example, for `scripts/Auto.sh` enter a line that says `{{ Auto }}` into `templates/master_README.md`. 

  * **Do not** include the file extension in `master_README.md` variables:
    * Good: `{{ file_name }}`
    * Bad: `{{ file_name.sh }}`
  * Variables can include dashes (`-`) and dots/periods (`.`)
    * `{{ file-name }}` is okay. So is `{{ file.name }}`.
  
For every file in `scripts/`, there should also be a `{{ filename }}` variable inside `templates/master_README.md`. **Ensure there is a one for one match.** 

#### Suggested variable names

`dynreadme.py` includes a `--suggest` function to automatically suggest `{{ var-names }}` for you to use inside `templates/master_README.md`.

Example:

```
$ ./dynreadme.py --suggest
Suggested master template variable for scripts/Auto.sh:
  {{ Auto }}
Suggested master template variable for scripts/script-with-dashes.py:
  {{ script-with-dashes }}
Suggested master template variable for scripts/test.echo.sh:
  {{ test.echo }}
Suggested master template variable for scripts/timed_process_killer.sh:
  {{ timed_process_killer }}
```


#### Run `dynreadme.py`:

```
$ ./dynreadme.py

Template variables found in templates/master_README.md:

Auto
script-with-dashes
test.echo
timed_process_killer

Adding contents of scripts/Auto.sh to output/new.md
Adding contents of scripts/script-with-dashes.py to output/new.md
Adding contents of scripts/test.echo.sh to output/new.md
Adding contents of scripts/timed_process_killer.sh to output/new.md
```

#### Output

The newly generated file (combination of static content from `templates/master_README.md` and the dynamic file contents of each file in `scripts/` is created in `output/new.md`.

#### Help

```
$ ./dynreadme.py --help
```
___

#### Issues / Problems / Enhancement Requests

Please [open a new Issue](https://github.com/ericdorsey/DynamicREADMEcodeblocks/issues/new).
___

#### Tested

OS | Python version  
--- | ---  
OSX 10.10.2 | 2.7.6  
