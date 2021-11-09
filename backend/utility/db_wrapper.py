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
        try:
            # print("before wrapper")
            result = func(*args, **kwargs)
        except Exception as e:
            # print("EXCEPTION HANDLED")
            g.cursor.close()
            g.pop("cursor")

            # this important line does not ending up CORRUPTING the database leading to its deletion in the db
            current_app.mysql.connection.rollback()
            raise e
        else:
            current_app.mysql.connection.commit()

        return result
    wrap.__name__ = func.__name__
    return wrap
