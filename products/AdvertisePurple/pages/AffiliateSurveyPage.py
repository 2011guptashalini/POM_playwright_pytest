import time

from products.AdvertisePurple.utils import utils as util


class AffiliateSurveyPage:
    def __init__(self, page):
        self.page = page
        # Locators
        self._affiliate_survey_text = self.page.get_by_text("Affiliate Survey", exact=True)
        self._expand_all = self.page.get_by_role("button", name="Expand All")
        self._collapse_all = self.page.get_by_role("button", name="Collapse All")
        self._affiliate_profile = self.page.get_by_role("button", name="Affiliate Profile Click here to toggle.")
        self._add_new_affiliate = self.page.get_by_role("button", name="Add new affiliate domain")
        self._add_new_contact = self.page.get_by_role("button", name="Add new contact")
        self._affiliate_profile_save = self.page.get_by_role("region", name="Affiliate Profile Click here to toggle.").get_by_role("button",
                                                                                                                                   name="Save")

        # finding affiliate id from DB
        sql_query_affiliate_id = f'''select id from affiliates where name = '{util.AFFILIATE_NAME}';'''
        util.connect_db()
        self.affiliate_id = util.run_query(sql_query_affiliate_id)
        util.disconnect_db()

        # Filling affiliate corporate name
        self._affiliate_corporate_name = self.page.get_by_label("Affiliate Corporate Name")
        self._alert = self.page.get_by_role("alert")

    def navigate_to_affiliate_survey(self):
        self.page.goto(f'https://testing.purplyapp.com/affiliates/{self.affiliate_id}/survey')
        time.sleep(10)

    @property
    def affiliate_survey_page(self):
        return self._affiliate_survey_text

    @property
    def affiliate_expand_all(self):
        return self._expand_all

    @property
    def affiliate_collapse_all(self):
        return self._collapse_all

    @property
    def affiliate_profile_toggle_displayed(self):
        return self._affiliate_profile

    def affiliate_profile_toggle(self):
        self._affiliate_profile.click()

    @property
    def affiliate_add_contact(self):
        return self._add_new_contact

    def affiliate_add_contact_click(self):
        self._add_new_contact.click()

    @property
    def affiliate_affiliate_profile_save(self):
        return self._affiliate_profile_save

    def fill_corporate_name(self, corp_name):
        self._affiliate_corporate_name.fill(corp_name)

    def click_affiliate_profile_save(self):
        self._affiliate_profile_save.click()

    @property
    def affiliate_confirmation_alert(self):
        return self._alert

