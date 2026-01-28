from utils.request import parse_form

def get_form(req):
    """
    Lazily parse POST form data.
    Safe: only reads body when needed.
    """
    environ = req["environ"]

    if "_parsed_form" in environ:
        return environ["_parsed_form"], environ.get("_parsed_file")

    form, file_item = parse_form(environ)

    environ["_parsed_form"] = form or {}
    environ["_parsed_file"] = file_item

    return environ["_parsed_form"], environ["_parsed_file"]
