#!/usr/bin/env python3

import json
import yaml
import os
import sys
from jinja2 import Environment, FileSystemLoader
from pprint import pprint

import logging
logging.basicConfig(level=logging.INFO)
log = logging.getLogger('generate')

# Helper function to convert OpenAPI spec types to Ansible types
def convert_type(type_value):

    table = {
        "string": "str",
        "boolean": "bool",
        "array": "list",
        "object": "dict",
        "integer": "int"
    }

    if type_value in table.keys():
        return table[type_value]
    elif type_value not in table.values():
        logging.warning("Unable to convert type '{}'".format(type_value))

    return type_value

# Helper function to extract examples for documentation from the demo playbook
def parse_examples(path="tests/demo_playbook.yml"):

    examples = dict()
    _examples = dict()

    with open(path, "r") as f:
        playbook = yaml.safe_load(f)

        # Find all examples and categorise by resource to 

        # Find the Create and Delete examples for each resource
        for task in playbook[0]['tasks']:
            if '(' not in task['name']:
                logging.info("Ignoring non-annotated task {}".format(task['name']))
                continue
            modname = task['name'].split("(")[1][:-1]
            if modname == "meta":
                logging.info("Ignoring meta task {}".format(task['name']))
                continue
            if modname == 'debug':
                logging.info("Ignoring debug task {}".format(modname))
                continue
            else:
                modfullname = "ryanph.vast.{}".format(modname)
            if 'vms_verify_ssl' in task[modfullname]:
                del task[modfullname]['vms_verify_ssl']
            if modname not in _examples:
                _examples[modname] = list()

            logging.info("Adding task '{}' to examples for '{}' module".format(task['name'], modname))
            _examples[modname].append(task)

        # Build the example data
        for key in _examples.keys():
            examples[key] = list()
            for e in _examples[key]:
                if 'vms_verify_ssl' in e:
                    del e['vms_verify_ssl']
                
                examples[key].append(yaml.dump(e, sort_keys=False))

    return examples

def parse_parameter_info(spec):

    param_map = {}
    for schema in spec['components']['schemas'].keys():
        param_map[schema] = spec['components']['schemas'][schema]['properties']
    return param_map
    
    

if __name__ == "__main__":

    environment = Environment(loader=FileSystemLoader("templates/"))

    log.info("Reading settings from settings.yml")
    with open('settings.yaml', 'r') as f:
        settings = yaml.safe_load(f)

    log.info("Reading project information from package.json")
    with open('package.json', 'r') as f:
        packageinfo = json.load(f)

    log.info("Reading OpenAPI spec from {}".format(settings['openapi_spec']))
    with open(settings['openapi_spec'], 'r') as f:
        api_spec = yaml.safe_load(f)

    log.info("Extracting examples from demo playbook tests/demo_playbook.yml")
    examples = parse_examples()

    log.info("Extracting parameter types and descriptions from OpenAPI spec for use in documentation")
    parameter_info = parse_parameter_info(api_spec)

    # Generate galaxy.yml
    log.info("Generating galaxy.yml from template")
    try:
        os.makedirs("build/ryanph/vast")
    except FileExistsError:
        pass
    template = environment.get_template("galaxy.yml.j2")
    with open("build/ryanph/vast/galaxy.yml", "w") as f:
        f.write(template.render(packageinfo))

    # Generate README.md
    log.info("Generating README.md from template")
    template = environment.get_template("readme.md.j2")
    with open("build/ryanph/vast/README.md", "w") as f:
        f.write(template.render({"settings":settings,"examples":examples,"packageinfo":packageinfo,"paraminfo":parameter_info}))

    # Generate module_utils.py
    log.info("Generating vast_utils.py")
    template = environment.get_template("vast_utils.py.j2")
    try:
        os.makedirs("build/ryanph/vast/plugins/module_utils")
    except FileExistsError:
        pass
    with open("build/ryanph/vast/plugins/module_utils/vast_utils.py", "w") as f:
        f.write(template.render({"settings":settings,"examples":examples}))

    # Generate Modules
    for module in settings['modules'].keys():

        log.info("Generating module '{}'".format(module))
        
        module_settings = settings['modules'][module]
        schema = api_spec['components']['schemas'][module_settings['schema']]

        options = {
            "vms_hostname": {
                "description": "The hostname of the Vast Management Service (VMS)",
                "type": "str",
                "required": False,
                "default": "'vast.local'"
            },
            "vms_username": {
                "description": "Username of the VMS manager to connect as",
                "type": "str",
                "required": False,
                "default": "'admin'"
            },
            "vms_password": {
                "description": "Password of the VMS manager to connect as",
                "type": "str",
                "required": False,
                "default": "'123456'",
                "no_log": True
            },
            "vms_verify_ssl": {
                "description": "Whether to verify SSL parameters when connecting to VMS",
                "type": "bool",
                "required": False,
                "default": True
            },
            "vms_auth_type": {
                "description": "The authentication type to use, bearer or basic",
                "type": "str",
                "required": False,
                "default": "'basic'"
            }
        }
        required_if_options = list()

        for opt in module_settings['options']:

            if opt not in schema['properties']:
                raise Exception("Option '{}' is not present in {} schema".format(opt, module))
            
            if 'description' not in schema['properties'][opt]:
                raise Exception("Missing required property in 'description' in OpenAPI Spec for {}.{}".format(module, opt))
            
            options[opt] = {
                "name": opt,
                "description": schema['properties'][opt]['description'],
                "type": convert_type(schema['properties'][opt]['type']),
                "default": schema['properties'][opt]['default'] if 'default' in schema['properties'][opt] else None
            }

            # Default search value parameter is always required
            if opt == module_settings['sdk_search_param_name']:
                options[opt]['required'] = True
                
            # Options with a default value are not required
            elif 'default' in schema['properties'][opt]:
                options[opt]['required'] = False
                if isinstance(options[opt]['default'], str):
                    options[opt]['default'] = "'" + schema['properties'][opt]['default'] + "'"
                else:
                    options[opt]['default'] = schema['properties'][opt]['default']

            # Other options are required if the state is 'present'
            else:
                options[opt]['required'] = False
                required_if_options.append(opt)

        if 'additional_options' in module_settings:
            for opt in module_settings['additional_options'].keys():
                options[opt] = {
                    "name": opt,
                    "required": module_settings['additional_options'][opt]['required'],
                    "description": module_settings['additional_options'][opt]['description'],
                    "type": convert_type(module_settings['additional_options'][opt]['type']),
                    "default": module_settings['additional_options'][opt]['default'] if 'default' in module_settings['additional_options'][opt] else None
                }

        if module_settings['query_only'] == False:
            options['state'] = {
                "description": "The desired state of the resource",
                "type": "str",
                "choices": ["absent", "present"],
                "required": True,
                "default": None
            }
            if 'action_only' in module_settings and module_settings['action_only']:
                options['state']['choices'].remove('absent')
                options['state']['required'] = False
                options['state']['default'] = "'present'"

        try:
            os.makedirs("build/ryanph/vast/plugins/modules")
        except FileExistsError:
            pass
        
        substitutions = {
            "name": module,
            "module_options": options,
            "settings": module_settings,
            "required_if_options": required_if_options
        }
        log.debug(substitutions)

        template = environment.get_template("module.py.j2")
        with open("build/ryanph/vast/plugins/modules/{}.py".format(module), "w") as f:
            f.write(template.render(substitutions))