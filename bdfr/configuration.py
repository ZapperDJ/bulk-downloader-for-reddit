#!/usr/bin/env python3
# coding=utf-8

from argparse import Namespace
from typing import Optional
import logging

import click
import yaml

logger = logging.getLogger(__name__)

class Configuration(Namespace):
    def __init__(self):
        super(Configuration, self).__init__()
        self.authenticate = False
        self.config = None
        self.opts: Optional[str] = None
        self.directory: str = '.'
        self.disable_module: list[str] = []
        self.exclude_id = []
        self.exclude_id_file = []
        self.file_scheme: str = '{REDDITOR}_{TITLE}_{POSTID}'
        self.folder_scheme: str = '{SUBREDDIT}'
        self.ignore_user = []
        self.include_id_file = []
        self.limit: Optional[int] = None
        self.link: list[str] = []
        self.log: Optional[str] = None
        self.make_hard_links = False
        self.max_wait_time = None
        self.multireddit: list[str] = []
        self.no_dupes: bool = False
        self.saved: bool = False
        self.search: Optional[str] = None
        self.search_existing: bool = False
        self.skip: list[str] = []
        self.skip_domain: list[str] = []
        self.skip_subreddit: list[str] = []
        self.sort: str = 'hot'
        self.submitted: bool = False
        self.subscribed: bool = False
        self.subreddit: list[str] = []
        self.time: str = 'all'
        self.time_format = None
        self.upvoted: bool = False
        self.user: list[str] = []
        self.verbose: int = 0

        # Archiver-specific options
        self.all_comments = False
        self.format = 'json'
        self.comment_context: bool = False

    def process_click_arguments(self, context: click.Context):
        if context.params['opts'] is not None:
            with open(context.params['opts']) as f:
                opts = yaml.load(f, Loader=yaml.FullLoader)
            for arg_key, val in opts.items():
                if not hasattr(self, arg_key):
                    logger.error(f'Ignoring an unknown YAML argument: {arg_key}')
                    continue
                setattr(self, arg_key, val)
        for arg_key in context.params.keys():
            if not hasattr(self, arg_key):
                logger.warning(f'Ignoring an unknown CLI argument: {arg_key}')
                continue
            val = context.params[arg_key]
            if val is None or val == ():
                # don't overwrite with an empty value
                continue
            setattr(self, arg_key, val)
