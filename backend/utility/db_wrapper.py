from flask import current_app


def get_cursor(func):
    """
    wrapper function to start and close the connection to database whenever the other functions are called.
    :param func: function
    :return: function output
    """

    def wrap(*args, **kwargs):
        cursor = current_app.mysql.connection.cursor()
        args += (cursor,)  # give the cursor argument to the func
        # call the function
        result = func(*args, **kwargs)
        return result

    return wrap
