
try:
    import os
    import time
    from seleniumwire import webdriver
    from selenium.webdriver.common.by import By
    from selenium.webdriver.support.ui import WebDriverWait
    from selenium.webdriver.support import expected_conditions as EC

    from selenium.webdriver.support.ui import Select
except Exception as e:
    print("Contact the program, You need to install some of library")
    print(e)
    time.sleep(10)
    exit()

def green(text):
    return f"\033[92m{text}\033[0m"


class Massar:
    def __init__(self):
        self.email = ""
        self.password = ""
        self.driver = ""
        self.get_data()

    def get_data(self):
        with open('./data.txt', 'r') as f:
            lines = f.readlines()
        self.email = lines[0].strip()
        self.password = lines[1].strip()
        return


    def get_driver(self):
        options = webdriver.ChromeOptions()
        options.add_argument("--headless=new")
        options.add_argument("--disable-gpu")
        options.add_argument("--disable-images")
        options.add_argument("--enable-features=NetworkService,NetworkServiceInProcess")

        options.add_argument("--log-level=3")

        mobile_emulation = {
            "deviceMetrics": {"width": 375, "height": 812, "pixelRatio": 3},
            "userAgent": "Mozilla/5.0 (Linux; Android 10; Pixel 3)"
        }
        #
        options.add_experimental_option("mobileEmulation", mobile_emulation)
        mobile_ua = "Mozilla/5.0 (Linux; Android 10; Pixel 3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.210 Mobile Safari/537.36"
        options.add_argument(f"user-agent={mobile_ua}")

        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
        options.add_argument("--disable-blink-features=AutomationControlled")


        def block_unwanted_requests(request):

                # if request.url.endswith(('.jpg', '.png', '.gif', '.css')):
                if request.url.endswith(('.png', '.jpg', '.jpeg', '.gif', '.svg', '.css', '.woff', '.woff2', '.ttf')):
                    request.abort()





        try:
            self.driver = webdriver.Chrome(options=options)
            self.driver.request_interceptor = block_unwanted_requests
            # print("DRIVER IS DONE")
        except:
            print("line 42 interaction.py")
        else:
            return True
    def calculate_usage(self):
        print('here')
        total_bytes = sum(len(request.response.body) for request in self.driver.requests if request.response)

        # Convert bytes to MB
        total_mb = total_bytes / (1024 * 1024)
        total_data = 0
        requests_data = []

        for request in self.driver.requests:
            if request.response:
                request_size = len(request.body) if request.body else 0
                response_size = len(request.response.body) if request.response.body else 0
                total_size = request_size + response_size
                total_data += total_size

                # Save request details
                requests_data.append((request.url, total_size))

        # Sort by highest usage
        requests_data.sort(key=lambda x: x[1], reverse=True)

        # Print the top requests consuming the most data
        print(f"Total data usage: {total_data / 1024:.2f} KB")
        print("Top data-consuming requests:")
        for url, size in requests_data[:10]:  # Show top 5 largest requests
            print(f"{url} → {size / 1024:.2f} KB")

        print(f"Total Data Transferred: {total_mb:.2f} MB")
        return total_mb

    def get_site(self):
        # print("GETTING THE SITE")
        try:
            self.driver.get("https://massar.men.gov.ma/Account")
        except Exception as e:
            print("WE CAN't OPEN THE BROWSER")
            return False
        else:
            # print("SITE OPENED")
            return True
    def fill_username(self):
        try:
            WebDriverWait(self.driver, 10).until(
                EC.visibility_of_element_located(
                    (
                        By.ID,"UserName",
                    )
                )
            )
        except Exception as e:
            print('line 60 interaction.py', e)
            return False
        else:
            username = self.driver.find_element(By.ID, "UserName")
            username.send_keys(self.email)
            # print("USERNAME FIELD DONE")
            return True

    def fill_password(self):
        password = self.driver.find_element(By.ID, "Password")
        password.send_keys(self.password)
        # print("PASSWORD FIELD DONE")
        return

    def submit_form(self):
        # submit the form
        sumbit_button = self.driver.find_element(By.ID, "btnSubmit")
        sumbit_button.click()
        # print("BUTTON CLICKED")
        # checking if we've getting any error while submiting the form
        # if not self.check_error_login():

        try:
            WebDriverWait(self.driver, 300).until(
                EC.presence_of_element_located(
                    (
                        By.ID, "sidebar-menu",
                    )
                )
            )
        except Exception as e:
            print('line 91, interaction.py', e)
            print("PLEASE CHECK YOUR LOGIN INFORMATION AND TRY AGAIN.")
            self.exit_program()
        else:
            print("WE HAVE SUCCESSFULLY LOGGED INTO YOUR ACCOUNT")
        return

    def exit_program(self):
        print("EXITING THE PROGRAM -- GOODBYE --")
        self.driver.close()
        self.driver.quit()

    def main_interaction(self):
        try:
            if self.get_driver():
                if self.get_site():
                    self.fill_username()
                    self.fill_password()
                    self.submit_form()
                    return True
                else:
                    self.driver.quit()
                    return False
            else:
                return False
        except:
            print("Browsing context has been discarded. Stopping further execution.")
            return False

    def get_absence_site(self):
        self.driver.get('https://massar.men.gov.ma/Evaluation/Absence/AbsenceJournaliereParEleve')
        try:
            WebDriverWait(self.driver, 3).until(
                EC.visibility_of_element_located((
                    By.XPATH, '//*[@id="Model_msg_Btn"]'
                ))
            )
        except:
            pass
        else:
            self.driver.find_element(By.XPATH, '//*[@id="Model_msg_Btn"]').click()
            print('closed clicked')


    def main_loop(self, nom_class, month, eleve, log_message):
        print(nom_class)
        TypeEnseignement = self.driver.find_element(By.ID, "TypeEnseignement")
        TypeEnseignement_all_options = TypeEnseignement.find_elements(By.TAG_NAME, "option")
        TypeEnseignement_Select = Select(TypeEnseignement)

        for TypeEnseignement_option in TypeEnseignement_all_options:
            try:
                WebDriverWait(self.driver, 5).until(
                    EC.invisibility_of_element_located(
                        (
                            By.ID, "loadingDiv",
                        )
                    )
                )
            except Exception as e:
                print('line 146 interaction.py', e)
                print("CHECK YOUR INTERNET CONNECTION THEN TRY AGAIN")
            TypeEnseignement_Select.select_by_value(TypeEnseignement_option.get_attribute("value"))

            Cycle = self.driver.find_element(By.ID, "Cycle")
            Cycle_all_options = Cycle.find_elements(By.TAG_NAME, "option")

            Cycle_Select = Select(Cycle)

            for Cycle_option in Cycle_all_options:
                if Cycle_option.text != "":
                    Cycle_Select.select_by_value(Cycle_option.get_attribute("value"))
                    Niveau = self.driver.find_element(By.ID, "Niveau")
                    Niveau_all_options = Niveau.find_elements(By.TAG_NAME, "option")
                    Niveau_Select = Select(Niveau)

                    for Niveau_option in Niveau_all_options:
                        if Niveau_option.text != "":
                            Niveau_Select.select_by_value(Niveau_option.get_attribute("value"))
                            try:
                                WebDriverWait(self.driver, 5).until(
                                    EC.invisibility_of_element_located(
                                        (
                                            By.ID, "loadingDiv",
                                        )
                                    )
                                )
                            except Exception as e:
                                print('line 146 interaction.py', e)
                                print("CHECK YOUR INTERNET CONNECTION THEN TRY AGAIN")

                            Classe = self.driver.find_element(By.ID, "Classe")
                            Classe_all_options = Classe.find_elements(By.TAG_NAME, "option")
                            Classe_Select = Select(Classe)

                            for Classe_option in Classe_all_options:
                                if Classe_option.text == nom_class.upper():
                                    Classe_Select.select_by_value(Classe_option.get_attribute("value"))
                                    Mois_Select = Select(self.driver.find_element(By.ID, "Mois"))
                                    Mois_Select.select_by_value(month)
                                    try:
                                        WebDriverWait(self.driver, 1).until(
                                            EC.visibility_of_element_located((
                                                By.XPATH, '//*[@id="Model_msg_Btn"]'
                                            ))
                                        )
                                    except:
                                        pass
                                    else:
                                        self.driver.find_element(By.XPATH, '//*[@id="Model_msg_Btn"]').click()
                                        print('closed clicked')
                                    try:
                                        WebDriverWait(self.driver, 10).until(
                                            EC.invisibility_of_element_located(
                                                (
                                                    By.ID, "loadingDiv",
                                                )
                                            )
                                        )
                                    except Exception as e:
                                        pass

                                    try:
                                        WebDriverWait(self.driver, 15).until(
                                            EC.element_to_be_clickable((By.CSS_SELECTOR,
                                                                        '#search > div > div > div > div.box-body > div.blocBtn > button'))
                                        )
                                    except Exception as e:
                                        print('LINE 204 interaction.py',e)
                                        pass
                                    else:
                                        self.searchBtn = self.driver.find_element(By.CSS_SELECTOR,
                                                                                  '#search > div > div > div > div.box-body > div.blocBtn > button')
                                        self.searchBtn.click()
                                    try:
                                        WebDriverWait(self.driver, 3).until(
                                            EC.invisibility_of_element_located(
                                                (
                                                    By.ID, "loadingDiv",
                                                )
                                            )
                                        )
                                    except Exception as e:
                                        pass
                                    else:
                                        print("Counting absence...")
                                        select_element = Select(self.driver.find_element(By.ID, "Eleve"))
                                        unique_options = list({opt.text.strip(): opt for opt in select_element.options}.values())

                                        # Loop through all <option> elements, print their text, and select each option
                                        log_message(str(len(unique_options)) + ' Eleves')
                                        # y = input("Toutes les eleves? (o/n)")
                                        # if y.lower() == 'n':
                                        #     nom = input("Entrer le nom: ")
                                        #     input_parts = set(nom.lower().split())
                                        for option in unique_options:
                                            if eleve:
                                                full_parts = set(option.text.lower().split())
                                                input_parts = set(eleve.lower().split())
                                                if not input_parts.issubset(full_parts):
                                                    continue
                                            select_element.select_by_visible_text(option.text)
                                            try:
                                                WebDriverWait(self.driver, 3).until(
                                                    EC.element_to_be_clickable((By.CSS_SELECTOR,
                                                                                '#search > div > div > div > div.box-body > div.blocBtn > button'))
                                                ).click()
                                            except:
                                                while True:
                                                    try:
                                                        WebDriverWait(self.driver, 1).until(
                                                            EC.presence_of_element_located((
                                                                By.XPATH, '//*[@id="Model_msg_Btn"]'
                                                            ))
                                                        )
                                                    except:
                                                        break
                                                    else:
                                                        self.driver.find_element(By.XPATH, '//*[@id="Model_msg_Btn"]').click()
                                                        print('closed clicked')
                                                        try:
                                                            WebDriverWait(self.driver, 3).until(
                                                                EC.element_to_be_clickable((By.CSS_SELECTOR,
                                                                                            '#search > div > div > div > div.box-body > div.blocBtn > button'))
                                                            ).click()
                                                        except:
                                                            pass
                                            else:
                                                try:
                                                    WebDriverWait(self.driver, 3).until(
                                                        EC.invisibility_of_element_located(
                                                            (
                                                                By.ID, "loadingDiv",
                                                            )
                                                        )
                                                    )
                                                except Exception as e:
                                                    pass
                                                else:
                                                    while True:
                                                        try:
                                                            WebDriverWait(self.driver, 1).until(
                                                                EC.visibility_of_element_located((
                                                                    By.XPATH, '//*[@id="Model_msg_Btn"]'
                                                                ))
                                                            )
                                                        except:
                                                            break
                                                        else:
                                                            self.driver.find_element(By.XPATH, '//*[@id="Model_msg_Btn"]').click()
                                                            print('closed clicked')
                                                            time.sleep(1)
                                                            try:
                                                                WebDriverWait(self.driver, 3).until(
                                                                    EC.element_to_be_clickable((By.CSS_SELECTOR,
                                                                                                '#search > div > div > div > div.box-body > div.blocBtn > button'))
                                                                ).click()
                                                            except:
                                                                pass

                                            # self.searchBtn.click()
                                                # try:
                                                #     WebDriverWait(m.driver, 5).until(
                                                #         EC.presence_of_element_located((
                                                #             By.XPATH, '//*[@id="Model_msg_Btn"]'
                                                #         ))
                                                #     )
                                                # except:
                                                #     print("here")
                                                #     pass
                                                # else:
                                                #     m.driver.find_element(By.XPATH, '//*[@id="Model_msg_Btn"]').click()
                                                #     print('closed clicked')

                                                checkboxes = self.driver.find_elements(By.CSS_SELECTOR,
                                                                                       '#DataTables-Table-0 input[type="checkbox"][data-val="True"]')

                                                # print(green(option.text), green(count))

                                                log_message(str(option.text)+" : " +str(len(checkboxes)) )
                                        return
if __name__ == "__main__":
    m = Massar()
    m.main_interaction()
    m.get_absence_site()
    mois = input("Entrez le mois : ")
    # print("Entrer X pour quitter")
    while True:
        try:
            WebDriverWait(m.driver, 1).until(
                EC.visibility_of_element_located((
                    By.XPATH, '//*[@id="Model_msg_Btn"]'
                ))
            )
        except:
            pass
        else:
            m.driver.find_element(By.XPATH, '//*[@id="Model_msg_Btn"]').click()
            print('closed clicked')
        nom_classe = input("Entrez le nom du classe : ")
        if nom_classe.upper() == 'X':
            m. exit_program()
            exit()
        else:
            m.main_loop(nom_class=nom_classe, month=mois)




