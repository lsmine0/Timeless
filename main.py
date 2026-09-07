from js import document, Decimal, Audio, window
from pyodide.ffi import create_proxy
from enum import Enum
import random

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
    "money": Decimal.new("1e10"),
    "click_power": [
        Decimal.new("1"),
        Decimal.new("1"),
        Decimal.new("1")],
    "sell_power": [
        Decimal.new("1"),
        Decimal.new("1")],
    "factory_power": [
        Decimal.new("1"),
        Decimal.new("0")],    
    "current_resource": ResourceType.BLOOD_ROCK,
    "resource_unlock": [False, False, False],
    "U9_bought": False,
    "U10_bought": False,
    "UPotion_Unlock": False

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
        Decimal.new("1e24")
    ],
    "F4" : [
        False,
        Decimal.new("0"),
        Decimal.new("1"),
        Decimal.new("10000"),
        Decimal.new("1e48")
    ]
}

class PrintFormat(Enum):
    SCIENTIFIC = 0      # 1.23e100
    NORMAL = 1          # 123,456
    SHORT = 3           # 123, 1e6, 1e12
    LETTERS = 4         # 1.23K, 4.56Qa, 7.89Dc


settings = {
    "printFormat": PrintFormat.LETTERS
}



def unlock_f1():
    factories["F1"][0] = True

def mult_click_u2():
    state["click_power"][0] = state["click_power"][0].add(1)

def unlock_r2():
    state["resource_unlock"][0] = True;
    next_btn = document.querySelectorAll(".next-res")
    for btn in next_btn:
        btn.removeAttribute("hidden")
    prev_btn = document.querySelectorAll(".prev-res")
    for btn in prev_btn:
        btn.removeAttribute("hidden")

def unlock_f2():
    factories["F2"][0] = True        

def unlock_r3():
    state["resource_unlock"][1] = True


def unlock_f3():
    factories["F3"][0] = True

def unlock_r4():
    state["resource_unlock"][2] = True

def unlock_f4():
    factories["F4"][0] = True

def mult_click_u9():
    state["U9_bought"] = True

def factory_mult_u10():
    state["U10_bought"] = True

def unlock_potion():
    document.getElementById("Alchemy").removeAttribute("hidden")
    state["UPotion_Unlock"] = True    

upgradelist = [
    {
        "purchased": False, 
        "id": "U1", 
        "cost": Decimal.new("20"), 
        "label": "Unlock Factory 1", 
        "action": unlock_f1,
        "req": []
    },
    {
        "purchased": False, 
        "id": "U2", 
        "cost": Decimal.new("100"), 
        "label": "Base click power increased +1", 
        "action": mult_click_u2,
        "req": []
    },
    {
        "purchased": False, 
        "id": "U3", 
        "cost": Decimal.new("1000"), 
        "label": "Unlock Next Resource", 
        "action": unlock_r2,
        "req": []
    },
    {
        "purchased": False, 
        "id": "U4", 
        "cost": Decimal.new("2000"), 
        "label": "Unlock Factory 2", 
        "action": unlock_f2,
        "req": [ "U3" ]
    },
    {
        "purchased": False, 
        "id": "U5", 
        "cost": Decimal.new("25000"), 
        "label": "Unlock Next Resource", 
        "action": unlock_r3,
        "req": [ "U3" ]
    },
    {
        "purchased": False, 
        "id": "U6", 
        "cost": Decimal.new("30000"), 
        "label": "Unlock Factory 3", 
        "action": unlock_f3,
        "req": [ "U5" ]
    },
    {
        "purchased": False, 
        "id": "U7", 
        "cost": Decimal.new("1000000"), 
        "label": "Unlock Next Resource", 
        "action": unlock_r4,
        "req": [ "U5" ]
    },
    {
        "purchased": False, 
        "id": "U8", 
        "cost": Decimal.new("2000000"), 
        "label": "Unlock Next Resource", 
        "action": unlock_f4,
        "req": [ "U7" ]
    },
    {
        "purchased": False, 
        "id": "U9", 
        "cost": Decimal.new("200"), 
        "label": "Boost Click Power Based on Resource", 
        "action": mult_click_u9,
        "req": []
    },
    {
        "purchased": False, 
        "id": "U10", 
        "cost": Decimal.new("1500"), 
        "label": "Boost Previous Factory Based on Next Resource", 
        "action": factory_mult_u10,
        "req": [ "U3" ]
    },
    {
        "purchased": False, 
        "id": "U11", 
        "cost": Decimal.new("1e9"), 
        "label": "Unlock Alchemy", 
        "action": unlock_potion,
        "req": [ "U3" ]
    }
]

