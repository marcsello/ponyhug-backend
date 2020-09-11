#!/usr/bin/env python3


def get_standard_error_handler(code: int):
    def error_handler(err):
        return {"msg": str(err)}, code

    return error_handler


# function to register all handlers


def register_all_error_handlers(app):
    error_codes_to_override = [404, 403, 401, 405, 400, 409, 422]

    for code in error_codes_to_override:
        app.register_error_handler(code, get_standard_error_handler(code))
