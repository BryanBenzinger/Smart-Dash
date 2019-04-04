import smartcar
from flask import render_template
from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

CLIENT_ID = '4c472273-b379-4191-bbe0-cdce0684de6c'
CLIENT_SECRET = '8e53b666-3b91-4bde-b9b9-75675500dbb0'
db = {'access': ''}

client = smartcar.AuthClient(
	client_id = CLIENT_ID,
	client_secret = CLIENT_SECRET,
	redirect_uri = 'http://localhost:5000/callback',
	scope = ['read_vehicle_info', 'read_location', 'control_security','read_odometer'],
	test_mode = True
	)

@app.route('/', methods=['GET'])
def index():
	auth_url = client.get_auth_url(force = True)
	link = {'auth': auth_url}
	return render_template('index.html', link=link)
@app.route('/callback', methods = ['GET'])
def callback():
	code = request.args.get('code')
	db['access'] = client.exchange_code(code)
	return render_template('callBack.html')

@app.route('/vehicle', methods = ['GET'])
def vehicle():
		vehicle_ids = smartcar.get_vehicle_ids(db['access']['access_token'])['vehicles']
		
		vehicle = smartcar.Vehicle(vehicle_ids[0], db['access']['access_token'], 'imperial')
		
		odometer = vehicle.odometer()
		miles = int(odometer["data"]["distance"])
		
		oilChange = miles;
		while(oilChange > 6000):
			oilChange -= 6000
		tireRotation = int(oilChange)
		
		info = vehicle.info()
		loc = vehicle.location()
		#import pdb; pdb.set_trace()
		lat = loc["data"]["latitude"]
		lng = loc["data"]["longitude"]
		diction = {'RX':462, 'X5':435, 'Wrangler':369, 'A8':445}
		
		make = info["make"]
		model = info["model"]
		year = info["year"]
		tankMiles = diction[model]
		
		gasMoney = int(((miles/tankMiles) * 2.5))
	
		return render_template('vehicleInfo.html',miles=miles,tireRotation=tireRotation,gasMoney=gasMoney,make=make,model=model,year=year, lat=lat, lng=lng)
if __name__ == '__main__':
    app.run(port=5000)