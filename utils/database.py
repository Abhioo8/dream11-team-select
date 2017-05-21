#!/usr/bin/env python
# coding=utf-8
import traceback
import MySQLdb
from get_logger import Logger


class Database:
    def __init__(self):
        self.conn = MySQLdb.connect(host='localhost', user='root', passwd='password', db='mine')
        self.conn.autocommit = True
        self.cursor = self.conn.cursor()

    def insert_teams_into_db(self, link, team1, team2):
        """
        This function inserts the given link, team1, teams into table
        `mine`
        :param link: str: espn_cricinfo link
        :param team1: list: team1 players
        :param team2: list: team2 players
        :return: None
        """
        try:
            import json
            self.cursor.execute('insert into dream11 (`link`, `team1`, `team2`) values (%s, %s, %s);', (link, json.dumps(team1), json.dumps(team2),))
            self.conn.commit()
        except MySQLdb.Error:
            self.conn.rollback()
            logger = Logger.get_console_logger()
            file_logger = Logger.get_file_logger()
            logger.info("Exception Occurred while inserting into database... writing to the log file")
            file_logger.debug(traceback.format_exc())

    def get_teams_from_db(self, link):
        """

        :param link: str: link to retrieve team players
        :return: tuple
        """
        try:
            self.cursor.execute('select `team1`, `team2` from dream11 where `link` = (%s);', (link,))
            res = self.cursor.fetchall()
            return res
        except MySQLdb.Error:
            logger = Logger.get_console_logger()
            file_logger = Logger.get_file_logger()
            logger.info("Exception Occurred while inserting into database... writing to the log file")
            file_logger.debug(traceback.format_exc())

    def __del__(self):
        try:
            if self.cursor:
                self.cursor.close()
            if self.conn:
                self.conn.close()
        except MySQLdb.Error:
            logger = Logger.get_console_logger()
            file_logger = Logger.get_file_logger()
            logger.info("Exception Occurred while inserting into database... writing to the log file")
            file_logger.debug(traceback.format_exc())
