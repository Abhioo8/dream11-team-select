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

    def get_data(self):
        try:
            total_data = list()
            headers = ['Player Name', 'Role', 'Price', 'Match Date', 'Total Points',
                       'Selected Percentage']
            self.driver = self.obj.get_driver_instance()
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
            # Get teams
            self.logger.info("Getting team names")
            teams = self.obj.wait_for_elements(self.driver, self.obj.get_xpath("Team_names"))
            try:
                file_name = self.obj.get_text_from_element(teams[0]) + 'vs' + \
                            self.obj.get_text_from_element(teams[1])
                self.logger.info("Got file name as %s " % file_name)
            except IndexError:
                raise Dream11Exception("Unable to get team names for file name")
            time.sleep(10)
            self.logger.info("Clicking on Create Team")
            self.obj.click_element(self.driver, self.obj.get_xpath("Create_team_btn"))
            time.sleep(10)
            self.logger.info("Clicking on WK tab")
            self.obj.click_element(self.driver, self.obj.get_xpath("Wk_tab_link"))
            total_elements = self.obj.wait_for_elements(self.driver, self.obj.get_xpath(
                "Total_wk"))
            for each_ele in total_elements:
                self.logger.info("Clicking on info")
                time.sleep(5)
                self.obj.wait_for_element_inside_webelement(each_ele, self.obj.get_xpath(
                    "Info_link")).click()
                self.logger.info("Getting Info of WKs")
                player_name = self.obj.get_text_from_element(
                    self.obj.wait_for_element(self.driver, self.obj.get_xpath(
                        "Player_name_text")))
                self.logger.info("Got player name %s " % player_name)
                player_price = self.obj.get_text_from_element(
                    self.obj.wait_for_element(self.driver, self.obj.get_xpath(
                        "Player_price_text")))
                player_dict = {
                    'Player Name': player_name,
                    'Price': player_price,
                    'Role': 'WK'
                }
                total_matches = self.obj.wait_for_elements(self.driver, self.obj.get_xpath(
                    "Total_matches"))
                self.logger.info("Getting info of total matches")
                for each_match in total_matches:
                    match_date = self.obj.get_text_from_element(
                        self.obj.wait_for_element_inside_webelement(each_match,
                                                                    self.obj.get_xpath(
                                                                        "Match_date_text")))
                    total_points = self.obj.get_text_from_element(
                        self.obj.wait_for_element_inside_webelement(each_match,
                                                                    self.obj.get_xpath(
                                                                        "Total_points_text")))
                    selected_percentage = self.obj.get_text_from_element(
                        self.obj.wait_for_element_inside_webelement(each_match,
                                                                    self.obj.get_xpath(
                                                                        "Selected_percentage_text")))
                    player_dict = deepcopy(player_dict)
                    player_dict['Match Date'] = match_date
                    player_dict['Total Points'] = total_points
                    player_dict['Selected Percentage'] = selected_percentage
                    total_data.append(player_dict)

                self.logger.info("Closing Player Info...")
                self.obj.click_element(self.driver, self.obj.get_xpath("Popup_close"))

            self.logger.info("Clicking on BAT tab")
            time.sleep(5)
            self.obj.click_element(self.driver, self.obj.get_xpath("Bat_tab_link"))
            total_elements = self.obj.wait_for_elements(self.driver, self.obj.get_xpath(
                "Total_bat"))

            for each_ele in total_elements:
                self.logger.info("Clicking on info")
                time.sleep(5)
                self.obj.wait_for_element_inside_webelement(each_ele, self.obj.get_xpath(
                    "Info_link")).click()
                self.logger.info("Getting Info of BATs")
                player_name = self.obj.get_text_from_element(
                    self.obj.wait_for_element(self.driver, self.obj.get_xpath(
                        "Player_name_text")))
                self.logger.info("Got player name %s " % player_name)
                player_price = self.obj.get_text_from_element(
                    self.obj.wait_for_element(self.driver, self.obj.get_xpath(
                        "Player_price_text")))
                player_dict = {
                    'Player Name': player_name,
                    'Price': player_price,
                    'Role': 'BAT'
                }
                total_matches = self.obj.wait_for_elements(self.driver, self.obj.get_xpath(
                    "Total_matches"))
                self.logger.info("Getting info of total matches")
                for each_match in total_matches:
                    match_date = self.obj.get_text_from_element(
                        self.obj.wait_for_element_inside_webelement(each_match,
                                                                    self.obj.get_xpath(
                                                                        "Match_date_text")))
                    total_points = self.obj.get_text_from_element(
                        self.obj.wait_for_element_inside_webelement(each_match,
                                                                    self.obj.get_xpath(
                                                                        "Total_points_text")))
                    selected_percentage = self.obj.get_text_from_element(
                        self.obj.wait_for_element_inside_webelement(each_match,
                                                                    self.obj.get_xpath(
                                                                        "Selected_percentage_text")))
                    player_dict = deepcopy(player_dict)
                    player_dict['Match Date'] = match_date
                    player_dict['Total Points'] = total_points
                    player_dict['Selected Percentage'] = selected_percentage
                    total_data.append(player_dict)

                self.logger.info("Closing Player Info...")
                self.obj.click_element(self.driver, self.obj.get_xpath("Popup_close"))

            self.logger.info("Clicking on AR tab")
            self.obj.click_element(self.driver, self.obj.get_xpath("Ar_tab_link"))
            total_elements = self.obj.wait_for_elements(self.driver, self.obj.get_xpath(
                "Total_ar"))
            for each_ele in total_elements:
                self.logger.info("Clicking on info")
                time.sleep(5)
                self.obj.wait_for_element_inside_webelement(each_ele, self.obj.get_xpath(
                    "Info_link")).click()
                self.logger.info("Getting Info of ARs")
                player_name = self.obj.get_text_from_element(
                    self.obj.wait_for_element(self.driver, self.obj.get_xpath(
                        "Player_name_text")))
                self.logger.info("Got player name %s " % player_name)
                player_price = self.obj.get_text_from_element(
                    self.obj.wait_for_element(self.driver, self.obj.get_xpath(
                        "Player_price_text")))
                player_dict = {
                    'Player Name': player_name,
                    'Price': player_price,
                    'Role': 'AR'
                }
                total_matches = self.obj.wait_for_elements(self.driver, self.obj.get_xpath(
                    "Total_matches"))
                self.logger.info("Getting info of total matches")
                for each_match in total_matches:
                    match_date = self.obj.get_text_from_element(
                        self.obj.wait_for_element_inside_webelement(each_match,
                                                                    self.obj.get_xpath(
                                                                        "Match_date_text")))
                    total_points = self.obj.get_text_from_element(
                        self.obj.wait_for_element_inside_webelement(each_match,
                                                                    self.obj.get_xpath(
                                                                        "Total_points_text")))
                    selected_percentage = self.obj.get_text_from_element(
                        self.obj.wait_for_element_inside_webelement(each_match,
                                                                    self.obj.get_xpath(
                                                                        "Selected_percentage_text")))
                    player_dict = deepcopy(player_dict)
                    player_dict['Match Date'] = match_date
                    player_dict['Total Points'] = total_points
                    player_dict['Selected Percentage'] = selected_percentage
                    total_data.append(player_dict)

                self.logger.info("Closing Player Info...")
                self.obj.click_element(self.driver, self.obj.get_xpath("Popup_close"))

            self.logger.info("Clicking on BOWL tab")
            self.obj.click_element(self.driver, self.obj.get_xpath("Bowl_tab_link"))
            total_elements = self.obj.wait_for_elements(self.driver, self.obj.get_xpath(
                "Total_bowl"))
            for each_ele in total_elements:
                self.logger.info("Clicking on info")
                time.sleep(5)
                self.obj.wait_for_element_inside_webelement(each_ele, self.obj.get_xpath(
                    "Info_link")).click()
                self.logger.info("Getting Info of BOWls")
                player_name = self.obj.get_text_from_element(
                    self.obj.wait_for_element(self.driver, self.obj.get_xpath(
                        "Player_name_text")))
                self.logger.info("Got player name %s " % player_name)
                player_price = self.obj.get_text_from_element(
                    self.obj.wait_for_element(self.driver, self.obj.get_xpath(
                        "Player_price_text")))
                player_dict = {
                    'Player Name': player_name,
                    'Price': player_price,
                    'Role': 'BOWL'
                }
                total_matches = self.obj.wait_for_elements(self.driver, self.obj.get_xpath(
                    "Total_matches"))
                self.logger.info("Getting info of total matches")
                for each_match in total_matches:
                    match_date = self.obj.get_text_from_element(
                        self.obj.wait_for_element_inside_webelement(each_match,
                                                                    self.obj.get_xpath(
                                                                        "Match_date_text")))
                    total_points = self.obj.get_text_from_element(
                        self.obj.wait_for_element_inside_webelement(each_match,
                                                                    self.obj.get_xpath(
                                                                        "Total_points_text")))
                    selected_percentage = self.obj.get_text_from_element(
                        self.obj.wait_for_element_inside_webelement(each_match,
                                                                    self.obj.get_xpath(
                                                                        "Selected_percentage_text")))
                    player_dict = deepcopy(player_dict)
                    player_dict['Match Date'] = match_date
                    player_dict['Total Points'] = total_points
                    player_dict['Selected Percentage'] = selected_percentage
                    total_data.append(player_dict)

                self.logger.info("Closing Player Info...")
                self.obj.click_element(self.driver, self.obj.get_xpath("Popup_close"))
            self.logger.info("Saving to csv")
            save_to_csv(headers, file_name, total_data)

        except WebDriverException:
            self.logger.info("Exception Occurred... writing to the log file")
            self.file_logger.debug(traceback.format_exc())
        finally:
            if self.driver:
                self.driver.quit()
            else:
                print("Driver not initialized")


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
