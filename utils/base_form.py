from wtforms import Form

class BaseForm(Form):
    def get_error(self):
        error = self.errors.popitem()[1][0]
        return error