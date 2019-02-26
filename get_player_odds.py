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
from utils.config import ConfigParser

config = ConfigParser()
config.optionxform = str


class Dream11(object):
    def __init__(self):
        self.driver = None
        self.obj = Config()
        self.logger = Logger.get_console_logger()
        self.file_logger = Logger.get_file_logger()

    def get_data(self, driver_name='phantom', filename='players.txt', sortby=1):
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
            if driver_name == 'chrome':
                try:
                    time.sleep(5)
                    self.driver.switch_to_window(self.driver.window_handles[1])
                    if self.driver.current_url == \
                        'chrome-extension://cfhdojbkjhnklbpkdaibdccddilifddb/firstRun.html':
                        # Closing Adblock tab
                        self.driver.execute_script('window.close();')
                        self.driver.switch_to_window(self.driver.window_handles[0])
                except IndexError:
                    pass
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
                    player_name = self.obj.get_text_from_element(
                        self.obj.wait_for_element_inside_webelement(each_ele, self.obj.get_xpath(
                        "Player_name_text")))
                    self.logger.info("Clicking on info")
                    time.sleep(3)
                    self.obj.wait_for_element_inside_webelement(each_ele, self.obj.get_xpath(
                        "Info_link")).click()
                    self.logger.info("Getting Info")
                    time.sleep(3)
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
                    player_name = self.obj.get_text_from_element(
                        self.obj.wait_for_element_inside_webelement(each_ele, self.obj.get_xpath(
                        "Player_name_text")))
                    self.logger.info("Clicking on info")
                    time.sleep(3)
                    self.obj.wait_for_element_inside_webelement(each_ele, self.obj.get_xpath(
                        "Info_link")).click()
                    self.logger.info("Getting Info")
                    time.sleep(3)
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
                    player_name = self.obj.get_text_from_element(
                        self.obj.wait_for_element_inside_webelement(each_ele, self.obj.get_xpath(
                        "Player_name_text")))
                    self.logger.info("Clicking on info")
                    time.sleep(3)
                    self.obj.wait_for_element_inside_webelement(each_ele, self.obj.get_xpath(
                        "Info_link")).click()
                    self.logger.info("Getting Info")
                    time.sleep(3)
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
                    player_name = self.obj.get_text_from_element(
                        self.obj.wait_for_element_inside_webelement(each_ele, self.obj.get_xpath(
                        "Player_name_text")))
                    self.logger.info("Clicking on info")
                    time.sleep(3)
                    self.obj.wait_for_element_inside_webelement(each_ele, self.obj.get_xpath(
                        "Info_link")).click()
                    self.logger.info("Getting Info")
                    time.sleep(3)
                    player_percentage = self.obj.get_text_from_element(
                        self.obj.wait_for_element(self.driver, self.obj.get_xpath(
                            "Player_percentage_text")))
                    players_wk[player_name] = float(player_percentage)
                    self.obj.click_element(self.driver, self.obj.get_xpath("Popup_close"))
                sorted_bat = sorted(players_bat.items(), key=operator.itemgetter(1), reverse=True)
                self.write_to_players('BAT', OrderedDict(sorted_bat))
                sorted_wk = sorted(players_wk.items(), key=operator.itemgetter(1), reverse=True)
                self.write_to_players('WK', OrderedDict(sorted_wk))
                sorted_bowl = sorted(players_bowl.items(), key=operator.itemgetter(1), reverse=True)
                self.write_to_players('BOWL', OrderedDict(sorted_bowl))
                sorted_ar = sorted(players_ar.items(), key=operator.itemgetter(1), reverse=True)
                self.write_to_players('AR', OrderedDict(sorted_ar))

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

    @staticmethod
    def write_to_players(section_name, data):
        """
        This function takes section_name and data and
        write to the players.txt file.
        @param: section_name: str: section name to be written
        @param: data: OrderedDict: players data to be written
        """
        fp = open('players.txt', 'a')
        config.add_section(section_name)
        for key,value in data.iteritems():
            config.set(section_name, key, str(value))
        config.write(fp)
        fp.close()


class Dream11Exception(Exception):
    """
    Custom Exception Class    
    """

    def __init__(self, message):
        super(Exception, self).__init__(message)
        self.message = message

    def __str__(self):
        return self.message


def construct_orderd_dict_from_players(section_name):
    res = list()
    config.read('players.txt')
    options = config.options(section_name)
    for option in options:
        res.append((option, config.get(section_name, option)))
    return OrderedDict(res)


def read_from_players():
    player_dict = dict()
    player_dict['BAT'] = construct_orderd_dict_from_players('BAT')
    player_dict['WK'] = construct_orderd_dict_from_players('WK')
    player_dict['BOWL'] = construct_orderd_dict_from_players('BOWL')
    player_dict['AR'] = construct_orderd_dict_from_players('AR')
    return player_dict


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