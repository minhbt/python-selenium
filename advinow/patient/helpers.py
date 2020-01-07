import requests
from bs4 import BeautifulSoup

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options


import logging
logger = logging.getLogger(__name__)

USERNAME = "advichrono"
PASSWORD = "Advinowapis1!"
ORIGIN_URL = 'https://advichrono.drchrono.com'


#=====================================================================================
#  THIS VERSION USING SELENIUM HEADLESS BROWSER TO SUBMIT CREATE PATIENT REQUEST
#=====================================================================================

#  Pipelines to register processing pipelines for view
pipelines = {
    "create": []
}

    
def register(view, field):
    """
    Decorator to register a function to handle input value using webdriver
    """
    def decor_func(func):
        if view not in pipelines.keys():
            # If view not in supported, we dont have to wrap
            return func
        
        pipelines[view].append((field, func))
        return func
    return decor_func


@register('create', None)
def _perform_login(webdriver=None):
    webdriver.get(f"{ORIGIN_URL}/accounts/login/")

    user_ele = webdriver.find_element_by_id("username")
    user_ele.send_keys(USERNAME)

    pass_ele = webdriver.find_element_by_id("password")
    pass_ele.send_keys(PASSWORD)

    login_btn = webdriver.find_element_by_id("login")
    login_btn.click()


@register('create', None)
def _goto_add_view(webdriver=None):
    webdriver.get(f"{ORIGIN_URL}/patients/new/")


@register('create', 'first_name')
def _set_first_name(value, webdriver=None):
    first_name_input = webdriver.find_element_by_id("id_first_name")
    first_name_input.click()
    first_name_input.send_keys(value)


@register('create', 'last_name')
def _set_last_name(value, webdriver=None):
    last_name_input = webdriver.find_element_by_id("id_last_name")
    last_name_input.click()
    last_name_input.send_keys(value)


@register('create', 'nick_name')
def _set_nick_name(value, webdriver=None):
    nick_name_input = webdriver.find_element_by_id("id_nick_name")
    nick_name_input.click()
    nick_name_input.send_keys(value)


@register('create', 'middle_name')
def _set_middle_name(value, webdriver=None):
    middle_name_input = webdriver.find_element_by_id("id_middle_name")
    middle_name_input.click()
    middle_name_input.send_keys(value)


@register('create', None)
def _active_extra_tab(webdriver=None):
    tab_extra_ele = webdriver.find_element_by_css_selector("a[class='nav_link'][href='#tabs-extra']")
    tab_extra_ele.click()


@register('create', 'ssn')
def _set_ssn(value, webdriver=None):
    ssn_input = webdriver.find_element_by_id("id_social_security_number")
    ssn_input.click()
    ssn_input.send_keys(value)


@register('create', 'dob')
def _set_dob(value, webdriver=None):
    formated_value = f"{value.month}/{value.day}/{value.year}"
    dob_input = webdriver.find_element_by_id("id_date_of_birth")
    dob_input.send_keys(formated_value)
    dob_input.send_keys(Keys.ESCAPE)


@register('create', 'approx_age')
def _set_age_approx(value, webdriver=None):
    age_approximate_input = webdriver.find_element_by_id("id_age_approximate")
    age_approximate_input.send_keys(value)


@register('create', 'sex')
def _set_sex(value, webdriver=None):
    male_option = webdriver.find_element_by_css_selector(f"select[id='id_gender'] option[value='{value}']")
    male_option.click()


@register('create', 'gender_id')
def _set_gender_identity(value, webdriver=None):
    gender_id_option = webdriver.find_element_by_css_selector(f"select[id='id_gender_identity'] option[value='{value}']")
    gender_id_option.click()


@register('create', 'sexual_orientation')
def _set_sexual_orientation(value, webdriver=None):
    sexual_orientation_option = webdriver.find_element_by_css_selector(f"select[id='id_sexual_orientation'] option[value='{value}']")
    sexual_orientation_option.click()


@register('create', 'race')
def _set_race(value, webdriver=None):
    race_btn = webdriver.find_element_by_css_selector('div[id="id_row_race"] button')
    race_btn.click()  # Open race menu
    for race in value:
        race_checkbox = webdriver.find_element_by_css_selector(f"div[id='id_row_race'] input[type='checkbox'][value='{race}']")
        race_checkbox.click()
    race_btn.click()  # Close race menu


@register('create', 'ethnicity')
def _set_ethnicity(value, webdriver=None):
    ethnicity_option = webdriver.find_element_by_css_selector(f"select[id='id_ethnicity'] option[value='{value}']")
    ethnicity_option.click()


@register('create', 'preferred_language')
def _set_preferred_language(value, webdriver=None):
    preferred_lang_option = webdriver.find_element_by_css_selector(f"select[id='id_preferred_language'] option[value='{value}']")
    preferred_lang_option.click()


@register('create', 'student_status')
def _set_student_status(value, webdriver=None):
    student_status_option = webdriver.find_element_by_css_selector(f"select[id='id_patient_student_status'] option[value='{value}']")
    student_status_option.click()


@register('create', 'country')
def _set_country(value, webdriver=None):
    country_options = webdriver.find_element_by_css_selector(f'select[id="id_country"] option[value="{value}"]')
    country_options.click()


@register('create', 'address')
def _set_address(value, webdriver=None):
    address_input = webdriver.find_element_by_id("id_address")
    address_input.send_keys(value)


