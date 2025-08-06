from flask import render_template
from app import db
from app.models import Post
from app import app

# Define the route for the dashboard
@app.route('/dashboard')
def dashboard():
    # Query the database to get all posts
    posts = Post.query.all()
    
    # Render the dashboard.html template, passing the posts data
    return render_template('dashboard.html', posts=posts)
