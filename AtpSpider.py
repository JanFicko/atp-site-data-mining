import scrapy

class AtpSpider(scrapy.Spider):

    name = "atp_spider"
    allowed_domains = ["atpworldtour.com"]
    start_urls = ["http://www.atpworldtour.com/en/rankings/singles/?rankRange=0-1"]

    activity = []
    player_age = None
    player_height = None
    player_weight = None
    activity_count = 0
    opponent_count = 0

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.download_delay = 0.250

    def parse(self, response):
        if "players" in response.request.url and "player-activity" in response.request.url:

            player_dict = {}

            #player_ranking = response.css("div.player-ranking-position div.data-number::text").extract_first().replace('\r\n', "").strip()

            self.player_age = self.extract_age(response)
            self.player_height = self.extract_height(response)
            self.player_weight = self.extract_weight(response)

            player_dict["p1_age"] = self.player_age
            player_dict["p1_birthplace"] = self.extract_birthplace(response)
            player_dict["p1_main_hand"] = self.extract_main_hand(response)
            player_dict["p1_backhand"] = self.extract_backhand(response)

            tournaments = response.css("div.activity-tournament-table")
            for i, tournament in enumerate(tournaments):
                player_dict["court_type"] = tournament.css("div.item-details::text").extract()[3].replace('\r\n', "").strip()
                player_dict["court_base"] = tournament.css("div.item-details span.item-value::text").extract()[2].replace('\r\n', "").strip()

                games = tournament.css("table.mega-table tbody tr")
                for j, game in enumerate(games):
                    player_ranking = response.css("div.activity-tournament-caption::text").extract()[i].replace("T", "").replace("-", "0").split(",")[1].split(":")[1].strip()
                    opponent_ranking = game.css("td::text").extract()[1].replace("T", "").replace("-", "0").replace('\r\n', "").strip()

                    if opponent_ranking:
                        player_dict["activity_id"] = self.activity_count
                        self.activity_count += 1

                        player_dict["p1_ranking"] = player_ranking
                        player_dict["p2_ranking"] = opponent_ranking

                        player_dict["ranking_diff"] = self.calculate_ranking_diff(player_ranking, opponent_ranking)
                        player_dict["result"] = game.css("td::text").extract()[5].replace(" ", "").replace('\r\n', "")

                        self.activity.append(player_dict.copy())

                        opponent_overview = game.css("td div.day-table-name a::attr(href)").extract_first()
                        url_opponent_overview = "http://www.atpworldtour.com" + opponent_overview
                        yield scrapy.Request(url_opponent_overview, callback=self.parse)

        elif "players" in response.request.url and "overview" in response.request.url:
            player_dict = self.activity[self.opponent_count]

            player_dict["p2_age"] = self.extract_age(response)
            player_dict["p2_birthplace"] = self.extract_birthplace(response)
            player_dict["p2_main_hand"] = self.extract_main_hand(response)
            player_dict["p2_backhand"] = self.extract_backhand(response)

            player_dict["age_diff"] = self.calculate_age_diff(self.player_age, player_dict["p2_age"])
            player_dict["weight_diff"] = self.calculate_weight_diff(self.player_weight, self.extract_weight(response))
            player_dict["height_diff"] = self.calculate_height_diff(self.player_height, self.extract_height(response))

            self.opponent_count += 1

            yield player_dict
        else:
            players_pages = response.css("td.player-cell a::attr(href)").extract()
            for player in players_pages:
                player_activity = player.replace("overview", "player-activity?year=2018")
                url_next_player_activity = "http://www.atpworldtour.com" + player_activity
                yield scrapy.Request(url_next_player_activity, callback=self.parse)

    def extract_age(self, response):
        try:
            return response.css("div.table-big-value::text").extract_first().replace('\r\n', "").strip()
        except:
            return None

    def extract_height(self, response):
        try:
            return response.css("span.table-height-cm-wrapper::text").extract_first().replace("(", "").replace(")", "").replace("cm", "")
        except:
            return None

    def extract_weight(self, response):
        try:
            return response.css("span.table-weight-kg-wrapper::text").extract_first().replace("(", "").replace(")", "").replace("kg", "")
        except:
            return None

    def extract_birthplace(self, response):
        try:
            birthplace = response.css("div.table-value::text").extract_first().replace(" ", "").replace('\r\n', "").split(",")
            return birthplace[len(birthplace) - 1]
        except:
            return None

    def extract_main_hand(self, response):
        try:
            handed = response.css("div.table-value::text").extract()[2].replace('\r\n', "").split(",")
            return handed[0].strip()
        except:
            return None

    def extract_backhand(self, response):
        try:
            handed = response.css("div.table-value::text").extract()[2].replace('\r\n', "").split(",")
            return handed[1].strip()
        except:
            return None

    def calculate_ranking_diff(self, p1_rang, p2_rang):
        try:
            p1_rang = int(p1_rang)
            p2_rang = int(p2_rang)
            if p2_rang == "-":
                return 2000 - p1_rang
            elif p1_rang > p2_rang:
                return p1_rang - p2_rang
            else:
                return p2_rang - p1_rang
        except:
            return None

    def calculate_height_diff(self, p1_height, p2_height):
        try:
            p1_height = int(p1_height)
            p2_height = int(p2_height)
            if p1_height > p2_height:
                return p1_height - p2_height
            else:
                return p2_height - p1_height
        except:
            return None

    def calculate_weight_diff(self, p1_weight, p2_weight):
        try:
            p1_weight = int(p1_weight)
            p2_weight = int(p2_weight)
            if p1_weight > p2_weight:
                return p1_weight - p2_weight
            else:
                return p2_weight - p1_weight
        except:
            return None

    def calculate_age_diff(self, p1_age, p2_age):
        try:
            p1_age = int(p1_age)
            p2_age = int(p2_age)
            if p1_age > p2_age:
                return p1_age - p2_age
            else:
                return p2_age - p1_age
        except:
            return None