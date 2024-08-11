# -*- coding: utf-8 -*-

name = u'maya_texture_retarget'

version = "1.0.0"

description = u'Add description of project here'

requires = [
    'python-3.11+'
]

variants = [['python-3.11']]

hashed_variants = True

build_command = 'python {root}/build.py {install}'

def commands():
    env.PYTHONPATH.append('{root}/python')
