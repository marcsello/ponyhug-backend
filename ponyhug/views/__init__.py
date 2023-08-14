#!/usr/bin/env python3
from .api import api

# objects have to be imported, so they are processed and restix will "know" about them
from .timeframes_view import CurrentTimeframeResource, TimeframesResource, TimeframeResource
from .stats_view import LeaderResource, FactionsResource
from .ponies_view import PoniesResource, PonyCountResource, PonyResource
from .players_view import PlayersResource, PlayerResource, PlayerMeResource
from .hugs_view import HugsResource, HugsCountResource, HugResource