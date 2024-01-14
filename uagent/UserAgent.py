from uagents import Agent, Context, Model

class InventoryMessage(Model):
    item: str
    message: str

UserAgent = Agent(
    name="dods",
    port=8003,
    seed="user_secret_phrase",
    endpoint=["http://127.0.0.1:8003/submit"],
)

async def process_inventory_message(ctx: Context, sender: str, msg: InventoryMessage):
    ctx.logger.info(f"Received message from {sender}: {msg.message} for {msg.item}")
    print(f"Received inventory alert for {msg.item}: {msg.message}")

@UserAgent.on_message(model=InventoryMessage)
async def inventory_message_handler(ctx: Context, sender: str, msg: InventoryMessage):
    await process_inventory_message(ctx, sender, msg)

if __name__ == "__main__":
    UserAgent.run()
