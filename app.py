from flask import Flask, render_template, request
import os
import markdown
import frontmatter
from datetime import datetime



app = Flask(__name__)

@app.context_processor
def inject_now():
    return {'now': datetime.utcnow()}

@app.route('/')
def index():
    return render_template('home.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/blog')
def blog():
    posts = []
    for filename in os.scandir('./posts'):
        if filename.name.endswith('.md') and filename.is_file():
            with open(filename, 'r') as file:
                post = frontmatter.load(file)
                if not post['draft']:
                    posts.append(post)
    return render_template('blog.html', posts=posts)

@app.route('/blog/<string:slug>')
def post(slug):
    posts = []
    for filename in os.scandir('./posts'):
        if filename.name.endswith('.md') and filename.is_file():
            with open(filename, 'r') as file:
                post = frontmatter.load(file)
            if not post['draft']:
                content = markdown.markdown(post.content)
                posts.append((post, content))  #
    for post, content in posts: #
        if post['slug'] == slug: #
            return render_template('post.html', post=post, content=content, tags=post['tags'])   #  
    return render_template('404.html'), 404
  

@app.route('/tags')
def tags():
    tags = {}
    for filename in os.scandir('./posts'):
        if filename.name.endswith('.md') and filename.is_file():
            with open(filename, 'r') as file:
                post = frontmatter.load(file)
                if not post['draft']:
                    for tag in post['tags']:
                        tags[tag] = tags.get(tag, 0) + 1
                           
    return render_template('tags.html', tags=tags)

@app.route('/tags/<string:tag>')
def tag(tag):
    posts = []
    for filename in os.scandir('./posts'):
        if filename.name.endswith('.md') and filename.is_file():
            with open(filename, 'r') as file:
                post = frontmatter.load(file)
                if not post['draft'] and tag in post['tags']:
                    posts.append(post)
    return render_template('tag.html', tag=tag, posts=posts)

@app.route('/contact')   
def contact():
    return render_template('contact.html')

if __name__ == '__main__':
    app.run(debug=True)
