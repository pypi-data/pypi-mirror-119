
.. _plugins:

Available plugins
=================
Builtin Mold plugins.

Domains
-------
Python
******
Location: ``mold.plugins.domains.python``

Begin developing a python project.

Registered tools:

- python module - basic Python source module template (from mold_builtin)
- setuptools - setuptools build and dependencies for source and wheel distributions (from mold_builtin)
- pytest+tox - Pytest and linters with Tox configuration (from mold_builtin)
- github+templates - GitHub VCS host with issue templates (from mold_builtin)
- contributing Python+GitHub - contributing guide for Python projects using GitHub (from mold_builtin)
- github actions - GitHub actions with Pytest and Tox (from mold_builtin)
- minimal gitignore - git version control with minimal gitignore file (from mold_builtin)
- gitignore for Python - comprehensive gitignore file for Python (from mold_builtin)
- Apache 2.0 - permissive license preserving copyright and license notices (from mold_builtin)
- BSD 3-Clause - permissive license prohibiting use of contributor names in derived products (from mold_builtin)
- GPLv3.0 - strong copyleft license disclosing source and granting patent rights (from mold_builtin)
- MIT - permissive license only preserving copyright and license notice (from mold_builtin)
- pypi readme - basic PyPI readme file using RST (from mold_builtin)
- rst readme - basic RST readme file (from mold_builtin)
- sphinx - Sphinx documentation with initial structure and release notes (from mold_builtin)
- rtd - Read The Docs for Sphinx with badges (from mold_builtin)
- python cli - source for a Python CLI tool (from mold_builtin)
- Mold plugin - create your own Mold plugin (from mold_builtin)
- rst todo - basic RST TODO file (from mold_builtin)

Tools
-----
contributing Python+GitHub
**************************
Location: ``mold.plugins.tools.contributing_py_github.tool``

Contributing guide for python projects using github.

Depends on:

- pytest+tox - Pytest and linters with Tox configuration (from mold_builtin)
- github+templates - GitHub VCS host with issue templates (from mold_builtin)

github+templates
****************
Location: ``mold.plugins.tools.github.tool``

Github vcs host with issue templates.

Depends on:

- github - GitHub VCS host (from mold_builtin)

github actions
**************
Location: ``mold.plugins.tools.github_actions.tool``

Github actions with pytest and tox.

Depends on:

- github+templates - GitHub VCS host with issue templates (from mold_builtin)
- pytest+tox - Pytest and linters with Tox configuration (from mold_builtin)

minimal gitignore
*****************
Location: ``mold.plugins.tools.gitignore_minimal.tool``

Git version control with minimal gitignore file.

Depends on:

- gitignore - ignore files in git version control (from mold_builtin)

gitignore for Python
********************
Location: ``mold.plugins.tools.gitignore_python.tool``

Comprehensive gitignore file for python.

Depends on:

- gitignore - ignore files in git version control (from mold_builtin)

MIT
***
Location: ``mold.plugins.tools.license_mit.tool``

Permissive license only preserving copyright and license notice.

Depends on:

- license - license applied to the project (from mold_builtin)

pytest+tox
**********
Location: ``mold.plugins.tools.pytest_tox.tool``

Pytest and linters with tox configuration.

Depends on:

- python module - basic Python source module template (from mold_builtin)
- setuptools - setuptools build and dependencies for source and wheel distributions (from mold_builtin)

pypi readme
***********
Location: ``mold.plugins.tools.readme_pypi.tool``

Basic pypi readme file using rst.

Depends on:

- package readme - simple readme file for a package manager (from mold_builtin)
- readme - simple readme file (from mold_builtin)
- build - project build provider and dependencies (from mold_builtin)

rst readme
**********
Location: ``mold.plugins.tools.readme_rst.tool``

Basic rst readme file.

Depends on:

- readme - simple readme file (from mold_builtin)

rtd
***
Location: ``mold.plugins.tools.rtd_sphinx.tool``

Read the docs for sphinx with badges.

Depends on:

- documentation host - provider for online documentation (from mold_builtin)
- sphinx - Sphinx documentation with initial structure and release notes (from mold_builtin)
- rst readme - basic RST readme file (from mold_builtin)
- setuptools - setuptools build and dependencies for source and wheel distributions (from mold_builtin)

setuptools
**********
Location: ``mold.plugins.tools.setuptools.tool``

Setuptools build and dependencies for source and wheel distributions.

Depends on:

- readme - simple readme file (from mold_builtin)
- build - project build provider and dependencies (from mold_builtin)
- source - project source files (from mold_builtin)
- todo - TODO file pre-filled by other tools (from mold_builtin)

python module
*************
Location: ``mold.plugins.tools.source_basic_py.tool``

Basic python source module template.

Depends on:

- source - project source files (from mold_builtin)
- readme - simple readme file (from mold_builtin)

python cli
**********
Location: ``mold.plugins.tools.source_cli_py.tool``

Source for a python cli tool.

Depends on:

- python module - basic Python source module template (from mold_builtin)
- readme - simple readme file (from mold_builtin)

Mold plugin
***********
Location: ``mold.plugins.tools.source_mold_plugin.tool``

Create your own mold plugin.

Depends on:

- python module - basic Python source module template (from mold_builtin)
- setuptools - setuptools build and dependencies for source and wheel distributions (from mold_builtin)

sphinx
******
Location: ``mold.plugins.tools.sphinx.tool``

