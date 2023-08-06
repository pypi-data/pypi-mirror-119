## Plugin for pylint which allows defining and checking variable name for exception (like `e` or `exc` or other)

Install:
```bash
pip install pylint-exception-var-name-plugin
```

Usage:
```bash
pylint --load-plugins exception_var_name FILES_TO_CHECK
```

`ALLOWED_VAR_NAME` default is `e`. Can be set in command line:
```bash
pylint --load-plugins exception_var_name ALLOWED_VAR_NAME FILES_TO_CHECK
```
or in pylint config file (`pylintrc`)
```bash
exception-var-name=ALLOWED_VAR_NAME
```