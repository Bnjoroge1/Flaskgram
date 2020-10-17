from srcode import app, create_current_app, db, cli
from srcode.models import Message, Notification, Task, User, Post

app = create_current_app()
cli.startup(app)

@app.shell_context_processor
def make_shell_context():
    return {'db': db, 'User':User, 'Post':Post, 'Notification': Notification, 'Message' : Message, 'Task' : Task}
def main():
    app.run(debug=True, ssl_context="adhoc", host= '0.0.0.0', port = 5000) 
    
if __name__ == '__main__':
    main()