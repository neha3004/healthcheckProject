# Health check project

This application runs the health checks that are provided in the form of a yaml file. These checks are run every 15 seconds.

## Setup

Clone the project from the main branch.

## Pre-requisites

Install the required packages by running the requirements.txt file.

```
pip install -r requirements.txt
```

## Implementation

Run the main.py by providing the yaml file which has all the health checks as an argument.

For example:

```
python main.py healthchecks.yaml
```