def show_click_popup(text, x, y):
    popup = document.createElement("div")

    popup.className = "click-popup"
    popup.textContent = text

    popup.style.left = f"{x + random.randint(-15, 15)}px"
    popup.style.top = f"{y + random.randint(-10, 10)}px"

    document.body.appendChild(popup)

    def remove_popup(event):
        popup.remove()

    remove_proxy = create_proxy(remove_popup)
    popup.addEventListener("animationend", remove_proxy)


def get_next_resource():
    current = state["current_resource"].value
    total = len(ResourceType)

    for offset in range(1, total + 1):
        next_id = (current + offset) % total

        # First resource is always unlocked
        if next_id == ResourceType.BLOOD_ROCK.value or state["resource_unlock"][next_id - 1]:
            state["current_resource"] = ResourceType(next_id)
            return state["current_resource"]

    return state["current_resource"]


def get_previous_resource():
    current = state["current_resource"].value
    total = len(ResourceType)

    for offset in range(1, total + 1):
        prev_id = (current - offset) % total

        # First resource is always unlocked
        if prev_id == ResourceType.BLOOD_ROCK.value or state["resource_unlock"][prev_id - 1]:
            state["current_resource"] = ResourceType(prev_id)
            return state["current_resource"]

    return state["current_resource"]


imageDict = {
    ResourceType.BLOOD_ROCK:  "img/BloodRockOfNight.png",
    ResourceType.HOT_METAL: "img/HotMetalOfLostWorld.png",
    ResourceType.LIGHT_CRYSTAL: "img/LightCrystalVariant2.png", 
    ResourceType.RED_DIAMOND: "img/RedDiamondOfTelor.png",
}

def change_img():
    document.querySelector("#clicker-image").src = imageDict[state["current_resource"]];
    document.querySelector(".resource-preview-wrapper").querySelector("img").src = imageDict[state["current_resource"]];


def buy_upgrade(upgrade_id):
    # Locate target profile metadata matching targeted ID
    target_upg = next((u for u in upgradelist if u["id"] == upgrade_id), None)
    cost = target_upg["cost"]
    
    if state["money"].gte(cost):
        target_upg = next((u for u in upgradelist if u["id"] == upgrade_id), None)
        
        if not target_upg or target_upg["purchased"]:
            return

        target_upg["action"]() 
        state["money"] = state["money"].minus(cost)
        # 2. Mark state status
        target_upg["purchased"] = True
        
        # 3. Destroy the HTML element completely
        card_element = document.getElementById(f"upg-card-{upgrade_id}")
        if card_element:
            card_element.remove()

        update_ui()
        RebuilUpgradeList()    

def upgrade_handler(u_id):
    return create_proxy(lambda event: buy_upgrade(u_id))

def upgrade_is_available(upg):
    for req_id in upg.get("req", []):
        required = next((u for u in upgradelist if u["id"] == req_id), None)

        if required is None or not required["purchased"]:
            return False

    return True

def RebuilUpgradeList():
    container = document.getElementById("upgrades-container")
    if not container:
        return


    container.innerHTML = ""

    available_upgrades = [
        u for u in upgradelist
        if not u["purchased"] and upgrade_is_available(u)
    ]
    

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
        cost_span.textContent = f"💰 {DisplayNumber(upg['cost'].ceil())}"
        
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
    display.textContent = f"{percent_val}% ({DisplayNumber(items_to_sell)} / {DisplayNumber(total_resources.floor())})"
    sell_btn.textContent = f"Sell {DisplayNumber(items_to_sell)} for 💰 {DisplayNumber(expected_profit)}"




def update_ui():
    document.getElementById("money-val").textContent = DisplayNumber(state["money"].floor())
    
    for index, count in enumerate(state["resources_arr"]):
        target_el = document.getElementById(f"res-{index}")
        if target_el:
            target_el.textContent = DisplayNumber(count.floor())

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
  
        if count_el: count_el.textContent = DisplayNumber(count)
        if mult_el: mult_el.textContent = f"{DisplayNumber(mult)} x"
        if cost_el: cost_el.textContent = DisplayNumber(cost)
        if mulcost_el: mulcost_el.textContent = DisplayNumber(multcost)
        
        if card_item:
            if is_unlocked:
                card_item.classList.remove("locked")
            else:
                card_item.classList.add("locked") 

    

