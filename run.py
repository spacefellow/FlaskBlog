from views import *


admin.add_view(ModelView(Post, db.session))
admin.add_view(ModelView(User, db.session))
if __name__ == '__main__':
    app.run(debug=True)
