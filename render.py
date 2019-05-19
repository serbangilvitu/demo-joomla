#!/usr/bin/env python3
import os
from jinja2 import Template
from argparse import ArgumentParser

parser = ArgumentParser()
parser.add_argument("-v", "--app_version", help="appVersion to be used")
args = parser.parse_args()

with open(os.getcwd()+'/k8s/service.j2', mode='r') as source:
    content = source.read()

tm = Template(content)
rendered = tm.render(app_version=args.app_version)

output = open(os.getcwd()+'/k8s/service.yaml', 'w')
output.write(rendered)
output.close()