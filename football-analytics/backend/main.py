from fastapi import FastAPI
from pydantic import BaseModel
import pandas as pd
import numpy as np
import json
from database import get_connection
from scraper import scrape_player_info

app = FastAPI(title="Football Analytics API")

# ---------------- AUTH ----------------
class LoginData(BaseModel):
    username: str
    password: str

@app.post("/login")
def login(data: LoginData):
    conn = get_connection()
    user = conn.execute(
        "SELECT * FROM users WHERE username=? AND password=?",
        (data.username, data.password)
    ).fetchone()
    conn.close()
    if user:
        return {"username": user["username"], "admin": bool(user["admin"])}
    return {"error": "Invalid credentials"}

# ---------------- PLAYERS ----------------
@app.get("/players")
def get_players():
    conn = get_connection()
    rows = conn.execute("SELECT * FROM players").fetchall()
    conn.close()
    return [dict(row) for row in rows]

@app.get("/stats")
def get_stats():
    conn = get_connection()
    df = pd.read_sql("SELECT Gls, Ast FROM players", conn)
    conn.close()
    return {
        "average_goals": float(np.mean(df["Gls"])),
        "average_assists": float(np.mean(df["Ast"])),
        "max_goals": int(np.max(df["Gls"])),
        "max_assists": int(np.max(df["Ast"]))
    }

@app.get("/player-info")
def player_info(name: str):
    return scrape_player_info(name)

# ---------------- ARTICLES CRUD ----------------
class ArticleCreate(BaseModel):
    title: str
    content: str
    author: str

@app.post("/articles")
def create_article(article: ArticleCreate, admin: bool = True):
    if not admin:
        return {"error": "Only admin can create articles"}
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO articles (title, content, author) VALUES (?, ?, ?)",
        (article.title, article.content, article.author)
    )
    conn.commit()
    conn.close()
    return {"message": "Article created"}

@app.get("/articles")
def get_articles():
    conn = get_connection()
    rows = conn.execute("SELECT * FROM articles").fetchall()
    conn.close()
    return [dict(row) for row in rows]

@app.put("/articles/{article_id}")
def update_article(article_id: int, article: ArticleCreate, admin: bool = True):
    if not admin:
        return {"error": "Only admin can update articles"}
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        "UPDATE articles SET title=?, content=?, author=? WHERE id=?",
        (article.title, article.content, article.author, article_id)
    )
    conn.commit()
    conn.close()
    return {"message": "Article updated"}

@app.delete("/articles/{article_id}")
def delete_article(article_id: int, admin: bool = True):
    if not admin:
        return {"error": "Only admin can delete articles"}
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM articles WHERE id=?", (article_id,))
    conn.commit()
    conn.close()
    return {"message": "Article deleted"}

# ---------------- FAVORITE XI CRUD ----------------
class FavoriteXI(BaseModel):
    username: str
    player_list: list

@app.post("/favorite-xi")
def create_favorite_xi(xi: FavoriteXI):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO favorite_xi (username, player_list) VALUES (?, ?)",
        (xi.username, json.dumps(xi.player_list))
    )
    conn.commit()
    conn.close()
    return {"message": "Favorite XI created"}

@app.get("/favorite-xi/{username}")
def get_favorite_xi(username: str):
    conn = get_connection()
    row = conn.execute("SELECT * FROM favorite_xi WHERE username=?", (username,)).fetchone()
    conn.close()
    if row:
        return {"username": row["username"], "player_list": json.loads(row["player_list"])}
    return {"message": "No favorite XI found"}

@app.put("/favorite-xi/{username}")
def update_favorite_xi(username: str, xi: FavoriteXI):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        "UPDATE favorite_xi SET player_list=? WHERE username=?",
        (json.dumps(xi.player_list), username)
    )
    conn.commit()
    conn.close()
    return {"message": "Favorite XI updated"}

@app.delete("/favorite-xi/{username}")
def delete_favorite_xi(username: str):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM favorite_xi WHERE username=?", (username,))
    conn.commit()
    conn.close()
    return {"message": "Favorite XI deleted"}
