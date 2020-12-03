from re import split


def snake_case_to_camel_case(string: str) -> str:
    return ''.join(a.capitalize() for a in split('([^a-zA-Z0-9])', string)if a.isalnum())
    # return ''.join(word.title() for word in string.split('_'))
