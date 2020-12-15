#!/usr/bin/env python
# -*- coding: utf-8 -*-

import setuptools

with open('README.md', 'r', encoding='utf-8') as f:
    README = f.read()

setuptools.setup(
    name='PySched-Lightning',
    version='0.1.0',
    description='A lightweight task queue scheduler that runs in the background',
    author='Yi Zhang',
    author_email='yizhang.dev@gmail.com',
    long_description=README,
    long_description_content_type='text/markdown',
    url='https://github.com/yzhang-dev/PySched-Lightning',
    download_url='https://github.com/yzhang-dev/PySched-Lightning',
    packages=[
        'pysched_lightning'
    ],
    keywords=[
        'timer',
        'scheduler',
        'job-queue',
        'task-queue',
        'delayed-jobs'
        'background-jobs',
        'background-thread',
        'tasks',
        'background'
    ],
    classifiers=[
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.7',
    ],
    license='MIT',
    python_requires='>=3.7',
)
