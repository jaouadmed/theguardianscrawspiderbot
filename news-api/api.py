from flask import Flask, jsonify, url_for, redirect, request
from flask_pymongo import PyMongo
from flask_restful import Api, Resource


app = Flask(__name__)
app.config["MONGO_DBNAME"] = "news"
app.config["MONGO_URI"] = "mongodb://admin:gJwnjAMtbgG2fCPN@SG-URcluster-30233.servers.mongodirector.com:51180,SG-URcluster-30232.servers.mongodirector.com:51180,SG-URcluster-30234.servers.mongodirector.com:51180/admin?replicaSet=RS-URcluster-0&ssl=true&ssl_cert_reqs=CERT_NONE"
#app.config["MONGO_URI"] = "mongodb://localhost:27017/news"
mongo = PyMongo(app)
APP_URL = "http://127.0.0.1:5000"

#First, create text index on headline and text fields:
#db.news.createIndex( { "headline": "text", "text": "text" } )
#Then, to search:
#db.news.find( { $text: { $search: keyword } } )

class Article(Resource):
    
    def get(self, keyword=None):
        data = []
        if keyword != None:
            articles = mongo.db['news'].find({'$text': { '$search': keyword } })
            
            for article in articles:
                article['id'] = str(article.pop('_id'))
                data.append(article)
            return jsonify({"status": "ok", "data": data})
            
        else:
            articles = mongo.db.news.find().limit(5)
            for article in articles:
                article['id'] = str(article.pop('_id'))
                data.append(article)  
            return jsonify({"response": data})

class Index(Resource):
    def get(self):
        return redirect(url_for("articles"))
    

api = Api(app)
api.add_resource(Index, "/", endpoint="index")
api.add_resource(Article, "/api", endpoint="articles")
api.add_resource(Article, "/api/keyword/<string:keyword>", endpoint="keyword")

if __name__ == "__main__":
    app.run(debug=True)