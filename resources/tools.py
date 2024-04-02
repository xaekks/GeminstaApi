import requests
from bs4 import BeautifulSoup as bs
from fastapi import HTTPException
headers = {'User-Agent': 'Mozilla/5.0 (Linux; Android 11; Infinix X6816C) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.6261.119 Mobile Safari/537.36 OPR/81.1.4292.78446'}


async def zerochan(string: str):
    url = f"https://www.zerochan.net/"+str(string)
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
         soup = bs(response.text, 'html.parser')
         img_tags = soup.find_all('img')
         src_list = [img.get('src') for img in img_tags]
         return src_list
    return False


def run(code, language):
    res = requests.get("https://emkc.org/api/v2/piston/runtimes")
    langs = next((lang for lang in res.json() if lang["language"] == language), None)

    if langs is not None:
        data = {
            "language": language,
            "version": langs["version"],
            "files": [
                {
                    "name": f"file.{langs['aliases'][0] if langs['aliases'] else 'xz'}",
                    "content": code,
                },
            ],
        }

        r = requests.post("https://emkc.org/api/v2/piston/execute", json=data)

        if r.status_code == 200:
            return {
                "language": r.json()["language"],
                "version": r.json()["version"],
                "code": data["files"][0]["content"].strip(),
                "output": r.json()["run"]["output"].strip()
            }
        else:
            raise HTTPException(status_code=r.status_code, detail=f"Status Text: {r.reason}")
    else:
        raise HTTPException(status_code=404, detail="Error: language is not found.")
        

def get_urbandict(word, max=10):
    response = requests.get(f"http://api.urbandictionary.com/v0/define?term={word}")
    if response.status_code == 200:
        data = response.json()
        z = []
        for x in data["list"]:
            a = {}
            a["count"] = x["thumbs_up"] - x["thumbs_down"]
            a["data"] = x
            z.append(a)
        
        z = z[:max]
        
        def hhh(e):
            return e["count"]
        
        z.sort(key=hhh)
        z.reverse()
        
        results = []
        
        for i in z:
            ndict = {}
            ndict["definition"] = i["data"]["definition"]
            ndict["example"] = i["data"]["example"]
            results.append(ndict)
        
        json_data = {}
        json_data["success"] = True
        json_data["results"] = results
        return json_data
    else:
        return {"success": False, "error": "Failed to fetch data"}

def translate_text(source_text, target_lang):
    response = requests.get(
        "https://translate.googleapis.com/translate_a/single",
        params={
            "client": "gtx",
            "sl": "auto",
            "tl": target_lang,
            "dt": "t",
            "q": source_text,
        },
    )
    if response.status_code == 200:
        translation = response.json()[0][0][0]
        return translation
    else:
        return {"success": False, "error": "Failed to fetch data"}