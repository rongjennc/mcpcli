import slixmpp
import asyncio

class MUCClient(slixmpp.ClientXMPP):
    def __init__(self, jid, password, room, nick):
        super().__init__(jid, password)

        self.room = room
        self.nick = nick

        self.register_plugin('xep_0030') # Service Discovery
        self.register_plugin('xep_0045') # Multi-User Chat
        self.register_plugin('xep_0199') # XMPP Ping

        self.add_event_handler("session_start", self.start)
        self.add_event_handler("groupchat_message", self.muc_message)

    async def start(self, event):
        """
        Process the session_start event.

        This event is raised when the bot has successfully
        connected, authenticated, and is ready to send and
        receive stanzas.

        Arguments:
            event -- An empty dictionary. The session_start
                     event does not provide any data.
        """
        self.send_presence()
        self.get_roster()
        await self.plugin['xep_0045'].join_muc(self.room, self.nick)

    def muc_message(self, msg):
        """
        Process a groupchat message.

        Arguments:
            msg -- The received message stanza. See the documentation
                   for stanza objects and the Message stanza to see
                   how it may be used.
        """
        if msg['mucnick'] != self.nick and msg['body']:
            print(f"\r{msg['mucnick']}: {msg['body']}\n> ", end="")

    async def send_group_message(self, message):
        """
        Sends a message to the MUC room.
        """
        self.send_message(mto=self.room, mbody=message, mtype='groupchat')


class DiscoveryClient(slixmpp.ClientXMPP):
    def __init__(self, jid, password, server):
        super().__init__(jid, password)
        self.server = server
        self.add_event_handler("session_start", self.start)
        self.register_plugin('xep_0030') # Service Discovery

    async def start(self, event):
        """
        Process the session_start event.
        """
        print(f"Discovering services on {self.server}...")
        try:
            items = await self.plugin['xep_0030'].get_items(jid=self.server)
            print("Found services:")
            for item in items['disco_items']['items']:
                try:
                    info = await self.plugin['xep_0030'].get_info(jid=item['jid'])
                    is_muc = False
                    for feature in info['disco_info']['features']:
                        if feature == 'http://jabber.org/protocol/muc':
                            is_muc = True
                            break
                    if is_muc:
                        print(f"- {item['jid']} (MUC Service)")
                    else:
                        print(f"- {item['jid']}")
                except Exception as e:
                    # Can't query this item, so just print its JID
                    print(f"- {item['jid']} (Could not query further: {e})")

        except Exception as e:
            print(f"Could not discover services: {e}")
        finally:
            self.disconnect()


class RoomDiscoveryClient(slixmpp.ClientXMPP):
    def __init__(self, jid, password, service):
        super().__init__(jid, password)
        self.service = service
        self.add_event_handler("session_start", self.start)
        self.register_plugin('xep_0030') # Service Discovery

    async def start(self, event):
        """
        Process the session_start event.
        """
        print(f"Discovering rooms on {self.service}...")
        try:
            items = await self.plugin['xep_0030'].get_items(jid=self.service)
            print("Found rooms:")
            for item in items['disco_items']['items']:
                print(f"- {item['jid']} ({item['name']})")
        except Exception as e:
            print(f"Could not discover rooms: {e}")
        finally:
            self.disconnect()
