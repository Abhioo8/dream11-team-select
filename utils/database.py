#!/usr/bin/env python
# coding=utf-8
import MySQLdb
import traceback
from utils.get_logger import Logger


class Database:
    def __init__(self):
        self.conn = MySQLdb.connect(host='localhost', user='root', passwd='password', db='mine')
        self.cursor = self.conn.cursor()
        self.logger = Logger.get_console_logger()
        self.file_logger = Logger.get_file_logger()

    def insert_teams_into_db(self, link, team1, team2):
        try:
            self.cursor.execute('insert into dream11 (`link`, `team1`, `team2`) values (%s, %s, %s)', (link, str(team1), str(team2)))
        except MySQLdb.Error, e:
            self.logger.info("Exception Occurred while inserting into database... writing to the log file")
            self.file_logger.debug(traceback.format_exc())

    def get_teams_from_db(self, link):
        try:
            self.cursor.execute('select `team1`, `team2` from dream11 where `link` = (%s)', (link,))
            res = self.cursor.fetchall()
            return res
        except MySQLdb.Error, e:
            self.logger.info("Exception Occurred while getting data from database... writing to the log file")
            self.file_logger.debug(traceback.format_exc())

    def __del__(self):
        try:
            if self.conn:
                self.conn.close()
        except MySQLdb.Error, e:
            self.logger.info("Exception Occurred... writing to the log file")
            self.file_logger.debug(traceback.format_exc())
