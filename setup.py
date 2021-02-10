import telebot
import pyowm
from pyowm.commons.enums import SubscriptionTypeEnum
from pyowm.utils.measurables import kelvin_to_celsius

bot = telebot.TeleBot('1677628398:AAEUJIomqlUKMtv0vjLUpIPPKAPmXHkcU0o')

config = {
    'subscription_type': SubscriptionTypeEnum.FREE,
    'language': 'ru',
    'connection': {
        'use_ssl': True,
        'verify_ssl_certs': True,
        'use_proxy': False,
        'timeout_secs': 5
    },
    'proxies': {
        'http': 'http://user:pass@host:port',
        'https': 'socks5://user:pass@host:port'
    }
}
owm = pyowm.OWM('68245f4216b8b31411aa83fed13cc451', config=config)
mgr = owm.weather_manager()


#temp_dict_kelvin = w.temperature()   # a dict in Kelvin units (default when no temperature units provided)
#temp_dict_kelvin['temp_min']
#temp_dict_kelvin['temp_max']
#temp_dict_fahrenheit = w.temperature('fahrenheit')  # a dict in Fahrenheit units
#temp_dict_celsius = w.temperature('celsius')  # guess?


#three_h_forecast = mgr.forecast_at_place(city, '3h')






#print(one_call.forecast_daily[0].temperature('celsius').get('feels_like_day', None))
#print(one_call.forecast_daily[0].temperature('celsius').get('day', None))
#print(one_call.forecast_daily[0].temperature('celsius').get('feels_like_evening', None))
#print(one_call.forecast_daily[0].temperature('celsius').get('feels_like_night', None))
#print(w.detailed_status)
#print(temp_dict_kelvin['temp_min'])
#print(temp_dict_kelvin['temp_max'])


@bot.message_handler(commamds=['start', 'help'])
def send_welcome(message):
    bot.reply_to(message, f'Привет, {message.from_user.first_name}. Я помогу тебе узнать погоду на улице в твоём городе прямо сейчас\nПросто напиши мне название места, где ты живёшь')

@bot.message_handler(content_types=['text'])
def get_text_messages(message):
    city = message
    observation = mgr.weather_at_place(city)
    w = observation.weather
    one_call = mgr.one_call(observation.location.lat, observation.location.lon)
    bot.send_message(message.from_user.id, "В городе " + city + " сейчас " + w.detailed_status + ", скорость ветра: " + str(
        one_call.forecast_hourly[1].wind().get('speed', 0)) + " м/с. \nТемпература на данный момент: " + str(
        kelvin_to_celsius(w.temp['temp'])) + "° по Цельсию.")
    
    bot.send_message(message.from_user.id,"Через 3 часа ожидается температура: " + str(kelvin_to_celsius(one_call.forecast_hourly[3].temp['temp'])))



bot.polling(none_stop=True)