from flask import Flask, jsonify, render_template
import json
import requests
from google.transit import gtfs_realtime_pb2
from google.protobuf.json_format import MessageToDict

app = Flask(__name__)

# Load agencies
with open("agencies.json") as f:
    AGENCIES = json.load(f)
def fetch_gtfs_rt(url, api_key=None):
    headers = {}
    if api_key:
        headers["x-api-key"] = api_key

    r = requests.get(url, headers=headers)
    r.raise_for_status()

    feed = gtfs_realtime_pb2.FeedMessage()
    feed.ParseFromString(r.content)

    return MessageToDict(feed, preserving_proto_field_name=True)
@app.route("/")
def map_page():
    return render_template("index.html")

@app.route("/api/transit/gtfs/vehicles/<agency>")
def vehicles(agency):
    if agency not in AGENCIES:
        return jsonify({"error": "unknown agency"}), 404

    cfg = AGENCIES[agency]
    return fetch_gtfs_rt(cfg["vehicle_url"], cfg.get("api_key"))

@app.route("/api/bikes/gbfs")
def gbfs():
    return "<a href='/'> RETURN </>"

if __name__ == "__main__":
    app.run(debug=True, port=5000)