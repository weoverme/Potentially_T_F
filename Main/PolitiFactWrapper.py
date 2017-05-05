import json, requests
from Main.natural_lang_processor import StatementNatLangProcessor

class PolitiFactStatement:

    def __init__(self, json):
        self.json_ = json
        self.statement_url = self.get_statement_url()
        self.statement = self.get_statement_text()
        self.parse_statement_text()
        self.speaker = self.get_statement_speaker()
        self.features = {} # dictionary for fast and easy searching
        self.get_features()

    def get_statement_text(self):
        return self.json_["statement"]

    def get_statement_speaker(self):
        return self.json_["speaker"]["name_slug"]

    def get_statement_url(self):
        return self.json_["statement_url"]

    def parse_statement_text(self):
        if self.statement.find("<p>") != -1:
            self.statement = self.statement.replace("<p>", "")
        if self.statement.find("</p>") != -1:
            self.statement = self.statement.replace("</p>", "")
        if self.statement.find("<div>") != -1:
            self.statement = self.statement.replace("<div>", "")
        if self.statement.find("&nbsp;") != -1:
            self.statement = self.statement.replace("&nbsp;", "")
        if self.statement.find("</div>") != -1:
            self.statement = self.statement.replace("</div>", "")
        if self.statement.find("&quot;") != -1:
            self.statement = self.statement.replace("&quot;", "\"")
        if self.statement.find("&#39;") != -1:
            self.statement = self.statement.replace("&#39;", "\'")
        if self.statement.find("&lsquo;") != -1:
            self.statement = self.statement.replace("&lsquo;", "\'")
        if self.statement.find("&lsquo;") != -1:
            self.statement = self.statement.replace("&rsquo;", "\'")
        return

    def get_features(self):
        nl = StatementNatLangProcessor()
        tok_list = nl.show_features_in(self.statement)

        # for each feture
        for token in tok_list:
            feature = token[1]
            try:
                # if feature exists in self.feature, do nothing
                if self.features[feature]:
                    pass
            # if feature not in self.features, add feature as key to self.features
            except KeyError:
                self.features[feature] = None # doesn't need to have a meaningful value
        # Force-End the method
        return


class PolitiFactWrapper:

    def __init__(self):
        self.base_url = "http://www.politifact.com/api/statements/"
        self.editions = []
        self.get_editions()
        self.statement_map = {} # k:statement_url, v:Statement object

    def get_editions(self):
        f_ed = open("politifact_editions.txt", "r")
        for ed in f_ed:
            self.editions.append(ed)

    def get_statements_by_date(self, edition, count):
        if count < 1:
            count = 1
        extension = (edition + "/json/?n=" + str(count))

        r = requests.get(self.base_url + extension)
        json_ = r.json()
        for i in range(count): # for each json
            st = PolitiFactStatement(json_[i])
            # dictionary K:statement_url, V:PolitiFactStatement
            self.statement_map[st.statement_url] = st


if __name__ == "__main__":
    PFWrapper = PolitiFactWrapper()
    ed = "truth-o-meter"
    PFWrapper.get_statements_by_date(ed, 5)

