# server.py
import os
from mcp.server.fastmcp import FastMCP
import sqlite3
import genanki
import random

mcp = FastMCP("gariben")

DATABASE_NAME = os.getenv("DATABASE_NAME")

DECK_ID = random.randrange(1 << 30, 1 << 31)
MODEL_ID = random.randrange(1 << 30, 1 << 31)
deck = genanki.Deck(DECK_ID, "Gariben Test Deck")


# really boilerplate model, nothing fancy
model = genanki.Model(
    MODEL_ID,
    "gariben-card",
    fields=[
        {"name": "Word"},
        {"name": "Translation"},
    ],
    templates=[
        {
            "name": "Card 1",
            "qfmt": "{{Word}}",
            "afmt": '{{FrontSide}}<hr id="answer">{{Translation}}',
        },
    ],
)


@mcp.tool()
def search_db(word: str) -> str:
    """
    Searches our DB for one Japanese word or kanji. Returns a string containing the Text matched in the DB as well as the date it was added to the DB.

    If there is no results, the string should be an empty list.

    Not necessary to run when adding cards.
    """
    res = cur.execute(f"select Text, DateCreated from WordList where Text='{word}'")
    return str(res.fetchall())


@mcp.tool()
def add_card(word, translation) -> str:
    """
    Adds card to Anki deck.
    """
    my_note = genanki.Note(model=model, fields=[word, translation])
    deck.add_note(my_note)
    return f"Added card for {word}"


@mcp.tool()
def save_deck() -> str:
    """
    Saves deck as file.
    """
    try:
        genanki.Package(deck).write_to_file("gariben-deck.apkg")
        return "Saved successfully."
    except Exception as e:
        return str(e)


if __name__ == "__main__":
    con = sqlite3.connect(DATABASE_NAME)
    cur = con.cursor()
    mcp.run(transport="stdio")
