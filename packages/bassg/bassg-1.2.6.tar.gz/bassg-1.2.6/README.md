# BASSG  

 **BASSG** *(Basic Agile Static Site Generator)* is a simple and easy to use static site generator for quickly creating static websites using [Jinja2](https://jinja.palletsprojects.com/en/3.0.x/) templating and [Markdown](https://www.markdownguide.org/getting-started/).

 Features:
 - Jinja2 templating
 - Markdown
 - Custom assets & site folder structure
 - Easy to use conventions for creating pages, templates, and markdown

# Installing  

```text
$ pip install bassg
```
I would recommend installing **BASSG** in a [virtual environment](https://docs.python.org/3/library/venv.html). This allows you to access **BASSG** using the "bassg" entry point:
```text
$ bassg --help
```
Otherwise, **BASSG** can be accessed with python directly:
```text
$ python -m bassg --help
```

# Usage

If you need help with a command, run:
```text
$ bassg <command> --help
```
to see the help menu for that command.

## Create the project directory:

```text
$ bassg create <project_name>
```
This will create the folder structure in the current directory (root):  
```
📦project_name
 ┣ 📂build
 ┃ ┣ 📂assets
 ┃ ┣ 📂config
 ┃ ┣ 📂markdown
 ┃ ┗ 📂templates
 ┗ 📂site
```

## Generating the site:

```text
$ bassg generate <project_name>
```
This will compile all of the html files in the *build/* directory using Jinja2 and Markdown

## Creating and using templates:

Place Jinja2 templates in the *templates/* directory. Any html files in the base *build/* directory that include these templates will be rendered accordingly.

## Using markdown:

If you want to use markdown in your site, create a file_name.md file with the same file name as the html page you want to insert it in. Place this file in the *build/markdown/* directory. The parsed markdown data will be passed into the Jinja2 parser as 'markdown'. If you wish to have multiple markdown files per page, you can use the naming convention:

`file_name0.md`  
`file_name1.md`  
...  

These can then be accesed in the `file_name.html` file as markdown[0], markdown[1], etc.

## Per-page config (json) files:

You can create (optional) configuration files for individual pages with a similar syntax to creating markdown files. Any `file_name.json` files with the same file name as an html page in the *build/* directory will be passed in through the Jinja2 parser.

For example:  
`file_name.json`:
```json
{
    "title": "Documentation",
    "date": "08/22/2021",
    "language": "English",
    "folder_struct": "docs"
}
```
All of these variables will be passed into the Jinja2 parser for `file_name.html`.

The special attribute `folder_struct` tells **BASSG** which folder to place the page in when it generates the site. In this example, the generated `file_name.html` file will be placed in the *site/docs/* folder. This can be used to easily organize the pages of your site.