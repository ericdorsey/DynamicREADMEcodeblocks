from __future__ import print_function # force use print()
from jinja2 import Environment, FileSystemLoader
import os

# TODO verify {{ foo }} in template before proceeding
# TODO dash in filenames breaks Jinja with Undef = undef err

#os.chdir("template/")
env = Environment(loader=FileSystemLoader('templates'))
#print(os.getcwd())
template = env.get_template('master_README.md')
#print(template)


# list all the files in /scripts
def generate_dynamic_readme():
    filenames = []
    template_values = {}
    #print(os.getcwd())
    os.chdir("scripts/")
    #print(os.getcwd())
    for filename in os.listdir('.'):
        #print(filename)
        template_name = filename.split(".")[0]
        data = "\n```\n"
        with open (filename, "r") as myfile:
            data += myfile.read()
        data += "```\n"
        template_values[template_name] = data
        filenames.append(filename)
        #print(data) # file contents
    #print(template_values)
    output_from_parsed_template = template.render(template_values)
    with open("../output/new.md", "wb") as outfile:
        outfile.write(output_from_parsed_template)
    for i in filenames:
        print("Generating codeblock for {0}".format(i))
    return filenames

generate_dynamic_readme()
#print(filenames)



