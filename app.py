import flask
from flask import jsonify, request
from flask.views import MethodView
from models import Ads, Session



app = flask.Flask(__name__)

@app.before_request
def before_request():
    session = Session()
    request.session = session
    
    
class AdsView(MethodView):
    
    def get(self, id=None):
        if id is None:
            ads = request.session.query(Ads).all()
            return jsonify([ad.dict for ad in ads])
        else:
            ads_id = request.session.get(Ads, id)
        if ads_id is None:
            return jsonify({"error": "ID not found"}), 404
        else:
            return jsonify(ads_id.dict)
    
    def post(self):
        new_ads = Ads(**request.json)
        request.session.add(new_ads)
        request.session.commit()
        return jsonify(new_ads.dict)
    
    def delete(self, id):
        ad = request.session.query(Ads).get(id)
        if ad is None:
            return jsonify({"error": "Ad not found"}), 404
        request.session.delete(ad)
        request.session.commit()
        return jsonify({"status": "deleted"})


ads_view = AdsView.as_view('ads_view')
app.add_url_rule('/ads/', view_func=ads_view, methods=['POST'])   
app.add_url_rule('/ads/<id>/', view_func=ads_view, methods=['GET', 'DELETE'])   
app.add_url_rule('/ads/', view_func=ads_view, methods=['GET'])


if __name__ == '__main__':
    app.run(debug=True)
    
    