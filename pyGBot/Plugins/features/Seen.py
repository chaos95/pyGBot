##
##    pyGBot - Versatile IRC Bot
##    Copyright (C) 2008 Morgan Lokhorst-Blight, Alex Soborov
##
##    This program is free software: you can redistribute it and/or modify
##    it under the terms of the GNU General Public License as published by
##    the Free Software Foundation, either version 3 of the License, or
##    (at your option) any later version.
##
##    This program is distributed in the hope that it will be useful,
##    but WITHOUT ANY WARRANTY; without even the implied warranty of
##    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
##    GNU General Public License for more details.
##
##    You should have received a copy of the GNU General Public License
##    along with this program.  If not, see <http://www.gnu.org/licenses/>.
##

from datetime import datetime

from elixir import *

metadata.bind = "sqlite:///seen.sqlite"

SeenEventTypes = dict(map(reversed, enumerate("Join Part Quit Kick Nick Say Do".split())))


class SeenEvent(Entity):
    user = Field(Unicode(30), primary_key=True)
    channel = Field(Unicode(100), primary_key=True)
    type = Field(Unicode(8))
    message = Field(UnicodeText)
    timestamp = Field(DateTime, primary_key=True)

    def __repr__(self):
        return ('<SeenEvent %s %s %s>' % (self.user, self.channel, self.timestamp)).encode('ascii', 'replace')

setup_all()
create_all()


def get_latest(username, channel=None):
    if channel is None:
        try:
            return SeenEvent.query.filter_by(user=unicode(username)).order_by("timestamp DESC")[0]
        except IndexError:
            raise IndexError("I'm sorry, I haven't seen that user.")
    else:
        try:
            return SeenEvent.query.filter_by(user=unicode(username), channel=unicode(channel)).order_by("timestamp DESC")[0]
        except IndexError:
            raise IndexError("I'm sorry, I haven't seen that user on that channel.")



###############################################################################
##
## Command
##
###############################################################################
from pyGBot.auth import AuthLevels
from pyGBot.commands import bot_command


@bot_command(AuthLevels.User)
def SeenCommand(bot, channel, user, args):
    args = args.strip().split()
    if not args:
        bot.replyout(channel, user, 'Command usage: seen <user> [channel]')
        return

    searchNick = args[0]
    try:
        searchChannel = args[1]
    except IndexError:
        searchChannel = None

    try:
        event = get_latest(searchNick, searchChannel)
    except IndexError, e:
        bot.replyout(channel, user, str(e))
        return

    outmessage = "The user, %s, was last seen " % event.user
    if event.channel:
        outmessage += "on channel %s " % event.channel
    else:
        outmessage += "on this network "

    lastseen = datetime.now() - event.timestamp

    days = lastseen.days
    hours = lastseen.seconds / 3600
    minutes = (lastseen.seconds % 3600) / 60
    seconds = lastseen.seconds % 60

    timemessage = []
    if days != 0:
        timemessage.append("%i days" % days)
    if hours != 0:
        timemessage.append("%i hours" % hours)
    if minutes != 0:
        timemessage.append("%i minutes" % minutes)
    if seconds != 0:
        timemessage.append("%i seconds" % seconds)

    if len(outmessage) > 0:
        outmessage += ", ".join(timemessage) + " ago, "
    else:
        outmessage += "just now, "

    if event.type == "Say":
        outmessage += "saying: <%s> %s" % (event.user, event.message)
    elif event.type == "Do":
        outmessage += "performing the action: * %s %s" % (event.user, event.message)
    elif event.type == "Msg":
        outmessage += "sending me a private message."
    elif event.type == "Part":
        outmessage += "parting the channel."
    elif event.type == "Join":
        outmessage += "joining the channel."
    elif event.type == "Quit":
        outmessage += "quitting with the message: %s" % event.message
    elif event.type == "Kick":
        outmessage += "getting kicked %s" % event.message
    elif event.type == "NickTo":
        outmessage += "changing nick to %s." % event.message
    elif event.type == "NickFrom":
        outmessage += "changing nick from %s." % event.message
    bot.replyout(channel, user, outmessage)


###############################################################################
##
## Plugin
##
###############################################################################
from pyGBot.BasePlugin import BasePlugin


class Seen(BasePlugin):
    def __init__(self, bot, options):
        self.bot = bot
        self.active = False

    def activate(self, channel=None):
        """
        Called when the plugin is activated.
        """
        self.active = True
        return True

    def deactivate(self, channel=None):
        """
        Called when the plugin is deactivated.
        """
        self.active = False
        return True

    # Event handlers for other users
    def user_join(self, channel, username):
        if self.active:
            SeenEvent(user=unicode(username), channel=unicode(channel), type=u'Join', timestamp=datetime.now())
            session.commit()

    def user_part(self, channel, username):
        if self.active:
            SeenEvent(user=unicode(username), channel=unicode(channel), type=u'Part', timestamp=datetime.now())
            session.commit()

    def user_kicked(self, channel, username, kicker, message=""):
        if self.active:
            SeenEvent(user=unicode(username), channel=unicode(channel), type=u'Kick', timestamp=datetime.now(), message=unicode(message))
            session.commit()

    def user_quit(self, username, reason=""):
        if self.active:
            SeenEvent(user=unicode(username), channel=u'', type=u'Quit', timestamp=datetime.now(), message=unicode(reason))
            session.commit()

    def user_nickchange(self, username, newname):
        if self.active:
            SeenEvent(user=unicode(username), channel=u'', type=u'NickFrom', timestamp=datetime.now(), message=u'%s -> %s' % (username, newname))
            SeenEvent(user=unicode(newname), channel=u'', type=u'NickTo', timestamp=datetime.now(), message=u'%s -> %s' % (username, newname))
            session.commit()

    # Event handlers for this bot
    def bot_connect(self):
        pass

    def bot_join(self, channel):
        pass

    def bot_part(self, channel):
        pass

    def bot_kicked(self, channel, kicker="", reason=""):
        pass

    def bot_disconnect(self):
        pass

    # Event handlers for incoming messages
    def msg_channel(self, channel, user, message):
        if self.active:
            SeenEvent(user=unicode(user), channel=unicode(channel), type=u'Say', timestamp=datetime.now(), message=unicode(message))
            session.commit()

    def msg_action(self, channel, user, message):
        if self.active:
            SeenEvent(user=unicode(user), channel=unicode(channel), type=u'Do', timestamp=datetime.now(), message=unicode(message))
            session.commit()

    def msg_private(self, user, message):
        pass

    def msg_notice(self, user, message):
        pass

    def channel_names(self, channel, nameslist):
        pass

    def timer_tick(self):
        pass
