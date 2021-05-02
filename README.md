# AQI-Forcasting

<p align="center">
  <img src="https://github.com/sanjuGoudru/AQI-Forcasting/blob/main/static/AQI_logo.png" >
</p>


## Quickstart
Run the following command in command line
```bash
git clone https://github.com/sanjuGoudru/AQI-Forcasting.git
cd AQI-Forcasting
pip install -r requirements.txt
```


</br></br>
Then run the following command in command line
```bash
python app.py
```
## Deployment
I have done deployment on [Heroku cloud](https://aqi-pred-flask.herokuapp.com/). But one can deploy on any cloud. All the required packages are mentioned in 'requirements.txt' file.
Note: Since for free version of heroku it only allows 500mb slug size. So I couldn't deploy LSTM Forecast part. That part I just tested on local machine. But if you want to do the deployment of it then I recommend to increase slug size and replace the following text in requirements.txt "tensorflow-cpu==2.4.1" by "tensorflow==2.4.1"

## Acknowledgment
The dataset has been obtained from [Kaggle](https://www.kaggle.com/rohanrao/air-quality-data-in-india?select=city_hour.csv)

## Screenshots
<img src="https://github.com/sanjuGoudru/AQI-Forcasting/blob/main/static/1.PNG" >
<img src="https://github.com/sanjuGoudru/AQI-Forcasting/blob/main/static/2.PNG" >
<img src="https://github.com/sanjuGoudru/AQI-Forcasting/blob/main/static/3.PNG" >
<img src="https://github.com/sanjuGoudru/AQI-Forcasting/blob/main/static/4.PNG" >
