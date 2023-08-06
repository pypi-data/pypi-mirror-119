<!--
SPDX-FileCopyrightText: 2021 Magenta ApS <https://magenta.dk>
SPDX-License-Identifier: MPL-2.0
-->


# RA Flatfile importer

OS2mo/LoRa flatfile importer.

## Build
```
docker build . -t ra-flatfile-importer
```
Which yields:
```
...
Successfully built ...
Successfully tagged ra-flatfile-importer:latest
```
After which you can run:
```
docker run --rm ra-flatfile-importer
```
Which yields:
```
Usage: flatfile_importer.py [OPTIONS] COMMAND [ARGS]...

  Flatfile importer.

    Used to validate and load flatfile data (JSON) into OS2mo/LoRa.

  Options:
    --help  Show this message and exit.

  Commands:
    lora  Lora Flatfile importer.
    mo    OS2mo Flatfile importer.
```

## Usage
The primary usage of the tool is to upload flat-files to LoRa / OS2mo.
```
docker run --rm ra-flatfile-importer lora upload < lora.json
docker run --rm ra-flatfile-importer mo upload < mo.json
```

The tool can generate dummy files to test out this functionality:
```
docker run --rm ra-flatfile-importer lora generate --name "Aarhus Kommune" > lora.json
docker run --rm ra-flatfile-importer mo generate --name "Aarhus Kommune" > mo.json
```
These test files should be uploadable to Lora/MO and produce a valid MO instance.


The tool has various other commands too, such as producing the validation schema for the flat file format:
```
docker run --rm ra-flatfile-importer lora schema --indent 4
```
Which yields:
```
{
    "title": "LoraFlatFileFormatModel",
    "description": "Flatfile format for LoRa.\n\nMinimal valid example is {}.",
    "type": "object",
    "properties": {
        "facetter": {
           ...
        },
        ...
    }
}
```
Or for validating whether a file is invalid:
```
docker run --rm ra-flatfile-importer lora validate < lora.json
```

## Versioning
This project uses [Semantic Versioning](https://semver.org/) with the following strategy:
- MAJOR: Incompatible changes to existing commandline interface
- MINOR: Backwards compatible updates to commandline interface
- PATCH: Backwards compatible bug fixes

The fileformat is versioned directly, and the version is exported in the file itself.

<!--
## Getting Started

TODO: README section missing!

### Prerequisites


TODO: README section missing!

### Installing

TODO: README section missing!

## Running the tests

TODO: README section missing!

## Deployment

TODO: README section missing!

## Built With

TODO: README section missing!

## Authors

Magenta ApS <https://magenta.dk>

TODO: README section missing!
-->
## License
- This project: [MPL-2.0](MPL-2.0.txt)
- Dependencies:
  - pydantic: [MIT](MIT.txt)

This project uses [REUSE](https://reuse.software) for licensing. All licenses can be found in the [LICENSES folder](LICENSES/) of the project.
