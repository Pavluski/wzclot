import discord
from wlct.models import Clan, Player, DiscordUser, DiscordChannelTournamentLink
from wlct.tournaments import Tournament, TournamentTeam, TournamentGame, TournamentPlayer, MonthlyTemplateRotation, get_games_finished_for_team_since, find_tournament_by_id, get_team_data_no_clan, RealTimeLadder, get_real_time_ladder, TournamentGame, ClanLeagueTournament
from discord.ext import commands, tasks
from wlct.cogs.common import is_admin
from django.utils import timezone
from traceback import print_exc
from wlct.logging import log_exception, log, LogLevel, Logger, log_bot_msg
import gc
import datetime
import pytz

class Tasks(commands.Cog, name="tasks"):
    def __init__(self, bot):
        self.bot = bot
        self.last_task_run = timezone.now()
        self.executions = 0
        self.bg_task.start()

    async def handle_rtl_tasks(self):
        ladders = RealTimeLadder.objects.all()
        for ladder in ladders:
            print("Handling rtl tasks....")
            games = TournamentGame.objects.filter(tournament=ladder, is_finished=False, mentioned=False)
            print("Total game count: {}".format(games.count()))
            # cache the game data + link for use with the embed
            emb = discord.Embed(color=self.bot.embed_color)
            emb.set_author(icon_url=self.bot.user.avatar_url, name="WarzoneBot")
            emb.title = "New Ladder Game Created"
            emb.set_footer(text="Bot created and maintained by -B#0292")
            for game in games:
                print("RTL: Found game")
                data = ""
                team1 = game.teams.split('.')[0]
                team2 = game.teams.split('.')[1]
                player1 = ladder.get_player_from_teamid(team1)
                player2 = ladder.get_player_from_teamid(team2)
                data += "<@{}> vs. <@{}> [Game Link]({})\n".format(player1.discord_member.memberid, player2.discord_member.memberid,
                                                                   game.game_link)
                emb.add_field(name="Game", value=data, inline=True)
                if player1:
                    user = self.bot.get_user(player1.discord_member.memberid)
                    if user:
                        await user.send(embed=emb)
                if player2:
                    user = self.bot.get_user(player2.discord_member.memberid)
                    if user:
                        await user.send(embed=emb)
                        game.mentioned = True
                        game.save()

    async def handle_clan_league_next_game(self):
        clt = ClanLeagueTournament.objects.filter(is_finished=False)
        for t in clt:
            # get the time until next game allocation
            start_times = t.games_start_times.split(';')

            # always take the next (first) one
            if len(start_times[0]) >= 8:  # every start time is a day/month/year, and we need at least 8 characters
                next_start = datetime.datetime.strptime(start_times[0], "%m.%d.%y")
                diff = datetime.datetime.utcnow() - next_start
                # diff is our delta, compute how many days, hours, minutes remaining

    async def handle_game_logs(self):
        channel_links = DiscordChannelTournamentLink.objects.all()
        games_sent = []
        try:
            for cl in channel_links:
                channel = self.bot.get_channel(cl.channelid)
                # for each channel, see if there are any new games that have finished in the tournament that's linked
                # only look at games that have finished times greater than when the bot started
                game_log_text = ""
                if hasattr(self.bot, 'uptime'):
                    games = TournamentGame.objects.filter(is_finished=True, tournament=cl.tournament, game_finished_time__gt=(self.bot.uptime-datetime.timedelta(days=3)), game_log_sent=False)
                    for game in games:
                        if game.game_finished_time is None and game.winning_team or not game.winning_team:
                            continue  # ignore games with no finished time (which might be 0 and returned in this query)
                        # we have the game, construct the log text and send it to the channel

                        # bold the clans if any, and italicize
                        teams = game.teams.split('.')
                        team_list = []
                        team_list.append(game.winning_team.id)
                        for team in teams:
                            if int(team) not in team_list:
                                team_list.append(int(team))

                        player_team_id_list = None
                        if game.players:
                            player_team_id_list = game.players.split("-")

                        wrote_defeats = False
                        for team in team_list:
                            tt = TournamentTeam.objects.filter(pk=team)
                            if tt:
                                tt = tt[0]
                                # look up the clan for this team, and bold/write the clan name in there.
                                if tt.clan_league_clan and tt.clan_league_clan.clan:
                                    game_log_text += "**{}** ".format(tt.clan_league_clan.clan.name)

                                # if game has 'players' value, use that otherwise get names from TournamentPlayer
                                if player_team_id_list:
                                    tplayers = player_team_id_list[teams.index(str(team))].split(".")
                                else:
                                    tplayers = TournamentPlayer.objects.filter(team=tt)

                                for tplayer in tplayers:
                                    if player_team_id_list:
                                        player_name = Player.objects.filter(token=tplayer)
                                        player_name = player_name[0].name
                                    else:
                                        player_name = tplayer.player.name
                                    game_log_text += "*{}* ,".format(player_name)

                                game_log_text = game_log_text[:-1]
                                if not wrote_defeats:
                                    game_log_text += " defeats "
                                    wrote_defeats = True

                        tournament = find_tournament_by_id(game.tournament.id, True)
                        if tournament and hasattr(tournament, 'clan_league_template') and tournament.clan_league_template:
                            game_log_text += "\n{}".format(tournament.clan_league_template.name)

                        game_log_text += "\n<{}>".format(game.game_link)

                        log_bot_msg("Looping through channels to log: {}".format(game_log_text))
                        if channel and len(game_log_text) > 0:
                            log_bot_msg("Sending game_log to channel: {}".format(channel.name))
                            await channel.send(game_log_text)
                            games_sent.append(game)
                            game_log_text = ""
        except Exception:
            log_exception()
        finally:
            for g in games_sent:
                g.game_log_sent = True
                g.save()

    async def handle_hours6_tasks(self):
        #await self.handle_clan_league_next_game()
        pass

    async def handle_hours4_tasks(self):
        # every 4 hours we currently only send clan league updates
        pass

    async def handle_hours_tasks(self):
        pass

    async def handle_day_tasks(self):
        pass

    async def handle_no_winning_team_games(self):
        games = TournamentGame.objects.filter(winning_team__isnull=True, is_finished=True, no_winning_team_log_sent=False)
        msg = ""
        if games:
            msg += "**Games finished with no winning team found**"
        for game in games:
            for cc in self.bot.critical_error_channels:
                msg += "\n{} | ID: {} \nLink: <{}> \nLogs: <http://wztourney.herokuapp.com/admin/wlct/processgamelog/?q={}>".format(game.tournament.name, game.gameid, game.game_link, game.gameid)
                msg = msg[:1999]
                await cc.send(msg)
                game.no_winning_team_log_sent = True
                game.save()
                msg = ""

    async def handle_rtl_ladder(self):
        tournaments = Tournament.objects.filter(has_started=True, is_finished=False)
        for tournament in tournaments:
            child_tournament = find_tournament_by_id(tournament.id, True)
            if child_tournament and not child_tournament.should_process_in_engine():
                try:
                    if child_tournament.update_in_progress:
                        continue
                    elif not child_tournament.game_creation_allowed:
                        continue
                    child_tournament.update_in_progress = True
                    child_tournament.save()
                    games = TournamentGame.objects.filter(is_finished=False, tournament=tournament)
                    for game in games.iterator():
                        # process the game
                        # query the game status
                        child_tournament.process_game(game)
                    # in case tournaments get stalled for some reason
                    # for it to process new games based on current tournament data
                    child_tournament.process_new_games()

                    # after we process games we always cache the latest data for quick reads
                    child_tournament.cache_data()
                except Exception as e:
                    log_exception()
                finally:
                    child_tournament.update_in_progress = False
                    child_tournament.save()
            gc.collect()

    async def handle_critical_errors(self):
        logs = Logger.objects.filter(level=LogLevel.critical, bot_seen=False)
        if logs:
            for log in logs:
                for cc in self.bot.critical_error_channels:
                    msg = "**Critical Log Found**\n"
                    msg += log.msg
                    msg = msg[:1999]
                    await cc.send(msg)
                    log.bot_seen = True
                    log.save()

    async def handle_all_tasks(self):
        # calculate the time different here
        # determine if we need hours run or 4 hours run
        # for 1 hour, executions should be 360
        hours = (self.executions % 360 == 0)
        hours4 = (self.executions % (360*4) == 0)
        hours6 = (self.executions % (360*6) == 0)
        day = (self.executions % (360*24) == 0)
        two_minute = (self.executions % 12 == 0)

        try:
            if hours:
                await self.handle_hours_tasks()
            if hours4:
                await self.handle_hours4_tasks()
            if hours6:
                await self.handle_hours6_tasks()
            if day:
                await self.handle_day_tasks()
            if two_minute:
                await self.handle_rtl_ladder()

            # always tasks
            await self.handle_always_tasks()
        except Exception:
            log_exception()

    async def handle_always_tasks(self):
        await self.handle_rtl_tasks()
        await self.handle_critical_errors()
        await self.handle_game_logs()
        #await self.handle_no_winning_team_games()

    async def process_member_join(self, memid):
        member = self.bot.get_user(memid)
        if member:
            send_message = False
            discord_user = DiscordUser.objects.filter(memberid=memid)
            emb = discord.Embed(color=self.bot.embed_color)
            emb.set_author(icon_url=self.bot.user.avatar_url, name="WarzoneBot")
            emb.title = "It's nice to meet you!"
            emb.set_footer(text="Bot created and maintained by -B#0292")
            msg = "Hello {},\n\nI'm a homemade Warzone Discord Bot. \n\nI'm reaching out because your discord account".format(
                member.name)
            msg += " is not linked to the CLOT (custom ladder or tournament). Please see http://wztourney.herokuapp.com/me/ for instructions"
            msg += " on how to link the two accounts together.\n\nThis will allow you to participate in the bot's"
            msg += " new real-time-ladder, as well as help to become verified in the Warzone discord server."
            emb.add_field(name="Welcome", value=msg)

            if not discord_user:
                discord_user = DiscordUser(memberid=memid)
                discord_user.save()
            else:
                discord_user = discord_user[0]

            if not discord_user.link_mention:
                print("Sending welcome message to {}".format(member.name))
                await member.send(embed=emb)
                discord_user.link_mention = True
                discord_user.save()

    @tasks.loop(seconds=10.0)
    async def bg_task(self):
        # runs every 10 seconds to check various things
        # are there any new games on the RTL that just got allocated?
        try:
            await self.bot.wait_until_ready()
            owner = self.bot.owner
            await self.handle_all_tasks()
            self.last_task_run = timezone.now()
            self.executions += 1
        except:
            print_exc()
            raise

def setup(bot):
    bot.add_cog(Tasks(bot))