from flask import Flask, render_template, request, redirect, url_for
import json
app = Flask(__name__)

def load_posts():
    """Gets the posts from json storage."""
    with open('blog_posts.json', 'r') as f:
        return json.load(f)

@app.route('/')
def index():
    """Loads the template for displaying the homepage."""
    blog_posts = load_posts()
    return render_template('index.html', posts=blog_posts)

@app.route('/add', methods=['GET', 'POST'])
def add():
    """Add a blog post."""
    if request.method == 'POST':
        with open('blog_posts.json', 'r') as f:
            blog_posts = json.load(f)

        title = request.form.get('title')
        author = request.form.get('author')
        content = request.form.get('content')

        new_id = max(post['id'] for post in blog_posts) + 1 if blog_posts else 1

        new_post = {'id': new_id, 'author': author, 'title': title, 'content': content}
        blog_posts.append(new_post)

        with open('blog_posts.json', 'w') as f:
            json.dump(blog_posts, f, indent=2)

        return redirect(url_for('index'))

    return render_template('add.html')

@app.route('/delete/<int:post_id>')
def delete(post_id):
    """Delete a blog post by its ID and redirect to the homepage."""
    with open('blog_posts.json', 'r') as f:
        blog_posts = json.load(f)

    blog_posts = [post for post in blog_posts if post['id'] != post_id]

    with open('blog_posts.json', 'w') as f:
        json.dump(blog_posts, f, indent=2)

    return redirect(url_for('index'))

@app.route('/update/<int:post_id>', methods=['GET', 'POST'])
def update(post_id):
    """Update an existing blog post by ID, using a form."""
    with open('blog_posts.json', 'r') as f:
        blog_posts = json.load(f)

    post = next((p for p in blog_posts if p['id'] == post_id), None)
    if post is None:
        return "Post not found", 404

    if request.method == 'POST':
        post['title'] = request.form.get('title')
        post['author'] = request.form.get('author')
        post['content'] = request.form.get('content')

        with open('blog_posts.json', 'w') as f:
            json.dump(blog_posts, f, indent=2)

        return redirect(url_for('index'))

    return render_template('update.html', post=post)

@app.route('/like/<int:post_id>')
def like(post_id):
    """Increment the like count for a blog post and redirect to homepage."""
    with open('blog_posts.json', 'r') as f:
        blog_posts = json.load(f)

    for post in blog_posts:
        if post['id'] == post_id:
            post['likes'] = post.get('likes', 0) + 1

    with open('blog_posts.json', 'w') as f:
        json.dump(blog_posts, f, indent=2)

    return redirect(url_for('index'))





if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5001, debug=True)