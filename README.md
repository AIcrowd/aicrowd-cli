
# aicrowd

A CLI app to interact with AIcrowd 

## How to install the CLI for development

 - Install the API locally https://github.com/AIcrowd/aicrowd-api
 - Install python client for Evaluations API https://gitlab.aicrowd.com/aicrowd/evaluations-api-clients/tree/dev/python (for grader commands only)
 - Clone this repository  https://github.com/AIcrowd/aicrowd-cli.git
 - inside the repository `pip install -r requirements.txt`
 - then do `python setup.py develop`
 - And now you are good to start developing/using the features


## Project Features
Before using the CLI one has to generate the ssh keys and access token required to interact with Gitlab.

- To generate ssh keys and upload them to Gitlab:
```bash
aicrowd ssh create
```

- To genereate personal access token from Gitlab:
```bash
aicrowd access_token create
```

- To create a folder for a challenge with challenge spec:
```bash
aicrowd challenge init
```
The console will ask for the challenge id (which will be provided on the challenge home page)

- To view all the datasets related to a challenge, (has to be run inside the challenge folder):
```bash
aicrowd dataset list
```

- To download a dataset:
```bash
aicrowd dataset download
```

- To Start with a template for the challenge:
```bash
aicrowd template list
aicrowd template download
```

- To quickly start working on a baseline for the challenge:
```bash
aicrowd baseline list
aicrowd baseline download
```

- To make a submission:
```bash
aicrowd submit
```
(Submit requires one to have already run aicrowd ssh create)

- To check the proogress of the submission once submitted: 
```bash
aicrowd status
```

### AIcrowd Evaluations API Commands

Login and save the auth token locally.

```bash
aicrowd evaluations login -e <email> -p <password>
```

Validate the grader repository

```bash
git clone <grader_repository>
cd <repository>
aicrowd evaluations grader create --repo <grader_repository> --validate
```

Creating a creader

```bash
git clone <grader_repository>
cd <repository>
aicrowd evaluations grader create --repo <grader_repository>
```

Passing the secrets when creating grader

```bash
aicrowd evaluations grader create \ 
    --repo <grader_repository> \ 
    -s secret1=value \ 
    -s secret2=value
```


Many more commands like `aicrowd convert` and `aicrowd capture` yet to come. Stay tuned.

* [aicrowd](http://aicrowd-cli.readthedocs.io/)
* a starter [Click](http://click.pocoo.org/5/) command-line application
* automated unit tests you can run with [pytest](https://docs.pytest.org/en/latest/)
* a [Sphinx](http://www.sphinx-doc.org/en/master/) documentation project

## Getting Started

The project's documentation contains a section to help you
[get started](https://aicrowd-cli.readthedocs.io/en/latest/getting_started.html) as a developer or
user of the library.

## Development Prerequisites

If you're going to be working in the code (rather than just using the library), you'll want a few utilities.

* [GNU Make](https://www.gnu.org/software/make/)
* [Pandoc](https://pandoc.org/)

## Resources

Below are some handy resource links.

* [Project Documentation](http://aicrowd-cli.readthedocs.io/)
* [Click](http://click.pocoo.org/5/) is a Python package for creating beautiful command line interfaces in a composable way with as little code as necessary.
* [Sphinx](http://www.sphinx-doc.org/en/master/) is a tool that makes it easy to create intelligent and beautiful documentation, written by Geog Brandl and licnsed under the BSD license.
* [pytest](https://docs.pytest.org/en/latest/) helps you write better programs.
* [GNU Make](https://www.gnu.org/software/make/) is a tool which controls the generation of executables and other non-source files of a program from the program's source files.


## Authors

* **S.P. Mohanty** - *Initial work* - [github](https://github.com/spMohanty)
* **Nikhil Rayaprolu** - *Initial work* (Current Maintainer) - [github](https://github.com/nikhilrayaprolu)   

See also the list of [contributors](https://github.com/spMohanty/aicrowd/contributors) who participated in this project.

## LicenseCopyright (c) AIcrowd SA

All rights reserved.
