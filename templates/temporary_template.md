

This is the `master_README.md` file. This is where you mix your static content with placeholder template variables 

The below template variable **timed_process_killer** will get populated with the contents of `scripts/timed_process_killer.sh`: 
 
{{ timed_process_killer }}

Similarly, the entry below this line will get dynamically populated with the contents of `scripts/Auto.sh`:

{{ Auto }}

Files with dots (`.`) in their names work, below is `scripts/test.echo.sh`:

{{ context()['test.echo'] }}

This is static content, but below is a file with dashes in it's name from `scripts/script-with-dashes.py`:

{{ context()['script-with-dashes'] }}

