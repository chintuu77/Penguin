from flask import Flask,render_template,url_for,request,redirect
import numpy as np
import pandas as pd
import joblib
import pickle


app = Flask(__name__)

model = joblib.load('classifier.pkl')
onehot = joblib.load('OneHotee.joblib')


@app.route('/')
@app.route('/main')
def main():
	return render_template('main.html')

@app.route('/predict',methods=['POST'])
def predict():
	int_features =[[x for x in request.form.values()]]
	c = ["island","sex","culmen_length_mm","culmen_depth_mm","flipper_length_mm","body_mass_g"]
	df = pd.DataFrame(int_features,columns=c)
	print("#"*20)
	print(df)	
	l = onehot.transform(df.iloc[:,0:2])
	print("&"*20)
	print(l)
	c = onehot.get_feature_names_out()
	t = pd.DataFrame(l,columns=c)
	l2 = df.iloc[:,2:]
	final =pd.concat([l2,t],axis=1)
	print("$"*30)

	print(final)
	result = model.predict(final)
	print("The Result is :",result)


	print(int_features)

	return render_template("main.html",prediction_text="Penguin Specie is : {}".format(result))


if __name__ == "__main__":
	app.debug=True
	app.run(host = '0.0.0.0',port =8000,debug=True)
