# MCPCLI

A terminal-based client for MCP (Multi-provider Chat Protocol) servers. This tool allows you to connect to and interact with various LLMs that expose an MCP interface, which is based on the XMPP Multi-User Chat (MUC) protocol (XEP-0045).

## Features

*   Connect to one or more MUC rooms.
*   Add and configure multiple XMPP accounts.
*   Add and configure LLM profiles, associating them with your accounts.
*   Discover MUC services on an XMPP server.
*   Discover public rooms on a MUC service.
*   Interactive chat client for MUC rooms.

## Installation

1.  **Clone the repository:**
    ```bash
    git clone <repository_url>
    cd mcpcli
    ```

2.  **Install dependencies using Poetry:**
    Make sure you have [Poetry](https://python-poetry.org/) installed.
    ```bash
    poetry install
    ```

## Usage

The `mcpcli` tool is used from the command line within the project directory using `poetry run mcpcli`.

### 1. Configure an Account

First, you need to add an XMPP account.

```bash
poetry run mcpcli accounts add <account_name> --jid <your_jid@example.com> --password <your_password>
```
- `<account_name>` is a friendly name you'll use to refer to this account (e.g., `my_jabber`).
- `<your_jid@example.com>` is your full Jabber ID.
- `<your_password>` is your XMPP account password.

**Example:**
```bash
poetry run mcpcli accounts add my_jabber --jid user@jabber.org --password "secret_password"
```

You can list your configured accounts with:
```bash
poetry run mcpcli accounts list
```

### 2. Configure an LLM Profile

An "LLM profile" is a configuration that connects one of your accounts to a specific MUC room where an LLM is present.

```bash
poetry run mcpcli llms add <llm_name> --account <account_name> --room-jid <room@conference.example.com> --nickname <your_nickname>
```
- `<llm_name>` is a friendly name for this LLM profile (e.g., `gpt-bot`).
- `<account_name>` is the name of the account you configured in the previous step.
- `<room@conference.example.com>` is the JID of the MUC room.
- `<your_nickname>` is the nickname you want to use in that room.

**Example:**
```bash
poetry run mcpcli llms add gpt-bot --account my_jabber --room-jid gpt-room@conference.jabber.org --nickname MyChatNick
```

You can list your configured LLM profiles with:
```bash
poetry run mcpcli llms list
```

### 3. Chat with an LLM

Once you have a configured LLM profile, you can start a chat session:

```bash
poetry run mcpcli chat <llm_name>
```

**Example:**
```bash
poetry run mcpcli chat gpt-bot
```
This will open an interactive chat session. Type `/quit` to exit.

### 4. Discover Services and Rooms

If you don't know the JID of the MUC service or rooms, you can use the `discover` commands.

**Discover MUC services on a server:**
```bash
poetry run mcpcli discover services <server> --jid <your_jid@example.com> --password <your_password>
```
- `<server>` is the domain of the XMPP server (e.g., `jabber.org`).

**Example:**
```bash
poetry run mcpcli discover services jabber.org --jid user@jabber.org --password "secret_password"
```

**Discover public rooms on a MUC service:**
```bash
poetry run mcpcli discover rooms <service_jid> --jid <your_jid@example.com> --password <your_password>
```
- `<service_jid>` is the JID of the MUC service you discovered (e.g., `conference.jabber.org`).

**Example:**
```bash
poetry run mcpcli discover rooms conference.jabber.org --jid user@jabber.org --password "secret_password"
```
