#!/usr/bin/env python
from __future__ import print_function # force use print()
from jinja2 import Environment, FileSystemLoader, contextfunction
import os
import sys
import re
import argparse
import pprint
import json

env = Environment(loader=FileSystemLoader('templates'))
template = env.get_template('master_README.md')


@contextfunction
def get_context(c):
    return c

template.globals['context'] = get_context

def check_master_template():
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
    fancy_new = [strip_it(i) for i in match_found]
    print("\nTemplate variables found in templates/master_README.md:\n")
    for i in fancy_new:
        print(i)
    os.chdir("..")
    return fancy_new


def generate_dynamic_readme(template_vars_found):
    template_values = {}
    os.chdir("scripts/")
    # print("")
    for filename in os.listdir('.'):
        # if "-" in filename:
        #     print("ERROR:")
        #     print("{0} contains a '-' character".format(filename))
        #     print("Please remove, or replace, all dashes from file names in scripts/ and rerun.")
        #     sys.exit(1)
        print("\nAdding contents of scripts/{0} to output/new.md".format(filename))
        #template_name = filename.split(".")[0]
        template_name = os.path.splitext(filename)[0]
        #template_name = u"{0}".format(template_name)
        print(repr(template_name))
        print("template_name is", template_name, type(template_name))
        # if template_name not in template_vars_found:
        #     print("ERROR:")
        #     print("{0} not found, or improperly formatted, in templates/master_README.md".format(template_name))
        #     print("Please add, or correct, template value for scripts/{0} and rerun.".format(template_name))
        #     sys.exit(1)
        data = "```\n"
        with open(filename, "r") as my_file:
            data += my_file.read()
        data += "\n```\n"
        template_values[template_name] = data
    #print(template_values)
    #pprint.pprint(template_values, width=1)
    print(json.dumps(template_values, indent=1))
    #output_from_parsed_template = template.render(template_values)
    output_from_parsed_template = template.render(template_values)
    print(output_from_parsed_template)
    with open("../output/new.md", "wb") as outfile:
        outfile.write(output_from_parsed_template)
    os.chdir("..")


def suggest_master_vars():
    os.chdir("scripts/")
    left = "{{"
    right = "}}"
    for filename in os.listdir("."):
        if "-" in filename:
            print("Suggested variable for {0}:".format(filename))
            print("  Replace '-' in {0} with '_'".format(filename))
            # print("  {left} {file} {right}".
            #       format(left=left, file=filename.replace("-", "_").
            #              split(".")[0], right=right))
            print("  {left} {file} {right}".format(
                left=left,
                file=os.path.splitext(filename)[0].replace("-", "_"),
                right=right))
        else:
            print("Suggested variable for {0}:".format(filename))
            # print("  {left} {file} {right}".
            #       format(left=left, file=filename.split(".")[0], right=right))
            print("  {left} {file} {right}".format(
                left=left,
                file=os.path.splitext(filename)[0],
                right=right))
    os.chdir("..")


def main(suggest=False):
    """
    Main program body.

    :param suggest: boolean
    :return: None
    """
    if suggest is True:
        suggest_master_vars()
    else:
        template_vars_found = check_master_template()
        generate_dynamic_readme(template_vars_found)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Dynamic README")
    parser.add_argument("-s", "--suggest",
                        help="suggest variable names for use in "
                             "master_README.md based on files in scripts/",
                        action="store_true", required=False)
    args = parser.parse_args()

    try:
        main(suggest=args.suggest)
    except KeyboardInterrupt:
        print("\nQuitting.")
