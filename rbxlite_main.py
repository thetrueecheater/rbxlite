import datetime
import requests

class Account:
    def __init__(self, cookie: str):
        self.cookie = cookie
        self.xcsrf_token = None
        self._authenticate()
    
    def _authenticate(self):
        rq1 = requests.post("https://auth.roblox.com/v2/logout", headers={
            "Content-Type": "application/json",
            "Cookie": f".ROBLOSECURITY={self.cookie}"
        })
        
        if rq1.status_code == 403:
            self.xcsrf_token = rq1.headers["x-csrf-token"]
        elif rq1.status_code == 401:
            logger("error", "Unauthorized.")
            exit()
        else:
            self.xcsrf_token = rq1.headers["x-csrf-token"]
    
    def changeDisplayName(self, new_display: str):
        if not self.xcsrf_token:
            self._authenticate()
        
        user_id = self.getAuthenticatedInfo()

        rq1 = requests.patch(f"https://users.roblox.com/v1/users/{user_id}/display-names", headers={
            "Content-Type": "application/json",
            "Cookie": f".ROBLOSECURITY={self.cookie}",
            "x-csrf-token": self.xcsrf_token
        }, json={
            "newDisplayName": new_display
        })    

        if rq1.status_code == 200:
            logger("info", f"You changed your display name to {new_display} successfully.")
        elif rq1.status_code == 401:
            logger("error", "Unauthorized.")
            exit()
        else:
            logger("warn", f"{rq1.text}")
            exit()

    def changeProfileDesc(self, new_desc: str):
        rq1 = requests.post("https://users.roblox.com/v1/description", headers={
            "Content-Type": "application/json",
            "Cookie": f".ROBLOSECURITY={self.cookie}",
            "x-csrf-token": self.xcsrf_token
        }, json={
            "description": f"{new_desc}"
        })
        if rq1.status_code == 200:
            logger("info", f"Changed description to {new_desc} successfully.")
        elif rq1.status_code == 401:
            logger("error", "Unauthorized.")
            exit()
        else:
            logger("warn", f"{rq1.text}")
            exit()
    
    def changeAccountGender(self, new_gender: str):
        rq1 = requests.post("https://users.roblox.com/v1/gender", headers={
            "Content-Type": "application/json",
            "Cookie": f".ROBLOSECURITY={self.cookie}",
            "x-csrf-token": self.xcsrf_token
        }, json={
            "gender": f"{new_gender}"
        })
        
        if rq1.status_code == 200:
            logger("info", f"Changed gender to {new_gender} successfully.")
        elif rq1.status_code == 401:
            logger("error", "Unauthorized.")
            exit()
        else:
            logger("warn", f"{rq1.text}")
            exit()
    
    def changeBirthdate(self, new_birth: dict, password: str):
        if not password:
            logger("warn", "Password is missing, you must provide your account password to change your birthdate.")
            return

        if not all(k in new_birth for k in ["birthMonth", "birthDay", "birthYear"]):
            logger("warn", "Invalid birthdate format. Must include 'birthMonth', 'birthDay', and 'birthYear'.")
            return

        if not self.xcsrf_token:
            self._authenticate()

        rq1 = requests.post("https://users.roblox.com/v1/birthdate", headers={
            "Content-Type": "application/json",
            "Cookie": f".ROBLOSECURITY={self.cookie}",
            "x-csrf-token": self.xcsrf_token
        }, json={
            "birthMonth": new_birth["birthMonth"],
            "birthDay": new_birth["birthDay"],
            "birthYear": new_birth["birthYear"],
            "password": password
        })

        if rq1.status_code == 200:
            logger("info", "Successfully changed birthdate.")
        elif rq1.status_code == 401:
            logger("error", "Unauthorized.")
            exit()
        else:
            logger("warn", f"{rq1.text}")

    def getCountryCode(self):
        rq1 = requests.get("https://users.roblox.com/v1/users/authenticated/country-code", headers={
            "Content-Type": "application/json",
            "Cookie": f".ROBLOSECURITY={self.cookie}",
            "x-csrf-token": self.xcsrf_token
        })
        
        if rq1.status_code == 200:
            data = rq1.json()
            if "countryCode" in data:
                country = data["countryCode"]
                logger("info", f"Your account country is: {country}")
            else:
                logger("warn", "countryCode not found.")
                exit()
        elif rq1.status_code == 401:
            logger("error", "Unauthorized.")
            exit()
        else:
            logger("warn", f"{rq1.text}")
            exit()
    
    def getProfileDesc(self):
        rq1 = requests.get("https://users.roblox.com/v1/description", headers={
            "Content-Type": "application/json",
            "Cookie": f".ROBLOSECURITY={self.cookie}",
            "x-csrf-token": self.xcsrf_token
        })
        
        if rq1.status_code == 200:
            data = rq1.json()
            if "description" in data:
                logger("info", f"{data["description"]}")
            else:
                logger("warn", "description not found.")
                exit()
        elif rq1.status_code == 401:
            logger("error", "Unauthorized.")
            exit()
        else:
            logger("warn", f"{rq1.text}")
            exit()
    
    def getGender(self):
        rq1 = requests.get("https://users.roblox.com/v1/gender", headers={
            "Content-Type": "application/json",
            "Cookie": f".ROBLOSECURITY={self.cookie}"
        })
        if rq1.status_code == 200:
            data = rq1.json() 
            logger("info", f"Your gender is: {data["gender"]}")
        elif rq1.status_code == 401:
            logger("error", "Unauthorized.")
            exit()
        else:
            logger("warn", f"{rq1.text}")
    
    def getAuthenticatedInfo(self):
        rq1 = requests.get("https://users.roblox.com/v1/users/authenticated", headers={
            "Content-Type": "application/json",
            "Cookie": f".ROBLOSECURITY={self.cookie}"
        })
        if rq1.status_code == 200:
            data = rq1.json()
            return data.get("id") 
        elif rq1.status_code == 401:
            logger("error", "Unauthorized.")
            exit()
        else:
            logger("warn", f"{rq1.text}")
        
def logger(level: str, message: str):
    """Logs messages with detailed timestamps and log levels."""
    now = datetime.datetime.now()
    timestamp = now.strftime("{%H:%M:%S, %d}")
    log_levels = {"error": "ERROR", "warn": "WARNING", "info": "INFO"}
    level_str = log_levels.get(level.lower(), "INFO")
    print(f"{timestamp}~ [{level_str}]: {message}")
