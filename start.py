from flask import Flask, jsonify, abort, request, make_response, url_for
# import json
from selenium import webdriver
import requests


app = Flask(__name__, static_url_path="")


def res_builder(output, reprompt, session_att, session):
    responce = \
        {
            "version": "1.0",
            "sessionAttributes": session_att,
            "response": {
                "outputSpeech": {
                    "type": "PlainText",
                    "text": output,
                },
                "card": {
                    "type": "Standard",
                    "title": "Title of the card",
                    "content": "Content of a simple card",
                    "text": "Text content for a standard card",
                },
                "reprompt": {
                    "outputSpeech": {
                        "type": "PlainText",
                        "text": reprompt,
                    }
                },
                "shouldEndSession": session
            }
        }
    return responce


@app.errorhandler(400)
def not_found(error):
    return make_response(jsonify({'error': 'Bad request'}), 400)


@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found'}), 404)


@app.route('/', methods=['POST'])
def post_tasks():
    # print(request.json)
    responce = functions[request.json['request']["type"]](request.json)
    return jsonify(responce)

@app.route('/', methods=['GET'])
def get_tasks():
    return "<h1 style = 'color:#ce4327;text-align:center'>EXORT</h1>"


launch_req = 'Train your self is a skill, that lets you to train skills for me without touching your keyboard, to start say new skill or edit skill followed by skill name'

news = "inside skill "

newi = "created new intent "

editif = "no intent named "

editis = "inside intent "

utteranceadd = "added utterance "

invocations = " has been set as your invocation word or sentance."

def launchrequest(json):
    return res_builder(launch_req, launch_req, {"skill":""}, False)

def intentrequest(json):
    # print("aaaaa",json)
    name = json["request"]["intent"]["name"]
    result = functions[name](json)
    return result

def newskill(json):
    slots = json["request"]["intent"]["slots"]
    skillname = slots["utterance"]["value"]
    return res_builder(news+skillname+'say your invocation word or utterance, for example try saying "set trigger word as my invocation word".', news+skillname, {"skill":skillname,"intent":[]}, False)

def addintent(json):
    slots = json["request"]["intent"]["slots"]
    name = slots["utterance"]["value"]
    attribute = json["session"]["attributes"]
    if name not in attribute["intent"]:
        attribute["intent"].append(name)
        attribute["currentintent"] = name
        attribute[name] = []
        return res_builder(newi + name + 'say add utterance, utterance to add a utterance to the intent', newi + name + 'say add utterance, utterance to add a utterance to the intent', attribute, False)
    else:
        return res_builder("intent " + name + " already exists.", "intent " + name + " already exists.", attribute, False)

def editintent(json):
    slots = json["request"]["intent"]["slots"]
    name = slots["utterance"]["value"]
    attribute = json["session"]["attributes"]
    if name not in attribute["intent"]:
        return res_builder(editif + name+" add the intent before editing it", editif + name, attribute, False)
    else:
        attribute["currentintent"] = name
        return res_builder(editis + name, editis + name, attribute, False)

def intentutterance(json):
    slots = json["request"]["intent"]["slots"]
    utterance = slots["speech"]["value"]
    attribute = json["session"]["attributes"]
    intent = attribute["currentintent"]
    attribute[intent].append(utterance)
    return res_builder(utteranceadd + utterance, utteranceadd + utterance, attribute, False)

def invocation(json):
    slots = json["request"]["intent"]["slots"]
    name = slots["utterance"]["value"]
    attribute = json["session"]["attributes"]
    attribute["invocation"] = name
    return res_builder(name + invocations + "say add or create intent, intent name to create intent", name + invocations, attribute, False)

def savemodel(json):
    attribute = json["session"]["attributes"]
    if "skill" not in attribute or "invocation" not in attribute:
        return res_builder("something went wrong please try again", "something went wrong please try again", attribute, False)
    else:
        automation(attribute)
        return res_builder("build started", "build started", attribute, True)

