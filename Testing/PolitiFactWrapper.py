import json
import requests
from Testing.nltk_spike import StatementNatLangProcessor

editions = []
base_url = "http://www.politifact.com/api/statements/"

all_statements = {}


class Statement:
    def __init__(self, json):
        self.json_ = json
        self.text = self.get_statement_text()
        self.speaker = self.get_statement_speaker()

    def get_statement_text(self):
        return self.json_[0]["statement"]

    def get_statement_speaker(self):
        return self.json[0]["name_slug"]


def get_editions():
    editions = []
    f_editions = open("politifact_editions.txt", "r")
    for edition in f_editions:
        editions.append(edition)

def parse_statement_of_html_tags(statement):
    if statement.find("<p>") != -1:
        statement = statement.replace("<p>", "")
    if statement.find("</p>") != -1:
        statement = statement.replace("</p>", "")
    if statement.find("<div>") != -1:
        statement = statement.replace("<div>", "")
    if statement.find("&nbsp;") != -1:
        statement = statement.replace("&nbsp;", "")
    if statement.find("</div>") != -1:
        statement = statement.replace("</div>", "")
    if statement.find("&quot;") != -1:
        statement = statement.replace("&quot;", "\"")
    if statement.find("&#39;") != -1:
        statement = statement.replace("&#39;", "\'")
    if statement.find("&lsquo;") != -1:
        statement = statement.replace("&lsquo;", "\'")
    if statement.find("&lsquo;") != -1:
        statement = statement.replace("&rsquo;", "\'")

    return statement


def get_statements_by_date(edition, count):
    if count < 1:
        count = 1
    extension = (edition+"/json/?n="+str(count))

    r = requests.get(base_url+extension)
    json_ = r.json()
    for i in range(count):
        st = json_[i]["statement"]
        st = parse_statement_of_html_tags(st)
        print(str(i)+"::"+ st)
        view_features_in_statement(st)



    """
    statement.replace("<p>", "")
    statement.replace("</p>", "")
    statement.replace("\n", " ")
    statement.replace("<div>&nbsp;</div>", " ")
    statement.replace("&#39;", "\'")
    statement.replace("&quot;", "\"")
    statement.replace("&lsquo;", "\'")
    statement.replace("&rsquo;", "\'")
    """


def view_features_in_statement(statement):
    nl = StatementNatLangProcessor()
    print(nl.show_features_in(statement))


get_statements_by_date("truth-o-meter", 20)


"""
class PolitiFactStatement(Statement):
    def __init__(self):
        super(PolitiFactStatement, self).__init__(None, None, "PolitiFact", None)

"""


