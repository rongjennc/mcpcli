import typer
from mcpcli import config, client
import toml
import asyncio
import logging
from aioconsole import ainput

app = typer.Typer()
accounts_app = typer.Typer()
llms_app = typer.Typer()

app.add_typer(accounts_app, name="accounts")
app.add_typer(llms_app, name="llms")

discover_app = typer.Typer()
app.add_typer(discover_app, name="discover")

@accounts_app.command("add")
def accounts_add(
    name: str = typer.Argument(..., help="A unique name for the account"),
    jid: str = typer.Option(..., help="The JID of the account (e.g., user@example.com)"),
    password: str = typer.Option(..., help="The password for the account")
):
    """Adds a new XMPP account to the configuration."""
    try:
        config.add_account(name, jid, password)
        print(f"Account '{name}' added successfully.")
    except Exception as e:
        print(f"Error adding account: {e}")

@accounts_app.command("list")
def accounts_list():
    """Lists the configured XMPP accounts."""
    try:
        conf = config.load_config()
        accounts = conf.get("accounts", {})
        if not accounts:
            print("No accounts configured.")
            return
        print("Configured accounts:")
        for name, account_details in accounts.items():
            print(f"- {name}: {account_details['jid']}")
    except Exception as e:
        print(f"Error listing accounts: {e}")

@llms_app.command("add")
def llms_add(
    name: str = typer.Argument(..., help="A unique name for the LLM profile"),
    account: str = typer.Option(..., help="The account name to use for this LLM"),
    room_jid: str = typer.Option(..., help="The JID of the MUC room for the LLM"),
    nickname: str = typer.Option(..., help="The nickname to use in the room")
):
    """Adds a new LLM profile to the configuration."""
    try:
        conf = config.load_config()
        if account not in conf.get("accounts", {}):
            print(f"Error: Account '{account}' not found. Please add it first with 'mcpcli accounts add {account}'.")
            raise typer.Exit(code=1)
        config.add_llm(name, account, room_jid, nickname)
        print(f"LLM profile '{name}' added successfully.")
    except Exception as e:
        print(f"Error adding LLM profile: {e}")

@llms_app.command("list")
def llms_list():
    """Lists the configured LLM profiles."""
    try:
        conf = config.load_config()
        llms = conf.get("llms", {})
        if not llms:
            print("No LLM profiles configured.")
            return
        print("Configured LLM profiles:")
        for name, llm_details in llms.items():
            print(f"- {name}:")
            print(f"  - Account: {llm_details['account']}")
            print(f"  - Room JID: {llm_details['room_jid']}")
            print(f"  - Nickname: {llm_details['nickname']}")
    except Exception as e:
        print(f"Error listing LLM profiles: {e}")

async def amain(llm_name: str):
    conf = config.load_config()
    llm_profile = conf.get("llms", {}).get(llm_name)
    if not llm_profile:
        print(f"LLM profile '{llm_name}' not found.")
        return

    account_name = llm_profile["account"]
    account = conf.get("accounts", {}).get(account_name)
    if not account:
        print(f"Account '{account_name}' for LLM profile '{llm_name}' not found.")
        return

    jid = account["jid"]
    password = account["password"]
    room = llm_profile["room_jid"]
    nick = llm_profile["nickname"]

    xmpp = client.MUCClient(jid, password, room, nick)

    # Setup logging.
    # logging.basicConfig(level=logging.DEBUG, format='%(levelname)-8s %(message)s')

    xmpp.connect()

    # Process packets in the background
    async def process_packets():
        xmpp.process(forever=False)

    # User input loop
    async def send_messages():
        while True:
            try:
                line = await ainput("> ")
                if line.strip().lower() == "/quit":
                    xmpp.disconnect()
                    break
                await xmpp.send_group_message(line)
            except (EOFError, KeyboardInterrupt):
                xmpp.disconnect()
                break

    await asyncio.gather(
        process_packets(),
        send_messages(),
    )

@discover_app.command("services")
def discover_services(
    server: str = typer.Argument(..., help="The server to discover services on."),
    jid: str = typer.Option(..., help="A JID on the server for authentication."),
    password: str = typer.Option(..., help="The password for the JID.")
):
    """Discovers MUC services on a given XMPP server."""
    # logging.basicConfig(level=logging.DEBUG, format='%(levelname)-8s %(message)s')
    xmpp = client.DiscoveryClient(jid, password, server)
    xmpp.connect()
    xmpp.process(forever=False)

@discover_app.command("rooms")
def discover_rooms(
    service_jid: str = typer.Argument(..., help="The JID of the MUC service."),
    jid: str = typer.Option(..., help="A JID on the server for authentication."),
    password: str = typer.Option(..., help="The password for the JID.")
):
    """Discovers public rooms on a given MUC service."""
    # logging.basicConfig(level=logging.DEBUG, format='%(levelname)-8s %(message)s')
    xmpp = client.RoomDiscoveryClient(jid, password, service_jid)
    xmpp.connect()
    xmpp.process(forever=False)

@app.command()
def chat(llm_name: str = typer.Argument(..., help="The name of the LLM profile to chat with")):
    """Starts a chat session with a configured LLM."""
    try:
        asyncio.run(amain(llm_name))
    except KeyboardInterrupt:
        print("\nExiting chat.")

if __name__ == "__main__":
    app()
