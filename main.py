from js import document, Decimal
from pyodide.ffi import create_proxy
from enum import Enum

class ResourceType(Enum):
    BLOOD_ROCK = 0
    HOT_METAL = 1
    LIGHT_CRYSTAL = 2
    RED_DIAMOND = 3
    

# KILLER_FLOWER = 3
# TIME_REMNANT = 5

state = {
    "resources_arr": ["0", "0", "0", "0"],
    "money": "0",
    "click_power": ["1","1","1"],
    "sell_power": ["1","1"],
    "current_resource": ResourceType.BLOOD_ROCK
}

def onSliderChange(event):
    """Fires dynamically while the user drags the bar."""
    slider = document.getElementById("sell-slider")
    display = document.getElementById("sell-percentage-display")
    if slider and display:
        display.textContent = f"{slider.value}%"


def update_ui():
    document.getElementById("money-val").textContent = state["money"]
    
    for index, count_str in enumerate(state["resources_arr"]):
        target_el = document.getElementById(f"res-{index}")
        if target_el:
            target_el.textContent = count_str
            
def onSellClick(event):
    """Sells only the dragged percentage fraction of the resources."""
    slider = document.getElementById("sell-slider")
    if not slider:
        return
        
    sell_percent = Decimal.new(slider.value).div(Decimal.new("100"))
    
    current_currency = Decimal.new(state["money"])
    total_profit = Decimal.new("0")
    multipliers = ["1", "5", "25", "125"]
    
    for index, count_str in enumerate(state["resources_arr"]):
        total_items = Decimal.new(count_str)
        
        items_to_sell = total_items.times(sell_percent).floor() 
        items_remaining = total_items.minus(items_to_sell)
        
        item_value = Decimal.new(multipliers[index])

        sellmult = Decimal.new(state["click_power"][1])
        sellpow = Decimal.new(state["click_power"][2])

        total_profit = total_profit.plus(items_to_sell.times(item_value.times(sellmult).pow(sellpow)))
        

        state["resources_arr"][index] = items_remaining.toString()
        
    new_currency_total = current_currency.plus(total_profit)
    state["money"] = new_currency_total.toString()
    
    update_ui()

def onClickerClick(event):
    active_idx = state["current_resource"].value
    
    current_resource_amt = Decimal.new(state["resources_arr"][active_idx])
    clickflat = Decimal.new(state["click_power"][0])
    clickmult = Decimal.new(state["click_power"][1])
    clickpow = Decimal.new(state["click_power"][2])

    delta = Decimal.new("0").plus(clickflat).mul(clickmult).pow(clickpow)
    state["resources_arr"][active_idx] = Decimal.new(state["resources_arr"][active_idx]).plus(delta).toString()
    
    update_ui()


def setup_game_listeners(event=None):
    click_target = document.getElementById("clicker-image")
    if click_target:
        click_target.addEventListener("click", create_proxy(onClickerClick))

    shop_sell_btn = document.querySelector("#panel-shop .sell-btn")
    if shop_sell_btn:
        shop_sell_btn.addEventListener("click", create_proxy(onSellClick))

    sell_slider = document.getElementById("sell-slider")
    if sell_slider:
        slider_proxy = create_proxy(onSliderChange)
        sell_slider.addEventListener("input", slider_proxy)

    update_ui()

if document.readyState == "complete":
    setup_game_listeners()
else:
    window.addEventListener("load", create_proxy(setup_game_listeners))