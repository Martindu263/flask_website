from app import create_app, db
from app.models import User, Post
#加上下两行代码原因是进flaskshell的时候不用再次命令行导入

app = create_app()

@app.shell_context_processor
def make_shell_context():
	return {'db': db, 'User': User, 'Post': Post}

if __name__ == '__main__':
	app.run(debug=True)