def automation(attribute):
    data = {
			"invocation": "set create vm",
			"skill": "create vm",
			"currentintent": "create",
			"create": [
				"create my vm",
				"create vm"
			],
			"delete": [
				"delete intent"
			],
			"intent": [
				"create",
				"delete"
			]
		}
    requests.post('http://localhost:5005/build',data=data)
    # driver = webdriver.Firefox()
    # driver.maximize_window()
    # driver.get(
    #     'https://www.amazon.com/ap/signin?clientContext=132-0852981-8720006&openid.return_to=https%3A%2F%2Fdeveloper.amazon.com%2Falexa%2Fconsole%2Fask&openid.identity=http%3A%2F%2Fspecs.openid.net%2Fauth%2F2.0%2Fidentifier_select&openid.assoc_handle=mas_dev_portal&openid.mode=checkid_setup&marketPlaceId=ATVPDKIKX0DER&openid.claimed_id=http%3A%2F%2Fspecs.openid.net%2Fauth%2F2.0%2Fidentifier_select&pageId=amzn_developer_portal&openid.ns=http%3A%2F%2Fspecs.openid.net%2Fauth%2F2.0&siteState=clientContext%3D135-7286414-6312915%2CsourceUrl%3Dhttps%253A%252F%252Fdeveloper.amazon.com%252Falexa%252Fconsole%252Fask%2Csignature%3Dnull&language=en_US')
    # driver.implicitly_wait(2)
    # driver.find_element_by_id('ap_email').send_keys('r.eniyanilavan@gmail.com')
    # driver.find_element_by_id('ap_password').send_keys('eniyan007')
    # driver.find_element_by_id('signInSubmit').click()
    # driver.implicitly_wait(10)
    # driver.find_element_by_xpath("//button[@class='astro__button astro__button--primary']").click()
    # driver.find_element_by_xpath(
    #     "//input[@class='astro-text-super astro-text-light skill-name-input-field']").send_keys('aaaaaa')
    # driver.find_element_by_xpath("//button[@class='astro__button astro__button--primary']").click()
    # driver.find_element_by_xpath("//button[@class='astro__button astro__button--primary' and @title='Select']").click()
    # driver.find_element_by_xpath("//button[@class='astro__button as-end astro__button--primary']").click()
    # driver.implicitly_wait(10)
    # driver.find_element_by_xpath("//a[@class='nav-item-header-link' and @title='Invocation']").click()
    # driver.find_element_by_xpath("//div[@class='form-field__wrapper']/input[1]").send_keys("asdsfad")
    # # driver.find_element_by_class_name('nav-item-header-link').click()
    return res_builder("build successful test your skill", "build successful test your skill", attribute, True)

functions = {
    "LaunchRequest": launchrequest,
    "IntentRequest": intentrequest,
    "invocation" : invocation,
    "newskill" : newskill,
    "newintent": addintent,
    "editintent": editintent,
    "intentutterance": intentutterance,
    "savemodel": savemodel,
}



if __name__ == '__main__':
    context = ('E:\\programing\\selinium_py\\alexa_automation\\certificate.pem', 'E:\\programing\\selinium_py\\alexa_automation\\key.pem')
    app.run(host = '0.0.0.0', port=3000, ssl_context=context)




# driver = webdriver.Firefox()
# driver.maximize_window()
# driver.get(
#     'https://www.amazon.com/ap/signin?clientContext=132-0852981-8720006&openid.return_to=https%3A%2F%2Fdeveloper.amazon.com%2Falexa%2Fconsole%2Fask&openid.identity=http%3A%2F%2Fspecs.openid.net%2Fauth%2F2.0%2Fidentifier_select&openid.assoc_handle=mas_dev_portal&openid.mode=checkid_setup&marketPlaceId=ATVPDKIKX0DER&openid.claimed_id=http%3A%2F%2Fspecs.openid.net%2Fauth%2F2.0%2Fidentifier_select&pageId=amzn_developer_portal&openid.ns=http%3A%2F%2Fspecs.openid.net%2Fauth%2F2.0&siteState=clientContext%3D135-7286414-6312915%2CsourceUrl%3Dhttps%253A%252F%252Fdeveloper.amazon.com%252Falexa%252Fconsole%252Fask%2Csignature%3Dnull&language=en_US')
# driver.implicitly_wait(2)
# driver.find_element_by_id('ap_email').send_keys('r.eniyanilavan@gmail.com')
# driver.find_element_by_id('ap_password').send_keys('eniyan007')
# driver.find_element_by_id('signInSubmit').click()
# driver.implicitly_wait(10)
# driver.find_element_by_xpath("//button[@class='astro__button astro__button--primary']").click()
# driver.find_element_by_xpath(
#     "//input[@class='astro-text-super astro-text-light skill-name-input-field']").send_keys('aaaaaa')
# driver.find_element_by_xpath("//button[@class='astro__button astro__button--primary']").click()
# driver.find_element_by_xpath("//button[@class='astro__button astro__button--primary' and @title='Select']").click()
# driver.find_element_by_xpath("//button[@class='astro__button as-end astro__button--primary']").click()
# driver.implicitly_wait(10)
# driver.find_element_by_xpath("//a[@class='nav-item-header-link' and @title='Invocation']").click()
# driver.find_element_by_xpath("//div[@class='form-field__wrapper']/input[1]").send_keys("asdsfad")



# data = {
# 			"invocation": "set create vm",
# 			"skill": "create vm",
# 			"currentintent": "create",
# 			"create": [
# 				"create my vm",
# 				"create vm"
# 			],
# 			"delete": [
# 				"delete intent"
# 			],
# 			"intent": [
# 				"create",
# 				"delete"
# 			]
# 		}
# requests.post('http://localhost:5005/build',json=data)
# print("zsad")