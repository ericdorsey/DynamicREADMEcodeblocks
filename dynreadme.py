from __future__ import print_function # force use print()
from jinja2 import Environment, FileSystemLoader
import os
import sys
import re

env = Environment(loader=FileSystemLoader('templates'))
template = env.get_template('master_README.md')


def check_master_template():
    """
    Gets everything in master_README.md that is between double braces.
    In other words, gets all the template variables.
    :return: List
    """
    def strip_it(my_value):
        new_value = my_value.replace("{{", "").replace("}}", "").strip()
        return new_value
    os.chdir("templates/")
    with open("master_README.md", "r") as my_file:
        data = my_file.read()
        match_found = re.findall(r'{{ .* }}', data)
    fancy_new = [strip_it(i) for i in match_found]
    print("Template variables found in templates/master_README.md:")
    for i in fancy_new:
        print(i)
    os.chdir("..")
    return fancy_new


def generate_dynamic_readme(template_vars_found):
    template_values = {}
    os.chdir("scripts/")
    print()
    for filename in os.listdir('.'):
        if "-" in filename:
            print("ERROR:")
            print("{0} contains a '-' character".format(filename))
            print("Please remove, or replace, all dashes from files in scripts/ and rerun.")
            sys.exit(1)
        print("Adding contents of scripts/{0} to output/new.md".format(filename))
        template_name = filename.split(".")[0]
        if template_name not in template_vars_found:
            print("ERROR:")
            print("{0} not found, or improperly formatted, in templates/master_README.md".format(template_name))
            print("Please add, or correct, template value for scripts/{0} and rerun.".format(template_name))
            sys.exit(1)
        data = "```\n"
        with open (filename, "r") as myfile:
            data += myfile.read()
        data += "\n```\n"
        template_values[template_name] = data
    output_from_parsed_template = template.render(template_values)
    with open("../output/new.md", "wb") as outfile:
        outfile.write(output_from_parsed_template)

template_vars_found = check_master_template()
generate_dynamic_readme(template_vars_found)