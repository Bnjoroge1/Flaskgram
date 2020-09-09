from flask_login import current_user, login_required
from srcode.community import community

@login_required
@community.route('/' , subdomain = 'community')
def community():
     return '<h1>Commmmity </h1>'