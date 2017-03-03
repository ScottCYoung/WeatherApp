import requests
import bs4
import collections

#creates a Weather Report class that is a named tuple
WeatherReport = collections.namedtuple('WeatherReport',
                                       'temperature, condition, scale, location')


def main():
    print_the_header()

    #Get zipcode
    code = input("Enter your zipcode (44857)")

    html = get_html_from_web(code)
    report = get_weather_from_html(html)

    print('The temp in {} is {} {} and {}'.format(report.location,
                                                  report.temperature,
                                                  report.scale,
                                                  report.condition))

def get_html_from_web(zipcode):
    url = 'https://www.wunderground.com/cgi-bin/findweather/getForecast?query={}'.format(zipcode)
    response = requests.get(url)
    return response.text

def print_the_header():
    print("---------------------------")
    print("        WeatherApp")
    print("---------------------------")
    print()


def cleanup_text(text : str):
    if not text:
        return text
    text = text.strip()
    return text

def find_city_and_state_from_loc(loc : str):
    parts = loc.split('\n')
    return parts[0].strip()


def get_weather_from_html(html):
    #cityCss = 'div#location h1'
    #weatherConditionCss = 'div#curCond span.wx-value'
    #weatherTempCss= 'div#curTemp span.wx-data span.wx-value'
    #weatherScaleCss = 'div#curTemp span.wx-data space.wx-unit'

    #parsing text to html parser
    soup = bs4.BeautifulSoup(html,'html.parser')

    loc = soup.find(id='location').find('h1').get_text()
    condition = soup.find(id='curCond').find(class_='wx-value').get_text()
    temp = soup.find(id='curTemp').find(class_='wx-data').find(class_='wx-value').get_text()
    scale = soup.find(id='curTemp').find(class_='wx-unit').get_text()

    loc = cleanup_text(loc)
    loc = find_city_and_state_from_loc(loc)


    report = WeatherReport(temperature=temp,scale=scale,location=loc,condition=condition)
    return report
    #return(condition, temp, scale, loc)


if __name__ == '__main__':
    main()

