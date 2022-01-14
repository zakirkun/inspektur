import random

from holehe.localuseragent import ua


async def quora(email, client, out):
    name = "Quora"
    domain = "quora.com"
    method= "register"
    frequent_rate_limit=False

    headers = {
        'User-Agent': random.choice(ua["browsers"]["firefox"]),
        'Accept': 'application/json, text/javascript, */*; q=0.01',
        'Accept-Language': 'fr,fr-FR;q=0.8,en-US;q=0.5,en;q=0.3',
        'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
        'X-Requested-With': 'XMLHttpRequest',
        'Origin': 'https://fr.quora.com',
        'Connection': 'keep-alive',
        'TE': 'Trailers',
    }
    try:
        r = await client.get("https://fr.quora.com", headers=headers)
        revision = r.text.split('revision": "')[1].split('"')[0]
        formkey = r.text.split('formkey": "')[1].split('"')[0]
    except:
        out.append({"name": name,"domain":domain,"method":method,"frequent_rate_limit":frequent_rate_limit,
                    "rate_limit": True,
                    "exists": False,
                    "email_recovery": None,
                    "phone_number": None,
                    "others": None})
        return()

    data = {
        'json': '{"args":[],"kwargs":{"value":"' + str(email) + '"}}',
        'formkey': str(formkey),
        '__hmac': '0XXXXXXxxXDxX',
        '__method': 'validate'
    }

    response = await client.post('https://fr.quora.com/webnode2/server_call_POST', headers=headers, data=data)
    try:
        if 'Un compte a' in response.text:
            out.append({"name": name,"domain":domain,"method":method,"frequent_rate_limit":frequent_rate_limit,
                        "rate_limit": False,
                        "exists": True,
                        "email_recovery": None,
                        "phone_number": None,
                        "others": None})
        else:
            out.append({"name": name,"domain":domain,"method":method,"frequent_rate_limit":frequent_rate_limit,
                        "rate_limit": False,
                        "exists": False,
                        "email_recovery": None,
                        "phone_number": None,
                        "others": None})
    except BaseException:
        out.append({"name": name,"domain":domain,"method":method,"frequent_rate_limit":frequent_rate_limit,
                    "rate_limit": True,
                    "exists": False,
                    "email_recovery": None,
                    "phone_number": None,
                    "others": None})
