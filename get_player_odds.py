import argparse
import operator
from collections import OrderedDict
import time
import traceback
from base64 import b64decode
from copy import deepcopy
from selenium.common.exceptions import WebDriverException
from utils.config import Config
from utils.get_logger import Logger
from utils.utils import save_to_csv


class Dream11(object):
    def __init__(self):
        self.driver = None
        self.obj = Config()
        self.logger = Logger.get_console_logger()
        self.file_logger = Logger.get_file_logger()

    def get_data(self, driver_name='phantom', filename='players.properties', sortby=1):
        try:
            with open(filename, 'w') as f:
                f.truncate()
            players_bat = dict()
            players_wk = dict()
            players_bowl = dict()
            players_ar = dict()
            self.file_logger.info(
                "********************************************************************************")
            self.driver = self.obj.get_driver_instance(driver_name)
            self.logger.info("Initialized driver...")
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
            time.sleep(10)
            try:
                self.logger.info("Selecting match")
                self.obj.click_element(self.driver, self.obj.get_xpath("Match_selector"))
                time.sleep(3)
                self.logger.info("Clicking on Create Team")
                self.obj.click_element(self.driver, self.obj.get_xpath("Create_team_btn"))
                time.sleep(5)
                # Getting Bats info
                self.logger.info("Clicking on BAT tab")
                self.obj.click_element(self.driver, self.obj.get_xpath("Bat_tab_link"))
                self.logger.info("Getting Batsmen info...")
                total_bats = self.obj.wait_for_elements(self.driver, self.obj.get_xpath(
                    "Players_batsmens"))
                for each_ele in total_bats:
                    self.logger.info("Clicking on info")
                    time.sleep(3)
                    self.obj.wait_for_element_inside_webelement(each_ele, self.obj.get_xpath(
                        "Info_link")).click()
                    self.logger.info("Getting Info")
                    time.sleep(3)
                    player_name = self.obj.get_text_from_element(
                        self.obj.wait_for_element(self.driver, self.obj.get_xpath(
                            "Player_name_text")))
                    player_percentage = self.obj.get_text_from_element(
                        self.obj.wait_for_element(self.driver, self.obj.get_xpath(
                            "Player_percentage_text")))
                    players_bat[player_name] = float(player_percentage)
                    self.obj.click_element(self.driver, self.obj.get_xpath("Popup_close"))
                # Getting Bowls info
                self.logger.info("Clicking on BOWL tab")
                self.obj.click_element(self.driver, self.obj.get_xpath("Bowl_tab_link"))
                self.logger.info("Getting Bowlers info...")                
                total_bowls = self.obj.wait_for_elements(self.driver, self.obj.get_xpath(
                    "Players_bowlers"))
                for each_ele in total_bowls:
                    self.logger.info("Clicking on info")
                    time.sleep(3)
                    self.obj.wait_for_element_inside_webelement(each_ele, self.obj.get_xpath(
                        "Info_link")).click()
                    self.logger.info("Getting Info")
                    time.sleep(3)
                    player_name = self.obj.get_text_from_element(
                        self.obj.wait_for_element(self.driver, self.obj.get_xpath(
                            "Player_name_text")))
                    player_percentage = self.obj.get_text_from_element(
                        self.obj.wait_for_element(self.driver, self.obj.get_xpath(
                            "Player_percentage_text")))
                    players_bowl[player_name] = float(player_percentage)
                    self.obj.click_element(self.driver, self.obj.get_xpath("Popup_close"))
                # Getting Allrounders info
                self.logger.info("Clicking on AR tab")
                self.obj.click_element(self.driver, self.obj.get_xpath("Ar_tab_link"))
                self.logger.info("Getting AllRounders info...")                
                total_ars = self.obj.wait_for_elements(self.driver, self.obj.get_xpath(
                    "Players_allrounders"))
                for each_ele in total_ars:
                    self.logger.info("Clicking on info")
                    time.sleep(3)
                    self.obj.wait_for_element_inside_webelement(each_ele, self.obj.get_xpath(
                        "Info_link")).click()
                    self.logger.info("Getting Info")
                    time.sleep(3)
                    player_name = self.obj.get_text_from_element(
                        self.obj.wait_for_element(self.driver, self.obj.get_xpath(
                            "Player_name_text")))
                    player_percentage = self.obj.get_text_from_element(
                        self.obj.wait_for_element(self.driver, self.obj.get_xpath(
                            "Player_percentage_text")))
                    players_ar[player_name] = float(player_percentage)
                    self.obj.click_element(self.driver, self.obj.get_xpath("Popup_close"))
                # Getting Wicket-Keepers info
                self.logger.info("Clicking on WK tab")
                self.obj.click_element(self.driver, self.obj.get_xpath("Wk_tab_link"))
                self.logger.info("Getting Wicket-Keepers info...")                
                total_wks = self.obj.wait_for_elements(self.driver, self.obj.get_xpath(
                    "Players_wicketkeepers"))
                for each_ele in total_wks:
                    self.logger.info("Clicking on info")
                    time.sleep(3)
                    self.obj.wait_for_element_inside_webelement(each_ele, self.obj.get_xpath(
                        "Info_link")).click()
                    self.logger.info("Getting Info")
                    time.sleep(3)
                    player_name = self.obj.get_text_from_element(
                        self.obj.wait_for_element(self.driver, self.obj.get_xpath(
                            "Player_name_text")))
                    player_percentage = self.obj.get_text_from_element(
                        self.obj.wait_for_element(self.driver, self.obj.get_xpath(
                            "Player_percentage_text")))
                    players_wk[player_name] = float(player_percentage)
                    self.obj.click_element(self.driver, self.obj.get_xpath("Popup_close"))
            except Exception:
                self.logger.info("Exception Occurred... writing to the log file")
                self.file_logger.debug(traceback.format_exc())
            finally:
                # Logout
                self.driver.get(self.obj.get_xpath("Target_URL"))
                time.sleep(5)
                self.logger.info("Logging out...")
                self.obj.click_element(self.driver, self.obj.get_xpath("Team_dropdown"))
                self.obj.click_element(self.driver, self.obj.get_xpath("Logout_btn"))

        except WebDriverException:
            self.logger.info("Exception Occurred... writing to the log file")
            self.file_logger.debug(traceback.format_exc())
        finally:
            if self.driver:
                self.driver.quit()
            else:
                print("Driver not initialized")
        ordered_players = sort_by(filename, sortby)
        with open('players.txt', 'w') as f:
            for player in ordered_players.iteritems():
                f.write(str(player[0])+'\n')
                f.write(str(player[1])+'\n')
        return


