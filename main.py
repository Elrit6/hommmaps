import os, threading, time, yaml
from flask import Flask, flash, render_template, redirect, request, session, url_for

class Main:   
    def __init__(self):
        self.maps = Maps()
        self.server = Server(self, __name__, static_folder="")

class Map:
    def __init__(self, author, comments, humans, votes, name, players, size):
        self.author = author
        self.comments = comments
        self.humans = humans
        self.votes = votes        
        self.name = name
        self.players = players
        self.size = size
    
class Maps:
    def __init__(self):
        self.authorSort, self.nameSort, self.minSort, self.maxSort, self.sizeSort = '', '', 0, 7, "any"
        self.sizes = {1:'S', 2:'M', 3:'L', 4:'XL'} 
        self.load(True) 
        self.sort(self.authorSort,
                  self.nameSort,
                  self.minSort,
                  self.maxSort,
                  self.sizeSort)
        
    def load(self, reset):
        self.mapsDictionary = {}
        mapsDir = "static/maps"
        for folder in os.listdir(mapsDir):
            mapPath = os.path.join(mapsDir, folder, "data.yaml")
            if (os.path.exists(mapPath)):
                with(open(mapPath, "r") as file):
                    data = yaml.safe_load(file.read())
                    self.mapsDictionary.update({folder : Map(
                        data["author"],
                        data["comments"],
                        data["humans"],
                        data["votes"],
                        #data["votes"],
                        folder,
                        data["players"],
                        data["size"],
                        )})
                if(reset):
                    data["comments"] = {}
                    data["votes"] = {}
                    data["commentsList"] = [""]
                    with(open(mapPath, "w") as file):
                        yaml.dump(data, file, default_flow_style=False)
                        
    def safeConvert(self, var, value, varType):
        try:
            return varType(var)
        except(ValueError, TypeError):
            return value
        
    def convertSorts(self):
        self.authorSort = self.safeConvert(self.authorSort, "", str.lower)
        self.nameSort = self.safeConvert(self.nameSort, "", str.lower)    
        self.minSort = self.safeConvert(self.minSort, 0, int)
        self.maxSort = self.safeConvert(self.maxSort, 7, int)
        self.sizeSort = self.safeConvert(self.sizeSort, 0, int)
        return self.authorSort, self.nameSort, self.minSort, self.maxSort, self.sizeSort
    
    def sort(self, authorSort, nameSort, minSort, maxSort, sizeSort):
        self.authorSort, self.nameSort, self.minSort, self.maxSort, self.sizeSort = authorSort, nameSort, minSort, maxSort, sizeSort
        self.convertSorts()
        print(f"search (name='{self.nameSort}' author='{self.authorSort}' min={self.minSort} max={self.maxSort} size={self.sizeSort})")
        self.sortedMaps = []
        self.mapsHtml = ""
        for i in list(self.mapsDictionary.values()):
            if ((self.minSort <= i.players <= self.maxSort) and (i.size == self.sizeSort or self.sizeSort == 0) and
            (i.name.lower() == self.nameSort or not self.nameSort) and (i.author.lower() == self.authorSort or not self.authorSort)):
                i.file = i.name.replace(" ", "") + ".mp2"
                self.sortedMaps.append(i)
      
class Server(Flask):
    def __init__(self, main, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.accounts = {"user" : "password",
                         "user2" : "password2",
                         "user3" : "password3"}
        self.alert = None
        self.config["SESSION_TYPE"] = "filesystem"
        self.secret_key = "ui34j9ufvegcn"
        self.loginResult = ""
        self.setupRoutes(main)

    def commentCheck(self, comments, user):
        return bool(user and session.get("logged_in") and user not in comments)

    def voteCheck(self, votes, user, vote):
        if not user or not session.get("logged_in"):
            return False
        return user not in votes or votes[user] != vote
         
    def mapVote(self, main, vote, mapName, user):
        mapp = main.maps.mapsDictionary.get(mapName)
        mapp.votes[user] = vote
        print(mapp.votes)
        print(f"{user} voted on {mapName} with ({vote})")
        
    def setupRoutes(self, main):
        @self.route("/", methods=["GET", "POST"])
        def home():
            self.alert = None
            if "user" in session: user = session["user"]
            else: user = None
            return render_template("home.html",
                alert = self.alert,
                author = main.maps.authorSort,
                sortedMaps = main.maps.sortedMaps,
                totalMaps = len(main.maps.sortedMaps),
                user = user)
        
        @self.route("/settings", methods=["GET", "POST"])
        def settings():
            if(request.method == "POST"):
                username = request.form.get("username")
                password = request.form.get("password")
                if(username in self.accounts and password == self.accounts[username]):
                    session["logged_in"] = True
                    session["user"] = username
                    session["login_result"] = "Logged in"
                    return redirect(url_for("settings"))
                else:
                    session["login_result"] = "wrong username" if(username not in self.accounts) else "wrong password"
                return redirect(url_for("account"))
            self.alert = session.pop("login_result", None)
            return render_template("settings.html",
                alert=self.alert)

        @self.route("/<mapName>", methods=["GET", "POST"])
        def map(mapName):
            if "user" in session: user = session["user"]
            else: user = None
            return render_template("map.html",
                map = main.maps.mapsDictionary[mapName],
                user = user)
        
        @self.route("/<mapName>/comment", methods=["POST"])
        def comment(mapName):
            if(request.method == "POST"):
                mapp = main.maps.mapsDictionary.get(mapName)
                user = session.get("user")
                if(self.commentCheck(list(mapp.comments.keys()), user)):
                    comment = request.form.get("comment")
                    mapp.comments[user] = comment
                    print(mapp.comments)
                    print(f"{comment} on {mapName}")
            return "", 204
        
        @self.route("/<mapName>/upvote", methods=["POST"])
        def upvote(mapName):
            if(request.method == "POST"):
                mapp = main.maps.mapsDictionary.get(mapName)
                user = session.get("user")
                if(self.voteCheck(mapp.votes, user, 1) == True):
                    self.mapVote(main, 1, mapName, user)
            return "", 204
        
        @self.route("/<mapName>/downvote", methods=["POST"])
        def downvote(mapName):
            if (request.method == "POST"):
                mapp = main.maps.mapsDictionary.get(mapName)
                user = session.get("user")
                if (self.voteCheck(mapp.votes, user, -1) == True):
                    self.mapVote(main, -1, mapName, user)
            return "", 204
        
        @self.route("/logout", methods=["GET"])
        def logout():
            if (session["logged_in"] == True):
                session.pop("user", None)
                session["logged_in"] = False
                session["login_result"] = "Logged out"
            else:
                session["login_result"] = "Already logged out"
            return redirect(url_for("settings"))
        
        @self.route("/mapsUpdate", methods=["GET", "POST"])
        def mapsUpdate():
            if (request.method == "POST"):
                main.maps.sort(
                    request.form.get("author"),
                    request.form.get("name"),
                    request.form.get("min"),
                    request.form.get("max"),
                    request.form.get("size"))
            return render_template("maps.html",
                alert = self.alert,
                sortedMaps = main.maps.sortedMaps,
                author = main.maps.authorSort,
                totalMaps = len(main.maps.sortedMaps))
        
        @self.errorhandler(404)
        def notFoundRoute(error):
            return redirect('/'), 404

if (__name__ == "__main__"):
    main = Main()
    main.server.run(port=5001)
