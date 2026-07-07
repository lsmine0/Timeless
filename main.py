from js import document, Decimal, Audio, window
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
    "resources_arr": [
        Decimal.new("0"), 
        Decimal.new("0"), 
        Decimal.new("0"), 
        Decimal.new("0")],
    "money": Decimal.new("100"),
    "click_power": [
        Decimal.new("1"),
        Decimal.new("1"),
        Decimal.new("1")],
    "sell_power": [
        Decimal.new("1"),
        Decimal.new("1")],
    "current_resource": ResourceType.BLOOD_ROCK
}

factories = {
    "F1" : [
        False,
        Decimal.new("0"),
        Decimal.new("1"),
        Decimal.new("10"),
        Decimal.new("1e6")
    ],
    "F2" : [
        False,
        Decimal.new("0"),
        Decimal.new("1"),
        Decimal.new("100"),
        Decimal.new("1e12")
    ],
    "F3" : [
        False,
        Decimal.new("0"),
        Decimal.new("1"),
        Decimal.new("1000"),
        Decimal.new("1e30")
    ],
    "F4" : [
        False,
        Decimal.new("0"),
        Decimal.new("1"),
        Decimal.new("10000"),
        Decimal.new("1e50")
    ]
}

settings = {

}


def unlock_f1():
    factories["F1"][0] = True
    pass

def unlock_f2():
    factories["F2"][0] = True
    pass

def unlock_f3():
    factories["F3"][0] = True
    pass
    
def unlock_f4():
    factories["F4"][0] = True
    pass

upgradelist = [
    {
        "purchased": False, 
        "id": "U1", 
        "cost": Decimal.new("20"), 
        "label": "Unlock Factory 1", 
        "action": unlock_f1
    },
    {
        "purchased": False, 
        "id": "U2", 
        "cost": Decimal.new("ee9.9"), 
        "label": "N̵̨̤̫̠͇̂̎͑̂̐̉͠U̴̧͈̞̱̲̗̾͑̓̃̊̿ͅḶ̵̡̰̪̝̦̳̳͂ͅL̷̢̝̙̩̜̫̣͉̝̜̜̓̍͛̚͝", 
        "action": unlock_f1
    },
    {
        "purchased": False, 
        "id": "U3", 
        "cost": Decimal.new("ee9.9"), 
        "label": "N̵̨̤̫̠͇̂̎͑̂̐̉͠U̴̧͈̞̱̲̗̾͑̓̃̊̿ͅḶ̵̡̰̪̝̦̳̳͂ͅL̷̢̝̙̩̜̫̣͉̝̜̜̓̍͛̚͝", 
        "action": unlock_f1
    },
    {
        "purchased": False, 
        "id": "U4", 
        "cost": Decimal.new("ee9.9"), 
        "label": "N̵̨̤̫̠͇̂̎͑̂̐̉͠U̴̧͈̞̱̲̗̾͑̓̃̊̿ͅḶ̵̡̰̪̝̦̳̳͂ͅL̷̢̝̙̩̜̫̣͉̝̜̜̓̍͛̚͝", 
        "action": unlock_f1
    },
    {
        "purchased": False, 
        "id": "U5", 
        "cost": Decimal.new("ee9.9"), 
        "label": "N̵̨̤̫̠͇̂̎͑̂̐̉͠U̴̧͈̞̱̲̗̾͑̓̃̊̿ͅḶ̵̡̰̪̝̦̳̳͂ͅL̷̢̝̙̩̜̫̣͉̝̜̜̓̍͛̚͝", 
        "action": unlock_f1
    },
    {
        "purchased": False, 
        "id": "U6", 
        "cost": Decimal.new("ee9.9"), 
        "label": "N̵̨̤̫̠͇̂̎͑̂̐̉͠U̴̧͈̞̱̲̗̾͑̓̃̊̿ͅḶ̵̡̰̪̝̦̳̳͂ͅL̷̢̝̙̩̜̫̣͉̝̜̜̓̍͛̚͝", 
        "action": unlock_f1
    },
    {
        "purchased": False, 
        "id": "U7", 
        "cost": Decimal.new("ee9.9"), 
        "label": "N̵̨̤̫̠͇̂̎͑̂̐̉͠U̴̧͈̞̱̲̗̾͑̓̃̊̿ͅḶ̵̡̰̪̝̦̳̳͂ͅL̷̢̝̙̩̜̫̣͉̝̜̜̓̍͛̚͝", 
        "action": unlock_f1
    }
]