class Dream11Exception(Exception):
    """
    Custom Exception Class    
    """

    def __init__(self, message):
        super(Exception, self).__init__(message)
        self.message = message

    def __str__(self):
        return self.message


def sort_by(filename, sortby):
    player_dict = dict()
    with open(filename) as f:
        players = f.readlines()
    for i,j in zip(range(0,len(players),2), range(1,len(players),2)):
        player_dict[players[i].strip('\n').strip()] = float(players[j].strip('\n').strip())
    if sortby == 1:
        sorted_players = sorted(player_dict.items(), key=operator.itemgetter(sortby), reverse=True)
    else:
        sorted_players = sorted(player_dict.items(), key=operator.itemgetter(sortby))
    ordered_players = OrderedDict(sorted_players)
    return ordered_players


def main(filename="players.properties", sortby=1, use_df=False):
    ordered_players = sort_by(filename, sortby)
    if use_df:
        import pandas as pd
        from tabulate import tabulate
        df = pd.DataFrame(ordered_players)
        tabular_df = tabulate(df, headers='keys', tablefmt='psql')
        print(tabular_df)
    return ordered_players


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="An utility that reads\
                                    the given file having two team players\
                                    separated by commas and generate required\
                                    number of pairs of cap and vice-cap")
    arg_group = parser.add_argument_group("Required Arguments")
    arg_group.add_argument("-s", "--sortby", required=False, help="An argument\
                            which tells to sort by player name or odds?")
    arg_group.add_argument("-d", "--usedf", required=False, help="This tells \
                           whether to use DataFrames or not")
    args = parser.parse_args()
    sortby = args.sortby if args.sortby else 1
    use_df = args.usedf if args.usedf else 0
    if args.usedf:
        try:
            use_df = int(use_df)
        except ValueError:
            raise ValueError("-d argument should be an integer")
    try:
        sortby = int(sortby)
    except ValueError:
        raise ValueError("-s argument should be an integer")
    obj = Dream11()
    obj.get_data()
    # main(filename, sortby, use_df)