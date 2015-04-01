### Dynamic README codeblock generator

Inserts complete contents of files (examples used `Auto.sh` and [`timed_process_killer.sh`](https://github.com/bcambl/timed-process-killer) below) as dynamically generated subsections, or parts (`Markdown code blocks`), of a new Markdown file `output/new.md`.

Allows a static, master template, `master_README.md`, to have dynamically generated subsections which are populated by the full contents of each file in `scripts/`.

Each file in `scripts/` becomes a `Markdown code block` in the new `outout/new.md`.

ie:
___

Some static content.


```
full contents of one of the files in scripts/
```

More static content.

```
full contents of another file in scripts/
```

___

#### Dependencies

* [jinja2 templating library](http://jinja.pocoo.org/docs/dev/)

If you don't have it already: `$ pip install jinja2`

#### Structure of this repo


```
├── README.md
├── dynreadme.py
├── output
│   └── new.md
├── scripts
│   ├── Auto.sh
│   └── timed_process_killer.sh
└── templates
    └── master_README.md
```

* README.md: This file
* dynreadme.py: When run, creates `output/new.md`, combining static content from `templates/master_README.md` as well as the file contents of each file in `scripts/`
* new.md: The new combined Markdown file
* `Auto.sh` and `timed_process_killer.sh`: The contents of each of these files end up as `code blocks` within the new `output/new.md` file
* master_README.md: The static content, the "master" template, contains the `{{ variables }}` which represent each file in `scripts/`. Each `{{ variable }}` gets dynamically populated with the contents of one of the files from `scripts/`.


#### Usage

In the `templates/master_README.md` put a reference to each script whose contents you want to become a `code block` on a line by itself, surrounded by `{{ }}`. These become the `master_README.md` variables.

For example, for `scripts/Auto.sh` enter a line that says `{{ Auto }}` into `templates/master_README.md`. 

  * *Do not* include the file extension in `master_README.md` variables:
    * `{{ file_name }}` not `{{ file_name.sh }}`
  * Variables in `master_README.md` *cannot* have `-`'s (dashes) in them:
    * `{{ file_name }}` not `{{ file-name }}`
  
For every file in `scripts/`, there should also be a `{{ filename }}` variable inside `master_README.md`. Ensure there is a one for one match. 

Run `dynreadme.py`:

```
$ python dynreadme.py
Template variables found in templates/master_README.md:
timed_process_killer
Auto

Adding contents of scripts/Auto.sh to output/new.md
Adding contents of scripts/timed_process_killer.sh to output/new.md
```

The newly generated file (combination of static content from `master_README.md` and the file contents of each file in `scripts/`) `new.md` is in `output/`.

___

#### Tested

OS | Python version  
--- | ---  
OSX 10.10.2 | 2.7.6  