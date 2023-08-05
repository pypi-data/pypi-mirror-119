{% set is_open_source = cookiecutter.open_source_license != 'Not open source' -%}

<h1 align = "center">:rocket: {{ cookiecutter.project_name }} :rocket:</h1>

{% if is_open_source %}

![image](https://img.shields.io/pypi/v/{{ cookiecutter.project_slug }}.svg)
![image](https://img.shields.io/travis/{{ cookiecutter.github_username }}/{{ cookiecutter.project_slug }}.svg)
![image](https://readthedocs.org/projects/{{ cookiecutter.project_slug | replace("_", "-") }}/badge/?version=latest)

{% endif %}

---
# Install
```python
pip install -U {{cookiecutter.project_slug}}
```

# Usages

---
# TODO