def buy_factory(f_id, amount_type="1", silent=False):
    user_cash = state["money"]
    data = factories[f_id]
    cost = data[3]
    if not data[0]: 
        return

    if amount_type == "1":
        if user_cash.gte(cost):
            if not silent:
                ClickEffect()
            state["money"] = user_cash.minus(cost)
            data[1] = data[1].plus(Decimal.new("1")) # Count += 1
            data[0] = True # Set isUnlocked to True
            # Simple scaling pricing mechanic: price * 1.5 per purchase
            data[3] = cost.times(Decimal.new("2"))
            
    elif amount_type == "max":
        # Check how many they can afford right now
        if user_cash.gte(cost):
            if not silent:
                ClickEffect()

            ratio = user_cash.div(cost)
            afford_count = Decimal.log2(ratio).floor()

            if afford_count.gt(0):
                # Total spent = base * (2^n - 1)
                total_spent = cost.times(
                    Decimal.new("2").pow(afford_count)
                    .minus(Decimal.new("1"))
                )

                state["money"] = user_cash.minus(total_spent)
                data[1] = data[1].plus(afford_count)
                data[0] = True

                # Next price after n purchases
                data[3] = cost.times(Decimal.new("2").pow(afford_count))
                buy_factory(f_id, silent=True)
    update_ui()                   

def upgrade_factory(f_id):
    user_cash = Decimal.new(state["money"])
    data = factories[f_id]
    
    up_cost = data[4]
    
    if user_cash.gte(up_cost):
        ClickEffect()
        state["money"] = user_cash.minus(up_cost)
        data[4] = data[4].times(Decimal.new("1e6"))
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
    
    index = state["current_resource"].value
    total_items = state["resources_arr"][index]
            
    items_to_sell = total_items.times(sell_percent).floor() 
    items_remaining = total_items.minus(items_to_sell)
            
    item_value = Resource_multipliers[index]

    sellmult = state["sell_power"][0]
    sellpow = state["sell_power"][1]

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

    if state["U9_bought"]:
        for resource in state["resources_arr"]:
            if resource.lt(2):
                continue    
            delta = delta.times(resource.log10())    



    show_click_popup(
        f"{DisplayNumber(delta)}",
        event.clientX,
        event.clientY
    )


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
        
        mult = state["factory_power"][0]
        powe = state["factory_power"][1]

        if is_unlocked and count.gt(0):

            
            production_second = count.times(Decimal.new(2).pow(power))
            if state["U10_bought"] and index < len(state["resources_arr"]) - 1:
                next_resource = state["resources_arr"][index + 1]

                if next_resource.gt(1):
                    resource_log = next_resource.log(300).plus(1)
                    production_second = production_second.pow(resource_log)

            document.getElementById(f"{f_id}-prod").textContent = DisplayNumber(production_second)    

            if production_second.gt(0):
                produced_this_tick = production_second.times(tick_fraction)
                # Add to current resource stockpile
                current_stock = state["resources_arr"][index]
                state["resources_arr"][index] = current_stock.plus(produced_this_tick)

    update_ui()




def DisplayNumber(value):
    match settings["printFormat"]:
        case PrintFormat.SCIENTIFIC:
            return value.toExponential(2)
        case PrintFormat.NORMAL:
            return value.toStringWithDecimalPlaces(2)
        case PrintFormat.SHORT:
            if value.lt(1e6):
                return value.toStringWithDecimalPlaces(0)
            return value.toExponential(1)
        case PrintFormat.LETTERS:
            suffixes = [
            "", "K", "M", "B", "T",
            "Qa", "Qi", "Sx", "Sp", "Oc", 
            "No", "Dc", "UDc", "DDc", "TDc",
            "QaDc", "QiDc", "SxDc", "SpDc",
            "OcDc", "NoDc", "Vg", "UVg",
            "DVg", "TVg", "QaVg", "QiVg",
            "SxVg", "SpVg", "OVg", "NVg",
            "Tg", "Tgm","G",   
            ]

            if value.lt(1000):
                return value.toStringWithDecimalPlaces(0)

            power = value.log10().floor()
            tier = power.div(3).floor()

            if tier.lt(len(suffixes)):
                divisor = Decimal.new(1000).pow(tier)
                scaled = value.div(divisor)

                return (
                    scaled.toStringWithDecimalPlaces(2)
                    + suffixes[tier.toNumber()]
                )

            return value.toExponential(2)

def next_resource(event):
    get_next_resource()
    change_img()
    update_ui()

def prev_resource(event):
    get_previous_resource()
    change_img()
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

    next_btn = document.querySelectorAll(".next-res")
    prev_btn = document.querySelectorAll(".prev-res")
    for btn in next_btn:
        btn.addEventListener("click", create_proxy(next_resource))    
    
    for btn in prev_btn:
        btn.addEventListener("click", create_proxy(prev_resource))

    tick_proxy = create_proxy(game_tick)
    window.setInterval(tick_proxy, 50)

    update_ui()
    RebuilUpgradeList()



if document.readyState == "complete":
    setup_game_listeners()
else:
    window.addEventListener("load", create_proxy(setup_game_listeners))