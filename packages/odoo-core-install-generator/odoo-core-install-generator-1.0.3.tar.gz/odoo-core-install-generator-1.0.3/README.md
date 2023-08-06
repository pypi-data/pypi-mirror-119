# Odoo Core Install Generator

## Install
- pip
```
pip install odoo-core-install-generator
```

## Using
#### Options
| Key | Description | Required | Default | Example |
|-|-|-|-|-|
| project | project name or code | :heavy_check_mark: | | project=biszx |
| website | website | | | website=https://biszx.com |
| version | version | | 14 | version=14 |
| addon_path | addon path to generate core install | | addons | addon_path=addons |
#### config
create ext.py in project core install directory
```
# tree view
addons/project_core_install
└── ext.py

# ext.py
options = {
    # more addon to depends addon directory
    # that contain in project path
    'addon_path': [],
  
    # more addon to depends by addon name
    'depends': [
        'more_addon',
    ]
}
```
#### running
```
odoo-core-install-generator project=biszx
```
