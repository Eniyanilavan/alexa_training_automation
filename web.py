from flask import Flask, jsonify, abort, request, make_response, url_for
from selenium import webdriver

app = Flask(__name__, static_url_path="")

@app.route('/build', methods=['POST'])
def get():
    print(request.json)
    attribute = request.json
    driver = webdriver.Firefox()
    driver.maximize_window()
    driver.get(
        'https://www.amazon.com/ap/signin?clientContext=132-0852981-8720006&openid.return_to=https%3A%2F%2Fdeveloper.amazon.com%2Falexa%2Fconsole%2Fask&openid.identity=http%3A%2F%2Fspecs.openid.net%2Fauth%2F2.0%2Fidentifier_select&openid.assoc_handle=mas_dev_portal&openid.mode=checkid_setup&marketPlaceId=ATVPDKIKX0DER&openid.claimed_id=http%3A%2F%2Fspecs.openid.net%2Fauth%2F2.0%2Fidentifier_select&pageId=amzn_developer_portal&openid.ns=http%3A%2F%2Fspecs.openid.net%2Fauth%2F2.0&siteState=clientContext%3D135-7286414-6312915%2CsourceUrl%3Dhttps%253A%252F%252Fdeveloper.amazon.com%252Falexa%252Fconsole%252Fask%2Csignature%3Dnull&language=en_US')
    driver.implicitly_wait(2)
    driver.find_element_by_id('ap_email').send_keys('r.eniyanilavan@gmail.com')
    driver.find_element_by_id('ap_password').send_keys('eniyan007')
    driver.find_element_by_id('signInSubmit').click()
    driver.implicitly_wait(10)
    driver.find_element_by_xpath("//button[@class='astro__button astro__button--primary']").click()
    driver.find_element_by_xpath(
        "//input[@class='astro-text-super astro-text-light skill-name-input-field']").send_keys(attribute['invocation'])
    driver.find_element_by_xpath("//button[@class='astro__button astro__button--primary']").click()
    driver.find_element_by_xpath("//button[@class='astro__button astro__button--primary' and @title='Select']").click()
    driver.find_element_by_xpath("//button[@class='astro__button as-end astro__button--primary']").click()
    driver.implicitly_wait(10)
    driver.find_element_by_xpath("//a[@class='nav-item-header-link' and @title='Invocation']").click()
    driver.find_element_by_xpath("//div[@class='form-field__wrapper']/input[1]").send_keys("create vm")
    driver.implicitly_wait(10)
    for i in attribute['intent']:
        driver.find_element_by_xpath("//div[@class='left-nav-menu']/div[2]/ol/li[1]/ol/li[1]/ol/li[2]/span/span/a[2]").click()
        driver.find_element_by_xpath("//div[@class='form-field__wrapper']/input[1]").send_keys(i)
        driver.find_element_by_xpath("//button[@class='astro__button custom-button astro__button--primary']").click()
        for j in attribute[i]:
            driver.find_element_by_xpath("//div[@class='notranslate public-DraftEditor-content']").send_keys(j)
            driver.find_element_by_xpath("//button[@class='chromeless' and @data-qa-hook='edit-intent-sample-add-new-button']").click()
        # driver.find_element_by_xpath("//section[@class='sub-header-top p-x-xl m-b-md']/button[1]").click()
        # driver.implicitly_wait(10)
        driver.find_element_by_xpath("//section[@class='sub-header-top p-x-xl m-b-md']/button[2]").click()
    return make_response(jsonify({'status': True}), 200)

if __name__ == '__main__':
    app.run(host = '0.0.0.0', port=5005)