Sphinx documentation with initial structure and release notes.

Depends on:

- documentation - documentation engine of the project (from mold_builtin)
- readme - simple readme file (from mold_builtin)
- source - project source files (from mold_builtin)
- setuptools - setuptools build and dependencies for source and wheel distributions (from mold_builtin)
- license - license applied to the project (from mold_builtin)

rst todo
********
Location: ``mold.plugins.tools.todo_rst.tool``

Basic rst todo file.

Depends on:

- todo - TODO file pre-filled by other tools (from mold_builtin)

Categories
----------
gitignore
*********
Location: ``mold.plugins.categories.gitignore``

.gitignore file for git

license
*******
Location: ``mold.plugins.categories.license_``

License applied to the project

source
******
Location: ``mold.plugins.categories.source``

Project source code

Interfaces
----------
build
*****
Location: ``mold.plugins.face.build.interface``

Project build provider and dependencies.

Provides variables:

- ``build_download_url`` (``<class 'str'>``)
- ``build_email`` (``<class 'str'>``)
- ``build_keywords`` (``<class 'str'>``)
- ``build_url`` (``<class 'str'>``)

Accepts variables:

- ``build_entry_points`` (``typing.Dict[str, typing.List[str]]``)
- ``build_extra_deps`` (``typing.Dict[str, typing.List[str]]``)
- ``build_project_urls`` (``typing.Dict[str, str]``)
- ``build_pyproject_sections`` (``typing.Dict[str, typing.List[str]]``)
- ``build_readme_file`` (``<class 'str'>``)

Associated questions:

- ``build_email``, prompt: package author email
- ``build_keywords``, prompt: package keywords (space separated)

documentation
*************
Location: ``mold.plugins.face.doc.interface``

Documentation engine of the project.

Accepts variables:

- ``doc_footer_lines`` (``typing.List[str]``)
- ``doc_header_lines`` (``typing.List[str]``)
- ``doc_links`` (``typing.List[mold.Link]``)

Associated questions:

- ``docs_semver_over_calver``, prompt: Choose a versioning scheme: Semantic Versioning (e.g. 1.7.2) or Calendar (e.g. 2018.11.03) Versioning [S]/C (leave empty for Semantic Versioning)

documentation host
******************
Location: ``mold.plugins.face.doc_host.interface``

Provider for online documentation.

Provides variables:

- ``doc_host_url`` (``<class 'str'>``)

github
******
Location: ``mold.plugins.face.github.interface``

Github vcs host.

Provides variables:

- ``github_repo`` (``<class 'str'>``)
- ``github_user`` (``<class 'str'>``)

Parent interfaces:

- vcs host - online host of the version control system (from mold_builtin)

Associated questions:

- ``github_user``, prompt: GitHub user name
- ``github_repo``, prompt: GitHub repository (leave empty for project slug)

gitignore
*********
Location: ``mold.plugins.face.gitignore.interface``

Ignore files in git version control.

Accepts variables:

- ``gitignore_items`` (``typing.List[str]``)

license
*******
Location: ``mold.plugins.face.license.interface``

License applied to the project.

Provides variables:

- ``license_author`` (``<class 'str'>``)
- ``license_shorthand`` (``<class 'str'>``)
- ``license_years`` (``<class 'str'>``)

Associated questions:

- ``license_author``, prompt: package author
- ``license_first_year``, prompt: first year of license (leave blank for current)

package readme
**************
Location: ``mold.plugins.face.package_readme.interface``

Simple readme file for a package manager.

Accepts variables:

- ``package_readme_footer_lines`` (``typing.List[str]``)
- ``package_readme_header_lines`` (``typing.List[str]``)
- ``package_readme_links`` (``typing.List[mold.Link]``)

documentation host
******************
Location: ``mold.plugins.face.read_the_docs.interface``

Provider for online documentation.

Provides variables:

- ``rtd_project`` (``<class 'str'>``)

Parent interfaces:

- documentation host - provider for online documentation (from mold_builtin)

Associated questions:

- ``rtd_project``, prompt: RTD project name (leave empty for project slug)

readme
******
Location: ``mold.plugins.face.readme.interface``

Simple readme file.

Provides variables:

- ``readme_description`` (``<class 'str'>``)

Accepts variables:

- ``readme_example_lines`` (``typing.List[str]``)
- ``readme_footer_lines`` (``typing.List[str]``)
- ``readme_header_lines`` (``typing.List[str]``)
- ``readme_links`` (``typing.List[mold.Link]``)

Associated questions:

- ``readme_description``, prompt: project description

source
******
Location: ``mold.plugins.face.source.interface``

Project source files.

Provides variables:

- ``source_full_dir`` (``<class 'str'>``)
- ``source_package_name`` (``<class 'str'>``)
- ``source_use_src_dir`` (``<class 'bool'>``)

Accepts variables:

- ``source_code_lines`` (``typing.List[str]``)
- ``source_doc_lines`` (``typing.List[str]``)
- ``source_import_lines`` (``typing.List[str]``)

todo
****
Location: ``mold.plugins.face.todo.interface``

Todo file pre-filled by other tools.

Accepts variables:

- ``todo_items`` (``typing.List[str]``)

vcs host
********
Location: ``mold.plugins.face.vcs_host.interface``

Online host of the version control system.

Provides variables:

- ``vcs_host_url`` (``<class 'str'>``)