def buy_upgrade(upgrade_id):
    user_cash = state["money"]
    # Locate target profile metadata matching targeted ID
    target_upg = next((u for u in upgradelist if u["id"] == upgrade_id), None)
    
    cost = target_upg["cost"]
    
    if user_cash.gte(cost):
        target_upg = next((u for u in upgradelist if u["id"] == upgrade_id), None)
        
        if not target_upg or target_upg["purchased"]:
            return

        target_upg["action"]() 
        
        # 2. Mark state status
        target_upg["purchased"] = True
        
        # 3. Destroy the HTML element completely
        card_element = document.getElementById(f"upg-card-{upgrade_id}")
        if card_element:
            card_element.remove()

        RebuilUpgradeList()    

def upgrade_handler(u_id):
    return create_proxy(lambda event: buy_upgrade(u_id))


def RebuilUpgradeList():
    container = document.getElementById("upgrades-container")
    if not container:
        return


    container.innerHTML = ""

    available_upgrades = [u for u in upgradelist if not u["purchased"]]
    

    sorted_upgrades = sorted(available_upgrades, key=lambda x: float(x["cost"].toString()))

    visible_upgrades = sorted_upgrades[:5]

    for upg in visible_upgrades:
        u_id = upg["id"]
        
        card = document.createElement("div")
        card.className = "card-item"
        card.id = f"upg-card-{u_id}"
        
        details = document.createElement("div")
        details.className = "card-details card-upgrade"
        
        label_span = document.createElement("span")
        label_span.className = "card-name"
        label_span.textContent = upg["label"]
        
        cost_span = document.createElement("span")
        cost_span.className = "card-cost"
        cost_span.textContent = f"💰 {upg['cost'].toString()}"
        
        details.appendChild(label_span)
        details.appendChild(cost_span)
        
        btn = document.createElement("button")
        btn.className = "secondary-btn"
        btn.id = f"upg-btn-{u_id}"
        btn.textContent = "Buy"
        
        btn.onclick = upgrade_handler(u_id)
        
        card.appendChild(details)
        card.appendChild(btn)
        
        container.appendChild(card)


Resource_multipliers = [
    Decimal.new("1"),
    Decimal.new("5"),
    Decimal.new("25"),
    Decimal.new("125")
    ]

click_sound = Audio.new("sound/click.wav")





def onSliderChange(event):
    slider = document.getElementById("sell-slider")
    display = document.getElementById("sell-percentage-display")
    sell_btn = document.getElementById("sell-btn-main")
    
    if not (slider and display and sell_btn):
        return
        
    percent_val = slider.value
    active_idx = state["current_resource"].value
    
    # 1. Grab base counts
    total_resources = state["resources_arr"][active_idx]
    
    # 2. Calculate target item fraction volume
    sell_percent = Decimal.new(percent_val).div(Decimal.new("100"))
    items_to_sell = total_resources.times(sell_percent).floor()
    
    # 3. Calculate expected cash value payload return
    item_value = Resource_multipliers[active_idx]
    expected_profit = items_to_sell.times(item_value)
    
    # 4. Update the text elements
    display.textContent = f"{percent_val}% ({items_to_sell.toString()} / {total_resources.floor().toString()})"
    sell_btn.textContent = f"Sell {items_to_sell.toString()} for 💰 {expected_profit.toString()}"




def update_ui():
    document.getElementById("money-val").textContent = state["money"].toString()
    
    for index, count in enumerate(state["resources_arr"]):
        target_el = document.getElementById(f"res-{index}")
        if target_el:
            target_el.textContent = count.floor().toString()

    onSliderChange(None)    

    for f_id, data in factories.items():
        is_unlocked = data[0]
        count = data[1]
        mult = data[2]
        cost = data[3]
        multcost =data[4]
        # 1. Update text displays dynamically
        count_el = document.getElementById(f"{f_id}-count")
        mult_el = document.getElementById(f"{f_id}-mult")
        cost_el = document.getElementById(f"{f_id}-cost")
        mulcost_el = document.getElementById(f"{f_id}-mult-cost")
        card_item = document.getElementById(f_id)
        
        if count_el: count_el.textContent = count.toString()
        if mult_el: mult_el.textContent = f"{mult.toString()}x"
        if cost_el: cost_el.textContent = cost.toString()
        if mulcost_el: mulcost_el.textContent = multcost.toString()
        
        if card_item:
            if is_unlocked:
                card_item.classList.remove("locked")
            else:
                card_item.classList.add("locked") 

    

