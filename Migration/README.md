# Migrating your files to Documaster

In order to get your files into Documaster in the easist possible way, we have defined a [JSON Schema](https://json-schema.org) model describing each file to be migrated.

JSON Schema is a well-known format that allows you to define and validate JSON documents.

Each source file should be accompanied by a JSON metadata file which follows the model.

Using JSON Schema, you can validate your metadata files to verify that they follow the format expected by Documaster. This is important to avaid any problems in the migration process.


## Validation of metadata files

### Validation online
https://www.jsonschemavalidator.net provides a free an easy to use validator.

Simply paste in [the model](./model.schema.json) on the left, and your JSON on the right.


### Validation with Python
If you have access to developers, you can also use Python to validate metadata files.

#### Requierments
- **python3**
- **jsonschema** `python3 -m pip install jsonschema`

#### Validating json files
```bash
jsonschema --instance <first_filename.json> [second_filename.json] [...] model.schema.json
```

##### Example
```bash
jsonschema --instance examples/complete-example.json model.schema.json
```

#### Resources
- https://github.com/python-jsonschema/jsonschema
