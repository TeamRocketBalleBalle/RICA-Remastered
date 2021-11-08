from flask import current_app, g


def get_cursor(func):
    """
    wrapper function to start and close the connection to database whenever the other functions are called.
    :param func: function
    :return: function output
    """

    def wrap(*args, **kwargs):
        if 'cursor' not in g:
            g.cursor = current_app.mysql.connection.cursor()

        kwargs["cursor"] = g.cursor  # give the cursor argument to the func
        # call the function
        result = func(*args, **kwargs)
        return result
    wrap.__name__ = func.__name__
    return wrap
