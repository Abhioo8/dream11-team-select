import time
import traceback
from base64 import b64decode
from collections import OrderedDict

import operator
from selenium.common.exceptions import WebDriverException
from utils.config import Config
from utils.get_logger import Logger
import re


class Dream11(object):
    def __init__(self):
        self.driver = None
        self.obj = Config()
        self.logger = Logger.get_console_logger()
        self.file_logger = Logger.get_file_logger()
        self.espn_list = list()

    def get_data(self):
        try:
            result_dict = dict()
            self.logger.info("Initializing driver")
            self.driver = self.obj.get_driver_instance("phantom")
            self.logger.info("Initialized driver...")
            # Get team data from espn
            self.get_espn_data()
            self.logger.info("Navigating to dream11 homepage...")
            self.driver.get(self.obj.get_xpath("Target_URL"))
            self.logger.info("Entering username")
            self.obj.send_keys(self.driver, self.obj.get_xpath("Username_input"),
                               self.obj.get_xpath(
                                   "Username"))
            self.logger.info("Entering password")
            self.obj.send_keys(self.driver, self.obj.get_xpath("Password_input"), b64decode(
                self.obj.get_xpath("Password")))
            self.logger.info("Clicking on login")
            self.obj.click_element(self.driver, self.obj.get_xpath("Login_btn"))
            self.logger.info("Sleeping for 10 seconds")
            time.sleep(10)
            # Get total teams
            self.logger.info("Selecting match")
            self.obj.click_element(self.driver, self.obj.get_xpath("Match_selector"))
            time.sleep(5)
            self.logger.info("Getting total teams")
            total_teams = self.obj.wait_for_elements(self.driver, self.obj.get_xpath(
                "Total_teams"))
            for each_team in total_teams:
                self.logger.info("Clicking on teams")
                each_team.find_element_by_xpath('a').click()
                time.sleep(5)
                total_players = self.obj.wait_for_elements(self.driver, self.obj.get_xpath(
                    "Total_players"))
                for each_player in total_players:
                    player_name = each_player.get_attribute('title')
                    if player_name not in result_dict:
                        result_dict[player_name] = 1
                    else:
                        result_dict[player_name] += 1
            temp = sorted(result_dict.items(), key=operator.itemgetter(1))
            temp.reverse()
            temp = OrderedDict(temp)
            for key, value in enumerate(temp.iteritems()):
                print("{0} : {1} - {2}".format(key+1, value[0], value[1]))
            # import ipdb;ipdb.set_trace()
            diff = set(self.espn_list) - set(result_dict.keys())
            print(diff)

        except WebDriverException:
            self.logger.info("Exception Occurred... writing to the log file")
            self.file_logger.debug(traceback.format_exc())
        finally:
            if self.driver:
                self.driver.quit()
            else:
                print("Driver not initialized")

    def get_espn_data(self):
        try:
            self.logger.info("Opening espn news page...")
            self.driver.get('http://www.espncricinfo.com/indian-premier-league-2017/content/story/1092006.html')
            team1 = self.obj.get_text_from_element(self.obj.wait_for_element(self.driver,
                                                                                  self.obj.get_xpath("Team1")))
            team2 = self.obj.get_text_from_element(self.obj.wait_for_element(self.driver,
                                                                                  self.obj.get_xpath(
                                                                                      "Team2")))
            # import ipdb;ipdb.set_trace()
            self.logger.info("Getting team names...")
            team_name1 = self.obj.get_text_from_element(self.obj.wait_for_element(self.driver,
                                                                                  self.obj.get_xpath("Team1")+"/b"))
            team_name2 = self.obj.get_text_from_element(self.obj.wait_for_element(self.driver,
                                                                                  self.obj.get_xpath(
                                                                                      "Team2") + "/b"))
            self.logger.info("Formatting the text...")
            team1 = "".join("".join(team1.split(team_name1)).strip(":").strip().split(', '))
            pt = re.compile('[\d+]')
            res = re.sub(pt, ',', team1)
            res = res.replace(',,', ',')
            self.logger.info("Adding team1 players to espn_list")
            for ele in res.split(', '):
                if ele:
                    self.espn_list.append(ele)
            self.logger.info("Team1 Players are %s" % self.espn_list)
            self.logger.info("Formatting the text...")
            team2 = "".join("".join(team2.split(team_name2)).strip(":").strip().split(', '))
            res = re.sub(pt, ',', team2)
            res = res.replace(',,', ',')
            self.logger.info("Adding team2 players to espn_list")
            team2_players = []
            for ele in res.split(', '):
                if ele:
                    self.espn_list.append(ele)
                    team2_players.append(ele)
            self.logger.info("Team2 Players are %s" % team2_players)

        except WebDriverException:
            self.logger.info("Exception Occurred... writing to the log file")
            self.file_logger.debug(traceback.format_exc())


class Dream11Exception(Exception):
    """
    Custom Exception Class    
    """

    def __init__(self, message):
        super(Exception, self).__init__(message)
        self.message = message

    def __str__(self):
        return self.message


if __name__ == "__main__":
    obj = Dream11()
    obj.get_data()
