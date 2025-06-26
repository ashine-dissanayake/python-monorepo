import os
import sqlite3
from typing import Any, Dict, Union

from flask import Flask, flash, redirect, render_template, request, url_for
from werkzeug.exceptions import abort
from werkzeug.wrappers import Response as WerkzeugResponse

# Define custom types for better type hints
SqliteRow = Dict[str, Any]
ResponseType = Union[str, WerkzeugResponse]


def get_db_connection() -> sqlite3.Connection:
    """Create and return a database connection.

    Returns:
        sqlite3.Connection: A connection to the SQLite database.
    """
    basedir = os.path.abspath(os.path.dirname(__file__))
    db_path = os.path.join(basedir, "database.db")
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    return conn


def get_post(post_id: int) -> sqlite3.Row:
    """Retrieve a single post by its ID.

    Args:
        post_id: The ID of the post to retrieve.

    Returns:
        sqlite3.Row: The post data as a row object.

    Raises:
        HTTPException: If no post with the given ID is found.
    """
    conn = get_db_connection()
    post = conn.execute("SELECT * FROM posts WHERE id = ?", (post_id,)).fetchone()
    conn.close()
    if post is None:
        abort(404)
    # The post is guaranteed to be not None here because of the abort() call above
    return post


app = Flask(__name__)
app.config["SECRET_KEY"] = "asdfghjklqwertyuiopzxcvbnm"


@app.route("/")
def index() -> str:
    """Display all posts on the index page.

    Returns:
        str: Rendered HTML of the index page with all posts.
    """
    conn = get_db_connection()
    posts = conn.execute("SELECT * FROM posts").fetchall()
    conn.close()
    return render_template("index.html", posts=posts)


@app.route("/<int:post_id>")
def post(post_id: int) -> str:
    """Display a single post.

    Args:
        post_id: The ID of the post to display.

    Returns:
        str: Rendered HTML of the post page.
    """
    post = get_post(post_id)
    return render_template("post.html", post=post)


@app.route("/create", methods=("GET", "POST"))
def create() -> ResponseType:
    """Handle creation of a new post.

    Returns:
        Union[str, Response]: Either the create post form or a redirect to the index.
    """
    if request.method == "POST":
        title = request.form["title"]
        content = request.form["content"]

        if not title:
            flash("Title is required!")
        else:
            conn = get_db_connection()
            conn.execute(
                "INSERT INTO posts (title, content) VALUES (?, ?)", (title, content)
            )
            conn.commit()
            conn.close()
            return redirect(url_for("index"))

    return render_template("create.html")


@app.route("/<int:id>/edit", methods=("GET", "POST"))
def edit(id: int) -> ResponseType:
    """Edit an existing post.

    Args:
        id: The ID of the post to edit.

    Returns:
        Union[str, Response]: Either the edit form or a redirect to the index.
    """
    post = get_post(id)

    if request.method == "POST":
        title = request.form["title"]
        content = request.form["content"]

        if not title:
            flash("Title is required!")
        else:
            conn = get_db_connection()
            conn.execute(
                "UPDATE posts SET title = ?, content = ? WHERE id = ?",
                (title, content, id),
            )
            conn.commit()
            conn.close()
            return redirect(url_for("index"))

    return render_template("edit.html", post=post)


@app.route("/<int:id>/delete", methods=("POST",))
def delete(id: int) -> WerkzeugResponse:
    """Delete a post.

    Args:
        id: The ID of the post to delete.

    Returns:
        Response: Redirect to the index page.
    """
    post = get_post(id)
    conn = get_db_connection()
    conn.execute("DELETE FROM posts WHERE id = ?", (id,))
    conn.commit()
    conn.close()
    flash(f'"{post["title"]}" was successfully deleted!')
    return redirect(url_for("index"))
