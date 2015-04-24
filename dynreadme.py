#!/usr/bin/env python
from __future__ import print_function  # Force use print()
from jinja2 import Environment, FileSystemLoader, contextfunction
import os
import re
import argparse
import shutil
import sys

# jinja2 templates are located in /templates
env = Environment(loader=FileSystemLoader('templates'))

# Files to exclude
exclude_files = [".DS_Store"]

# Override builtin raw_input for Python 3
try:
    input = raw_input
except NameError:
    pass


def copy_master():
    """
    Creates a temp copy of templates/master_README.md for handling output
    of file names which have "-" or "." in them.

    :return: None
    """
    shutil.copyfile("master_README.md", "temporary_template.md")


def create_master_temp():
    """
    Creates the templates/temporary_template.md file

    :return:
    """
    os.chdir("templates/")
    with open("temporary_template.md", "w") as new_file:
        pass
    os.chdir("..")


@contextfunction
def get_context(c):
    """
    jinja2 context function decorator for referencing
    special files names with "." or "-" in them

    :param c:
    :return: current context
    """
    return c


def retrieve_master_template_vars(exclude_files):
    """
    Gets everything in master_README.md that is between double braces.
    In other words, gets all the template variables.

    :return: list
    """
    def strip_it(my_value):
        new_value = my_value.replace("{{", "").replace("}}", "").strip()
        return new_value
    os.chdir("templates/")
    with open("master_README.md", "r") as my_file:
        data = my_file.read()
        match_found = re.findall(r'{{ .* }}', data)
    template_variables_found = [strip_it(i) for i in match_found]
    print("\nTemplate variables found in templates/master_README.md:\n")
    for i in sorted(template_variables_found):
        print(i)
    os.chdir("..")

    return template_variables_found


def generate_dynamic_readme(template_vars_found, exclude_files):
    template_values = {}  # To store contents of each file in scripts/
    special_case_characters = ["-", "."]
    os.chdir("scripts/")
    number_of_special_case_characters = 0
    left = "{{"
    right = "}}"
    print("")
    for index, filename in enumerate(os.listdir('.')):
        if filename not in exclude_files:
            print("Adding contents of scripts/{0} to output/new.md".format(filename))
            template_name = os.path.splitext(filename)[0]  # Strip off extension
            for char in special_case_characters:
                # For special character files.
                # We need to modify the temporary_template.md {{ vars }}
                # Example: {{ context()['vars'] }}
                if char in template_name:
                    number_of_special_case_characters += 1
                    os.chdir("../templates/")
                    # If this is our first special character file,
                    # copy the master onto the temp master template
                    if os.stat("temporary_template.md").st_size == 0:
                        copy_master()
                    with open("temporary_template.md", "r+") as current_file:
                        data = current_file.read()
                    re_match_string = "{left} {template_name} {right}".format(left=left, template_name=template_name, right=right)
                    replacement_var_name = "{left} context()['{template_name}'] {right}".format(left=left, template_name=template_name, right=right)
                    data = re.sub(re_match_string, replacement_var_name, data)
                    with open("temporary_template.md", "w") as new_file:
                        new_file.write(data)
                    os.chdir("../scripts/")
            # Load contents if each of the files in /scripts
            script_file_contents = "```\n"
            with open(filename, "r") as my_file:
                script_file_contents += my_file.read()
            script_file_contents += "\n```\n"
            template_values[template_name] = script_file_contents

    # If there were no special characters, need to copy master to
    # temp master to create new output.md file from
    if number_of_special_case_characters is 0:
        print("there were no special characters")
        print(">" * 10, "current dir is", os.getcwd())
        os.chdir("../templates/")
        copy_master()

    # Create the output/new.md file
    os.chdir("..")
    template = env.get_template('temporary_template.md')
    template.globals['context'] = get_context
    output_from_parsed_template = template.render(template_values)

    # Make a backup of previous output file before proceeding
    if os.path.exists("output/new.md"):
        shutil.copy2("output/new.md", "output/new_previous.md")

    with open("output/new.md", "wb") as outfile:
        # encode utf-8 for Python3
        outfile.write(output_from_parsed_template.encode('utf-8'))
    print("")


def suggest_master_vars(exclude_files):
    """
    Suggest template variable names for use in templates/master_README.md

    :param exclude_files: list
    :return:
    """
    os.chdir("scripts/")
    left = "{{"
    right = "}}"
    for filename in os.listdir("."):
        if filename not in exclude_files:
            print("Suggested master template variable for scripts/{0}:".format(filename))
            print("  {left} {file} {right}".format(
                left=left,
                file=os.path.splitext(filename)[0],
                right=right))
    os.chdir("..")


def compare_num_template_vars_to_scripts(template_vars_found, exclude_files):
    number_of_template_vars = len(template_vars_found)
    number_of_scripts = 0
    for filename in os.listdir("scripts/"):
        if filename not in exclude_files:
            number_of_scripts += 1
    if number_of_template_vars != number_of_scripts:
        choice = input("\nWarning! Number of template variables in templates/master_README.md not equal to "
                       "the number of files in scripts/ folder. \nProceed? (y/n): ")
        if choice.lower().startswith("n"):
            sys.exit("\nExiting..\n")


def main(suggest=False):
    """
    Main program body.

    :param suggest: boolean
    :return: None
    """

    if suggest is True:
        suggest_master_vars(exclude_files)
    else:
        create_master_temp()
        template_vars_found = retrieve_master_template_vars(exclude_files)
        compare_num_template_vars_to_scripts(template_vars_found, exclude_files)
        generate_dynamic_readme(template_vars_found, exclude_files)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Dynamic README")
    parser.add_argument("-s", "--suggest",
                        help="suggest variable names for use in "
                             "master_README.md based on files in 'scripts/'",
                        action="store_true", required=False)
    args = parser.parse_args()

    try:
        main(suggest=args.suggest)
    except KeyboardInterrupt:
        print("\nQuitting.")
