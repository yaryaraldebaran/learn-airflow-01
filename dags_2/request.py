import requests

url = "https://api-football-v1.p.rapidapi.com/v3/timezone"

headers = {
	"X-RapidAPI-Key": "d4d3a173f2msh7f2e9959604e9ebp1b650fjsnb418130cc3e4",
	"X-RapidAPI-Host": "api-football-v1.p.rapidapi.com"
}

response = requests.get(url, headers=headers)

print(response.json())