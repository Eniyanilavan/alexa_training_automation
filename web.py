from flask import Flask, jsonify, abort, request, make_response, url_for
from selenium import webdriver
import psycopg2

conn = psycopg2.connect(database = "alexa", user = "exort", password = "exort123!", host = "exort.ckoboohjx3y0.us-east-1.rds.amazonaws.com", port = "5432")
cur = conn.cursor()

app = Flask(__name__, static_url_path="")

@app.route('/build', methods=['POST'])
def get():
    print(request.json)
    attribute = request.json
    email = attribute['email']
    cmd = ("SELECT temp FROM login where email = '"+email+"'")
    cur.execute(cmd)
    a = cur.fetchall()
    password = a[0][0]
    driver = webdriver.Firefox()
    driver.maximize_window()
    driver.get('https://developer.amazon.com/alexa/console/ask?')
    driver.find_element_by_id('ap_email').send_keys(email)
    driver.find_element_by_id('ap_password').send_keys(password)
    driver.find_element_by_id('signInSubmit').click()
    # driver.find_element_by_id('ap_password').send_keys('eniyan007')
    # driver.find_element_by_id('signInSubmit').click()
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

    # aws lambda

    driver.get('https://www.amazon.com/ap/signin?openid.assoc_handle=aws&openid.return_to=https%3A%2F%2Fsignin.aws.amazon.com%2Foauth%3Fcoupled_root%3Dtrue%26response_type%3Dcode%26redirect_uri%3Dhttps%253A%252F%252Fconsole.aws.amazon.com%252Flambda%252Fhome%253Fregion%253Dus-east-1%2526state%253DhashArgs%252523%25252Ffunctions%2526isauthcode%253Dtrue%26client_id%3Darn%253Aaws%253Aiam%253A%253A015428540659%253Auser%252Flambda&openid.mode=checkid_setup&openid.ns=http%3A%2F%2Fspecs.openid.net%2Fauth%2F2.0&openid.identity=http%3A%2F%2Fspecs.openid.net%2Fauth%2F2.0%2Fidentifier_select&openid.claimed_id=http%3A%2F%2Fspecs.openid.net%2Fauth%2F2.0%2Fidentifier_select&action=&disableCorpSignUp=&clientContext=&marketPlaceId=&poolName=&authCookies=&pageId=aws.login&siteState=registered%2CEN_US&accountStatusPolicy=P1&sso=&openid.pape.preferred_auth_policies=MultifactorPhysical&openid.pape.max_auth_age=120&openid.ns.pape=http%3A%2F%2Fspecs.openid.net%2Fextensions%2Fpape%2F1.0&server=%2Fap%2Fsignin%3Fie%3DUTF8&accountPoolAlias=&forceMobileApp=0&language=EN_US&forceMobileLayout=0&awsEmail=dayanidhicse%40gmail.com')
    driver.find_element_by_id('ap_password').send_keys('karthikayan92D')
    driver.find_element_by_id('signInSubmit-input')
    # driver.quit()
    return make_response(jsonify({'status': True}), 200)

if __name__ == '__main__':
    app.run(host = '0.0.0.0', port=5005)