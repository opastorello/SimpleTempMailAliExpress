import tempmail
import random
import string
import time
import requests
from os import system
from bs4 import BeautifulSoup

def main():
    get_domains = tempmail.domains()
    list_domains = list()

    for c in range(len(get_domains)):
        list_domains.append(get_domains[c].get('domain'))

    email = str(random.randint(111111111111,999999999999)) + "@" + list_domains[int(0)]
    senha = ''.join([random.choice(string.ascii_lowercase + string.digits) for _ in range(11)])

    assunto_email = 'Seu código de verificação AliExpress'
    class_nome = 'code'

    print("E-mail: " + email)
    print("Senha: " + senha)

    code = tempMail(email, senha, assunto_email, class_nome)

    print("Seu código de verificação: " + code)

def tempMail(email, senha, assunto_email, class_nome):
    my_mail = tempmail.TempMail(email, senha)

    try:
        account = my_mail.generate()

    except tempmail.GenerateError as error:
        print(f"{error}, reiniciando sistema de e-mail temporário...")
        input("Pressione Enter para reiniciar.")
        system("cls")
        main()

    else:
        inbox_mails = my_mail.get_messages()

        while True:
            new_mail = my_mail.get_messages()

            if len(new_mail) > len(inbox_mails):
 
                header = {
                    'authority': 'api.mail.tm',
                    'sec-ch-ua': '" Not A;Brand";v="99", "Chromium";v="90", "Google Chrome";v="90"',
                    'accept': 'application/json, text/plain, */*',
                    'authorization': 'Bearer '+my_mail._token,
                    'sec-ch-ua-mobile': '?0',
                    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.212 Safari/537.36',
                    'origin': 'https://mail.tm',
                    'sec-fetch-site': 'same-site',
                    'sec-fetch-mode': 'cors',
                    'sec-fetch-dest': 'empty',
                    'referer': 'https://mail.tm/',
                    'accept-language': 'vi-VN,vi;q=0.9,fr-FR;q=0.8,fr;q=0.7,en-US;q=0.6,en;q=0.5'
                }

                html = requests.get("https://api.mail.tm/messages/" + new_mail[0]["id"], headers=header)
                
                if assunto_email in html.json()["subject"]:
                    soup = BeautifulSoup(html.json()["html"][0], "html.parser")
                    code = soup.find(class_=class_nome).text.strip()
                    return code
                    break

                inbox_mails = new_mail
            time.sleep(5)

system("cls")
main()