def buy_factory(f_id, amount_type="1"):
    user_cash = state["money"]
    data = factories[f_id]
    cost = data[3]
    if not data[0]: 
        return
    ClickEffect()
    if amount_type == "1":
        if user_cash.gte(cost):
            state["money"] = user_cash.minus(cost)
            data[1] = data[1].plus(Decimal.new("1")) # Count += 1
            data[0] = True # Set isUnlocked to True
            # Simple scaling pricing mechanic: price * 1.5 per purchase
            data[3] = cost.times(Decimal.new("1.5")).floor() 
            
    elif amount_type == "max":
        # Check how many they can afford right now
        if user_cash.gte(cost):
            afford_count = user_cash.div(cost).floor()
            if afford_count.gt(0):
                total_spent = afford_count.times(cost)
                state["currency_str"] = user_cash.minus(total_spent)
                data[1] = data[1].plus(afford_count)
                data[0] = True
                data[3] = cost.times(Decimal.new("1.5").pow(afford_count)).floor()

    update_ui()                   

def upgrade_factory(f_id):
    user_cash = Decimal.new(state["money"])
    data = factories[f_id]
    
    up_cost = data[4]
    
    if user_cash.gte(up_cost):
        ClickEffect()
        state["money"] = user_cash.minus(up_cost)
        data[4] = data[4].pow(Decimal.new("2"))
        data[2] = data[2].plus(Decimal.new("1")) # Multiplier production step up +1
        update_ui()

# --- PROXY CLOSURES FOR CLICK ARGUMENTS ---
def make_buy_handler(f_id, amt):
    return create_proxy(lambda event: buy_factory(f_id, amt))

def make_upgrade_handler(f_id):
    return create_proxy(lambda event: upgrade_factory(f_id))
            
def onSellClick(event):
    """Sells only the dragged percentage fraction of the resources."""
    slider = document.getElementById("sell-slider")
    if not slider:
        return
        
    sell_percent = Decimal.new(slider.value).div(Decimal.new("100"))
    
    current_currency = Decimal.new(state["money"])
    total_profit = Decimal.new("0")
    
    for index, count_str in enumerate(state["resources_arr"]):
        total_items = Decimal.new(count_str)
        
        items_to_sell = total_items.times(sell_percent).floor() 
        items_remaining = total_items.minus(items_to_sell)
        
        item_value = Resource_multipliers[index]

        sellmult = state["click_power"][1]
        sellpow = state["click_power"][2]

        total_profit = total_profit.plus(items_to_sell.times(item_value.times(sellmult).pow(sellpow)))
        

        state["resources_arr"][index] = items_remaining
        
    new_currency_total = current_currency.plus(total_profit)
    state["money"] = new_currency_total
    ClickEffect()


    update_ui()

def ClickEffect():
    click_sound.currentTime = 0
    click_sound.play()

def onClickerClick(event):
    ClickEffect()


    active_idx = state["current_resource"].value
    
    current_resource_amt = state["resources_arr"][active_idx]
    clickflat = state["click_power"][0]
    clickmult = state["click_power"][1]
    clickpow = state["click_power"][2]

    delta = Decimal.new("0").plus(clickflat).mul(clickmult).pow(clickpow)
    state["resources_arr"][active_idx] = state["resources_arr"][active_idx].plus(delta)
    
    update_ui()


def game_tick():

    tick_fraction = Decimal.new("0.05")
    state_changed = False

    for index, f_id in enumerate(["F1", "F2", "F3", "F4"]):
        data = factories[f_id]
        is_unlocked = data[0]
        count = data[1]
        power = data[2]
        

        if is_unlocked and count.gt(0):
            produced_this_tick = count.pow(power).times(tick_fraction)
            
            if produced_this_tick.gt(0):
                # Add to current resource stockpile
                current_stock = state["resources_arr"][index]
                state["resources_arr"][index] = current_stock.plus(produced_this_tick)

    update_ui()

def setup_game_listeners(event=None):
    click_target = document.getElementById("clicker-image")
    if click_target:
        click_target.addEventListener("click", create_proxy(onClickerClick))

    shop_sell_btn = document.getElementById("sell-btn-main")
    if shop_sell_btn:
        shop_sell_btn.addEventListener("click", create_proxy(onSellClick))

    sell_slider = document.getElementById("sell-slider")
    if sell_slider:
        slider_proxy = create_proxy(onSliderChange)
        sell_slider.addEventListener("input", slider_proxy)

    for f_id in factories.keys():
        btn_buy1 = document.getElementById(f"{f_id}-buy1")
        btn_max = document.getElementById(f"{f_id}-buymax")
        btn_up = document.getElementById(f"{f_id}-upgrade")
        
        if btn_buy1: btn_buy1.addEventListener("click", make_buy_handler(f_id, "1"))
        if btn_max: btn_max.addEventListener("click", make_buy_handler(f_id, "max"))
        if btn_up: btn_up.addEventListener("click", make_upgrade_handler(f_id))

    tick_proxy = create_proxy(game_tick)
    window.setInterval(tick_proxy, 50)

    update_ui()
    RebuilUpgradeList()




if document.readyState == "complete":
    setup_game_listeners()
else:
    window.addEventListener("load", create_proxy(setup_game_listeners))