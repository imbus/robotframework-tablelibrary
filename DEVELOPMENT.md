# Development

## pre-commit

When starting to work on this library, please ensure you have installed the development requirements from the ``readme.md``.    

Once you have them installed, please execute the following shell command:    

```shell
pre-commit install
```

This will activate the ``.pre-commit-config.yaml`` from your ``root``directory.

### Run pre-commit manually from shell

You can run the configured pre-commit hook manually with the following shell command:

```shell
pre-commit run --all-files
```

### VS Code Git vs. Shell Git

If you're working with a virtual environment, you might get problems with committing changes with the VS Code Git Controls.     
In that case, please open a shell where your virtual environment is activated & add, commit & push your changes via git shell commands!


### VS Code custom Docstring template

If you want to use the custom docstring template for this project you have to get [autoDocstring](https://marketplace.visualstudio.com/items?itemName=njpwerner.autodocstring) first. Add the path to the custom template under [Custom Template Path](vscode://settings/autoDocstring.customTemplatePath) './vsc_plugins/autoDocstring/robotDoc.mustache' 