![update-releases](https://github.com/test-and-trace-data/releases/workflows/update-releases/badge.svg)
![deploy](https://github.com/test-and-trace-data/releases/workflows/deploy/badge.svg)

# Register of software releases

This is a tool for publishing the release history for digital services. This repository contains tools for validating the data, updating the data and publishing the dataset as a website.

## Adding or editing products or services

Edit the csv files in the `data/` directory to add new products or services. Each record can have the following properties:

* **version:** the version number for the release
* **datetime:** the date and time the version was releases in [ISO 8601 date format](https://en.wikipedia.org/wiki/ISO_8601)
* **release_notes:** a description of the changes for this release

## Adding a new product or service

To add a new product or service, you can create a new csv file in the `data/` directory and add a new `resource` to the `datapackage.json` file.

## Software developers

If you are a software developer and want to run a local copy, first install Python 3 and Pip3, then follow these instructions:

```
git clone [THIS REPOSITORY] releases
cd releases
python3 -m venv env
source env/bin/activate
make validate
make web
```

To serve the site locally:

```
python3 -m http.server --directory _site/
```

### Publishing online

This tools is designed to be published on GitHub Pages. There is a GitHub Action that generates the site and copies it to a separate branch (gh-pages) on commit. You will need to enable Github Pages for that branch in the settings of your repository.


### Tools and scripts

* `python3 -m website.generator generate` will generate the static website
* `python3 -m website.tools updatetimestamp` will update the `updated` attribute in datapackage.json based on the latest edit in the `data/` directory.
* `python3  -m website.tools checkreleases` will check for new releases from the AppStore and PlayStore for IDs specified in `scripts/config.yml`
* `pytest` will run unit tests

### Configuration

Most configuration is handled by the datapackage.json file. Configuration that relates only to the generation of the web view or other tools is in `scripts/config.yaml`.
