from js import document
from pyodide.ffi import create_proxy

gold = 0


def update_ui():
    document.getElementById(
        "gold"
    ).textContent = str(gold)


def mine(event):
    global gold
    gold += 1
    update_ui()

mine_proxy = create_proxy(mine)

document.getElementById(
    "mine"
).addEventListener(
    "click",
    mine_proxy
)

update_ui()