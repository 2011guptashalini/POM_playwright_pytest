from playwright.sync_api import expect

from products.AdvertisePurple.pages.LoginPage import LoginPage
from products.AdvertisePurple.pages.AffiliateSurveyPage import AffiliateSurveyPage
from products.AdvertisePurple.utils import utils as util
from products.AdvertisePurple.utils import ap_mysql_delete as AP_MYSQL


class TestAffiliateSurvey:
    def test_reaching_affiliate_survey(self, set_up_tear_down) -> None:
        page = set_up_tear_down
        login = LoginPage(page)
        credentials = {'username': util.USERNAME, 'password': util.PASSWORD}
        login.do_login(credentials)
        affiliate_survey = AffiliateSurveyPage(page)
        affiliate_survey.navigate_to_affiliate_survey()
        expect(affiliate_survey.affiliate_survey_page).to_have_text("Affiliate Survey")

    def test_affiliate_profile_section(self, set_up_tear_down) -> None:
        page = set_up_tear_down
        login = LoginPage(page)
        credentials = {'username': util.USERNAME, 'password': util.PASSWORD}
        login.do_login(credentials)
        affiliate_survey = AffiliateSurveyPage(page)
        affiliate_survey.navigate_to_affiliate_survey()
        expect(affiliate_survey.affiliate_survey_page).to_have_text("Affiliate Survey")
        expect(affiliate_survey.affiliate_expand_all).to_be_visible()
        expect(affiliate_survey.affiliate_collapse_all).to_be_visible()
        expect(affiliate_survey.affiliate_profile_toggle_displayed).to_be_visible()
        affiliate_survey.affiliate_profile_toggle()
        affiliate_survey.affiliate_add_contact_click()
        expect(affiliate_survey.affiliate_add_contact).to_be_visible()
        expect(affiliate_survey.affiliate_affiliate_profile_save).to_be_visible()

    def test_affiliate_corporate_name(self, set_up_tear_down, api_setup) -> None:
        page = set_up_tear_down
        cur = api_setup
        login = LoginPage(page)
        credentials = {'username': util.USERNAME, 'password': util.PASSWORD}
        login.do_login(credentials)
        affiliate_survey = AffiliateSurveyPage(page)
        affiliate_survey.navigate_to_affiliate_survey()
        affiliate_survey.affiliate_profile_toggle()
        affiliate_survey.fill_corporate_name("Test Corporate Name")
        affiliate_survey.click_affiliate_profile_save()
        expect(affiliate_survey.affiliate_confirmation_alert).to_be_visible()
        expect(affiliate_survey.affiliate_confirmation_alert).to_have_text("Successfully saved the client information survey.Got it")

        # Getting corporate name saved in DB
        sql_affiliate_corp_name = f'''select affiliateCorporateName from affiliateSurveyProfiles where affiliateId = {affiliate_survey.affiliate_id}'''
        cur.execute(sql_affiliate_corp_name)
        result = cur.fetchone()
        affiliate_corp_name = result[0]
        assert affiliate_corp_name == "Test Corporate Name"
