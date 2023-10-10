# Speckle Automate function template - Python


This is a template repository for a Speckle Automate functions written in python
using the [specklepy](https://pypi.org/project/specklepy/) SDK to interact with Speckle data.

This template contains the full scaffolding required to publish a function to the automate environment.
Also has some sane defaults for a development environment setups.

## Getting started

1. Use this template repository to create a new repository in your own / organization's profile.

Register the function 

### Add new dependencies

To add new python package dependencies to the project, use:
`$ poetry add pandas`

### Change launch variables

describe how the launch.json should be edited

### Github Codespaces

create new repo from template, and use the create new code


### Local dev environment




# Archive

This is a simple example of how to use the Speckle Automate Python package to automate the creation of a Speckle stream.


## Using this Speckle Function

1. [Create](https://automate.speckle.dev/) a new Speckle Automation.
1. Select your Speckle Project and Speckle Model.
1. Select the existing Speckle Function named [`Random comment on IFC beam`](https://automate.speckle.dev/functions/e110be8fad).
1. Enter a phrase to use in the comment.
1. Click `Create Automation`.

## Getting Started with creating your own Speckle Function

1. [Fork](https://docs.github.com/en/get-started/quickstart/fork-a-repo) this repository.
1. [Clone](https://docs.github.com/en/get-started/quickstart/fork-a-repo#cloning-your-forked-repository) your forked repository to your development environment, or use [GitHub CodeSpaces](https://github.com/features/codespaces).
1. [Register](https://automate.speckle.dev/) your Function with [Speckle Automate](https://automate.speckle.dev/).
1. After completing the registration of the Function you will be shown a Function Publish Token and a Function ID. You will need these later.
1. Save your Function Publish Token as a [GitHub Action Secret](https://docs.github.com/en/actions/security-guides/encrypted-secrets#creating-encrypted-secrets-for-a-repository) named `SPECKLE_AUTOMATE_FUNCTION_PUBLISH_TOKEN`.
1. Save your Function ID as a [GitHub Action Secret](https://docs.github.com/en/actions/security-guides/encrypted-secrets#creating-encrypted-secrets-for-a-repository) named `SPECKLE_AUTOMATE_FUNCTION_ID`.
1. Make changes to your Function in `main.py`. See below for the Developer Requirements, and instructions on how to test.
1. Every commit to `main` branch will create a new version of your Speckle Function.

## Developer Requirements

1. Install the following:
    - [Python 3](https://www.python.org/downloads/)
    - [Poetry](https://python-poetry.org/docs/#installing-with-the-official-installer)
1. Run `poetry shell && poetry install` to install the required Python packages.

## Building and Testing

The code can be tested locally by running `poetry run pytest`.
The code should also be packaged into the format required by Speckle Automate, a Docker Container Image, and that should also be tested.

## Resources

- [Learn](https://speckle.guide/dev/python.html) more about SpecklePy, and interacting with Speckle from Python.
