from srcode import app
import os, click

def startup(app):
    @app.cli.group()
    def translate():
        """Translation and localization commands for easier translations. Parent command that provides a base for other commands below"""
        pass

    @translate.command()
    @click.argument('lang')
    def update():
        '''update all the languages'''
        if os.system('pybabel extract -F babel.cfg -k _l -o messages.pot .'):
            raise RuntimeError('extract command failed')
        if os.system('pybabel update -i messages.pot -d srcode/translations'):
            raise RuntimeError('update command failed')
        os.remove('messages.pot')

    @translate.command()
    def compile():
        """Compile all languages."""
        if os.system('pybabel compile -d srcode/translations'):
            raise RuntimeError('compile command failed')

    @translate.command()
    @click.argument('lang')
    def init(lang):
        """Initialize a new language."""
        if os.system('pybabel extract -F babel.cfg -k _l -o messages.pot .'):
            raise RuntimeError('extract command failed')
        if os.system(
                'pybabel init -i messages.pot -d srcode/translations -l ' + lang):
            raise RuntimeError('init command failed')
        os.remove('messages.pot')     