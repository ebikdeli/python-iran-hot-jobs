def _insert_fields_values(data:dict, string_fields:list=[], ignore_none: bool=True) -> tuple[str]|None:
    """For sql insert, with this function we can insert any arbitrary number of fields and values into db when using:\n
    "INSERT INTO table (...fields...) VALUES (...values...)"\n
    without hardcoding exact fields and their respective values into db.\n
    "data" is a dictionary contains data should be inserted into db as {field1: value1, field2: value2, ...}.\n
    "string_fields" is a list of string fields to tells the function if value of the field must have string character
    'value' around it to be inserted into the db without error.\n
    "ignore_none" is a boolean. If it is True, if the field has no value in it, ignore the field and its value.\n
    Returns 2-element tuple. First element is a string represents (...fields...) as comma separated.
    Second element is a string represnts (...values...) as comma separated.\n
    If exception raised return None.
    """
    try:
        fields = str()
        values = str()
        for k, v in data.items():
            # Ignore fields with no value in them
            if ignore_none:
                if not v:
                    continue
            fields += str(k) + ', '
            # Put stirng character '' around the value of the field
            if k in string_fields:
                values += "'" + str(v) + "'" + ', '
            else:
                values += str(v) + ', '
        return fields[:-2], values[:-2]
    except Exception as e:
        print('Error in "database._helper_functions._insert_fields_values":\n', e.__str__())