@register('create', 'zip_code')
def _set_zip_code(value, webdriver=None):
    zipcode_input = webdriver.find_element_by_id("id_patient_zip_code")
    zipcode_input.send_keys(value)


@register('create', 'city')
def _set_city(value, webdriver=None):
    city_input = webdriver.find_element_by_id('id_city')
    city_input.send_keys(value)


@register('create', 'state')
def _set_state(value, webdriver=None):
    state_options = webdriver.find_element_by_css_selector(f'select[id="id_patient_state"] option[value="{value}"]')
    state_options.click()


@register('create', 'county_code')
def _set_county_code(value, webdriver=None):
    county_code_input = webdriver.find_element_by_id('id_patient_county_code')
    county_code_input.send_keys(value)


@register('create', None)
def _perform_submit(webdriver=None):
    submit_btn = webdriver.find_element_by_css_selector('input[type="submit"][name="_save"]')
    webdriver.execute_script("arguments[0].click();", submit_btn)

    WebDriverWait(webdriver, 10).until(
        EC.url_matches(f'{ORIGIN_URL}/patients/(?!new)')
    )
    logger.info('Save patient successful')


#  This version using selenium headless browser to create patient (avg speed 25s)
def create_patient(data):
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    driver = webdriver.Chrome(options=chrome_options)
    result = True, None

    try:
        for field, func in pipelines['create']:
            if field is not None:
                value = data.get(field)
                if value is not None:
                    func(data.get(field), webdriver=driver)
            else:
                func(webdriver=driver)
        logger.info('Executed all create view pipelines.')
    except Exception as e:
        result = False, e
        logger.error(e)
        logger.info(f'{dir(e)}')
    finally:
        driver.close()
    
    return result


#=====================================================================================
#  THIS VERSION USING REQUESTS FOR BETTER PERFORMANCE (avg speed 6s)
#=====================================================================================

def _perform_login_v2(session):
    # Login to retrieve a session cookies
    r = session.get(f'{ORIGIN_URL}/accounts/login/')
    soup = BeautifulSoup(r.text)
    payload = {}
    for element in soup.select('form input'):
        payload[element.attrs['name']] = element.attrs['value']
    payload['username'] = USERNAME
    payload['password'] = PASSWORD

    req = requests.Request(
        'POST', 
        r.url, 
        data=payload, 
        cookies=session.cookies, 
        headers={
            "Origin": ORIGIN_URL,
            "Referer": r.url,
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
            "Accept-Language": "en-US,en;q=0.9",
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.88 Safari/537.36"
        })
    prepped = session.prepare_request(req)
    r = session.send(prepped)
    return r


def _perform_submit_create_v2(session, data):
    r = session.get(f'{ORIGIN_URL}/patients/new/')
    soup = BeautifulSoup(r.text)
    payload = {}

    for element in soup.select('form[id="profileForm"] input , form[id="profileForm"] select , form[id="profileForm"] textarea'):
        key = element.attrs.get('name')
        if not key:
            continue
        
        payload[key] = element.attrs.get('value')
        if element.name == 'select':
            option = element.select_one('option[selected]')
            if option:
                payload[key] = option.attrs.get('value')

    files = {}
    for element in soup.select('form[id="profileForm"] input[type="file"]'):
        key = element.attrs.get('name')
        del payload[key]
        files[key] = element.attrs.get('value')

    payload['first_name'] = data.get('first_name')
    payload['nick_name'] = data.get('nick_name')
    payload['middle_name'] = data.get('middle_name')
    payload['last_name'] = data.get('last_name')

    payload['social_security_number'] = data.get('ssn')

    dob = data.get('dob')
    if dob:
        payload['date_of_birth'] = f"{dob.month}/{dob.day}/{dob.year}"
    
    payload['age_approximate'] = data.get('approx_age')
    payload['gender'] = data.get('sex')
    payload['gender_identity'] = data.get('gender_id')
    payload['sexual_orientation'] = data.get('sexual_orientation')

    payload['race'] = ','.join(data.get('race') or ['blank'])
    payload['ethnicity'] = data.get('ethnicity')
    payload['preferred_language'] = data.get('preferred_language')
    payload['patient_student_status'] = data.get('student_status')

    payload['patient_zip_code'] = data.get('zip_code')
    payload['country'] = data.get('country')
    payload['address'] = data.get('address')
    payload['city'] = data.get('city')
    payload['patient_county_code'] = data.get('county_code')
    payload['patient_state'] = data.get('state')
    payload['_save'] = 'Save'

    req = requests.Request(
        'POST', 
        r.url, 
        files=files,
        data=payload, 
        cookies=session.cookies, 
        headers={
            "Origin": ORIGIN_URL,
            "Referer": r.url,
            "Accept-Encoding": "gzip, deflate, br",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
            "Accept-Language": "en-US,en;q=0.9",
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.88 Safari/537.36"
        })
    prepped = session.prepare_request(req)
    r = session.send(prepped)
    return r


def create_patient_v2(data):
    session = requests.Session()  # Start a session to track cookie and web session
    result = True, None

    r = _perform_login_v2(session)
    if r.status_code != 200:
        return False, Exception('Cannot login using requests')
    
    # Submit create patient request
    r = _perform_submit_create_v2(session, data)
    if r.status_code != 200:
        return False, Exception('Cannot create patient using request')
    
    return result
