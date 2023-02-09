# import/migration helpers


## python3 [validate_single.py](./validate_single.py)
Validates _json_ file(s) intented to provide metadata for a single file.

### Requierments
- python3
- pydantic `python3 -m pip install pydantic`


### Validating json files
When `pydantic` has been installed, run:
```bash
python3 validate_single.py <first_filename.json> [second_filename.json] [...]
```

## Swagger / openAPI [openapi.json](./openapi.json)
If you have tools that use the openAPI format, a _version 3.0.2_ file with schemas has also been provided.

### FileImportModel schema
For single files metadata, the __FileImportModel__ schema is exspected to accopany the file.
