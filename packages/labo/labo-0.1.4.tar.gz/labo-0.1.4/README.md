# labo - LaTeX Bootstrapper
`labo` is a CLI-utility for bootstrapping LaTeX-projects based on templates.
It uses [Jinja2](https://jinja2docs.readthedocs.io/en/stable/) for the templating.

## Configuration
By default `labo` looks for the configuration file in `$HOME/.config/labo/labo.toml` and `$HOME/.labo.toml`, in that order. Currently the only configuration option is the location of the templates. This is specified by the `template_dir` key:

```toml
template_dir = /home/user/.labo
```

## Templates
A template for a LaTeX project for `labo` is specified by a `config.toml` file in a folder in the template directory. See `example_template/` for a simple example.
The name of the template is determined by the name of this folder. In the config file the template files can be specified using the `instantiate` key.
For the time being it supports rendering LaTeX and Makefile templates using Jinja2.
Files that need to be copied or need to be linked to the new project can also be specified using the `copy` and `link` keys, respectively.
Below is an example of these keys

``` toml
instantiate = ["main.tex", "Makefile"]
copy = ["document.tex"]
link = ["myclass.cls", "mypackage.sty"]
```

### Variables
The templates can contain variables. These variables can either be defined using hooks or by specifying them
in the `config.toml` under the `[variables]` section.
`labo` prompts automatically for the variables during the bootstrapping of the project.
A variable can be defined as followed:

``` toml
[variables]
var.prompt = "Foo"
var.default = 1
```
The `prompt` key defines the text used for prompting for the variable and is mandatory.
The `default` key is used to infer the type of the variable and is mandatory.

The variable can be used in a LaTeX-template by `\VAR{var}` and in a Makefile template by `{{var}}`.

### Hooks
Before the templates are rendered a `pre_template_hook` is ran. This hook can be defined in a `hooks.py`
file in the template folder. This hook is passed four arguments: The current working directory, the project path, the options (see next section) and the variables. It is expected to return a dictionary of variables.

Since this hook allows for the execution of arbitrary Python code it is important to ensure that the hook does not contain any malicious code.

### Options
A template can define extra options with the options key.

``` toml
options = ["opt"]
```

### Help
Using the `help` key a help message can be added to the template.

## Usage
Using `labo ls` all templates can be listed. `labo help <template>` displays help information about the template `<template>`. To bootstrap a project use `labo new <template> <project name> <template options>`.
