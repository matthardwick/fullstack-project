import webapp2
import os
import jinja2

template_dir = os.path.join(os.path.dirname(__file__), 'templates')
jinja_env = jinja2.Environment(loader=jinja2.FileSystemLoader(template_dir),
                               autoescape=True)


def char_encrypt(char, alphabet):
    if char.isupper():
        alphabet = alphabet.upper()
        char = alphabet[alphabet.find(char) + 13]
        return char
    char = alphabet[alphabet.find(char) + 13]
    return char


def encrypt(text):
    alphabet = 'abcdefghijklmnopqrstuvwxyzabcdefghijklmABCDEFGHIJKLMNOPQRSTUVWXYZ'
    encrypted = ['']
    for char in text:
        if char in alphabet:
            char = char_encrypt(char, alphabet)
            encrypted.append(char)
        else:
            encrypted.append(char)
    return "".join(encrypted)


class Handler(webapp2.RequestHandler):

    def write(self, *a, **kw):
        self.response.out.write(*a, **kw)

    def render_str(self, template, **params):
        t = jinja_env.get_template(template)
        return t.render(params)

    def render(self, template, **kw):
        self.write(self.render_str(template, **kw))


class MainPage(Handler):

    def get(self):
        self.render("rot13.html")


class EncryptHandler(Handler):

    def get(self):
        self.render("rot13.html")

    def post(self):
        rottext = self.request.get("text")
        rottext = encrypt(rottext)
        self.render("rot13.html", rottext=rottext)

app = webapp2.WSGIApplication([('/', MainPage),
                               ('/rot13', EncryptHandler)
                              ],
                             debug=True)
