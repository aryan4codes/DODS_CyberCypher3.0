from uagents import Agent, Context, Model
from uagents.setup import fund_agent_if_low

class InventoryMessage(Model):
    item: str
    message: str

grocery_agent = Agent(
    name="grocery_agent",
    port=8004,
    seed="grocery_secret_phrase",
    endpoint=["http://127.0.0.1:8004/submit"],
)

fund_agent_if_low(grocery_agent.wallet.address())

# Define the inventory levels for each item in the grocery store
inventory_levels = {
    "SUGAR": {"min_quantity": 10, "max_quantity": 50},
    "WHEAT": {"min_quantity": 5, "max_quantity": 30},
    "COLD DRINKS": {"min_quantity": 7, "max_quantity": 40},
    # Add more items as needed
}

async def notify_user(ctx: Context, item, message):
    user_address = "agent1qg9ymqksph0d778ewuul5f9pj39f7xrezjhzp0c9s6xp4c3yfxu8jhthrhv"  # Replace with the actual UserAgent address

    # Create a message object with a valid model schema
    message_obj = InventoryMessage(item=item, message=message)

    # Send the message to the user agent
    await ctx.send(user_address, message_obj)

def monitor_inventory():
    alerts = []
    for item, levels in inventory_levels.items():
        current_quantity = int(input(f"Enter current quantity for {item}: "))
        min_quantity = levels["min_quantity"]
        max_quantity = levels["max_quantity"]

        if current_quantity < min_quantity:
            alerts.append(f"Inventory for {item} is below the minimum limit ({min_quantity}).")
        elif current_quantity > max_quantity:
            alerts.append(f"Inventory for {item} is above the maximum limit ({max_quantity}).")

    return alerts

@grocery_agent.on_interval(period=3600.0)  # Check every hour
async def inventory_monitor(ctx: Context):
    inventory_alerts = monitor_inventory()
    ctx.logger.info(inventory_alerts)

    for alert in inventory_alerts:
        item_name = alert.split()[2]
        await notify_user(ctx, item_name, alert)

if __name__ == "__main__":
    grocery_agent.run()
