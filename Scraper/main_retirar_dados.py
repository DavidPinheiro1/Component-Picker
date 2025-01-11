#ctrl+alt+shitf+insert para scratch file
import os
import time
import random
from urllib.request import Request, urlopen

from selenium import webdriver
from selenium.webdriver.common.by import By
import sqlite3

path = "C:\\Users\\David Pinheiro\\Desktop\\Scraper\\IMAGENS"

conn = sqlite3.connect("Componentes.db")
cursor = conn.cursor()

driver = webdriver.Chrome()

file=open("links_cpu.txt", "r")
links=file.read().split("\n")
file.close()



for url in links:

    try:

        if url != "":
            driver.get(url)
            print(url)

            time.sleep(3)
            # cookies
            try:
                driver.find_element(by=By.CSS_SELECTOR,
                                    value=".ch2-btn.ch2-allow-all-btn.ch2-btn-primary.ch2-btn-text-xxs").click()
            except:
                pass

            driver.execute_script("window.scrollTo(0,document.body.scrollHeight)")

            try:
                driver.find_element(by=By.CSS_SELECTOR,
                                    value=".z-1.base-container.py-5.bg-background.pb-28.flex-grow .text-9xl.font-bold.text-primary")
                continue
            except:
                pass

            url_go = False
            try:
                urlimage = driver.find_elements(By.CSS_SELECTOR,
                                     value=".image-container img")[0]
                url_go=True
            except:
                pass

            if url_go:
                urls=[]

                urls.append(urlimage.get_attribute("src"))

                while True:
                    id = random.randint(0, 9999999)
                    if not os.path.exists(f"{path}\\{id}"):
                        os.mkdir(f"{path}\\{id}")
                        break

                for ur in urls:
                    try:
                        req = Request(ur, headers={'User-Agent': 'Mozzila/5.0'})
                        WD = urlopen(req, timeout=2).read()
                        imgnome = id
                        first_lap = False
                        while True:
                            if first_lap:
                                imgnome= random.randint(0, 9999999)
                            first_lap=True
                            if not f"{imgnome}.png" in os.listdir(f"{path}\\{id}"):
                                with open(f"{path}\\{id}\\{imgnome}.png", "wb") as f:
                                    f.write(WD)
                                    break
                    except Exception as e:
                        print(e)


            specs = driver.find_elements(by=By.CSS_SELECTOR,
                                 value=".reset-defaults.cms-product-table ul li")

            preco = driver.find_element(by=By.CSS_SELECTOR,
                                 value=".text-primary.text-2xl.font-black").text

            nome_raw = driver.find_element(by=By.CSS_SELECTOR, value=".grid.gap-6 h1").text.split(" ")
            nome = ""
            for nomebreak in nome_raw:
                if "Intel" in nomebreak.lower():
                    continue

                if "-core" in nomebreak.lower():
                    break
                nome += f"{nomebreak} "

            nome = nome.strip()

            print(nome)
            print(preco)
            socket = ""
            freq_base = ""
            freq_boost = ""
            nucleos = ""
            threads = ""
            tdp = ""
            cooler = ""



            for caracteristicas in specs:
                if "socket" in caracteristicas.text.lower():
                    socket = caracteristicas.text
                if "frequência base" in caracteristicas.text.lower() or "clock base" in caracteristicas.text.lower() or "Clock básico" in caracteristicas.text:
                    freq_base = caracteristicas.text
                if "frequência turbo" in caracteristicas.text.lower() or "clock de max boost" in caracteristicas.text.lower():
                    freq_boost = caracteristicas.text
                if "número de núcleos:" in caracteristicas.text.lower() or "número núcleos" in caracteristicas.text.lower() or "Nº de Núcleos" in caracteristicas.text:
                    nucleos = caracteristicas.text
                if "Número de threads:" in caracteristicas.text or "Nº de Threads" in caracteristicas.text or "número threads" in caracteristicas.text.lower():
                    threads = caracteristicas.text
                if "tdp" in caracteristicas.text.lower() or "TDP Turbo" in caracteristicas.text:
                    tdp = caracteristicas.text
                if "solução térmica" in caracteristicas.text.lower() or "Cooler Incluído" in caracteristicas.text:
                    cooler = caracteristicas.text

            if socket == "":
                nameskt = driver.find_element(by=By.CSS_SELECTOR, value=".grid.gap-6 h1").text.split(" ")
                for sktbreak in nameskt:
                    if "skt" in sktbreak.lower():
                        socket = sktbreak


            print(socket)
            print(freq_base)
            print(freq_boost)
            print(nucleos)
            print(threads)
            print(tdp)
            print(cooler)
            print(imgnome)
            print(id)
            print("")

            cursor.execute(f''' INSERT INTO "processadores" VALUES("{nome}", "{preco}", "{socket}", "{freq_base}", "{freq_boost}", "{nucleos}", "{threads}", "{tdp}", "{cooler}", "{imgnome}", "{id}","{url}")''')

            conn.commit()

            caract = f' "{nome}", "{preco}", "{socket}", "{freq_base}", "{freq_boost}", "{nucleos}", "{threads}", "{tdp}", "{cooler}", "{imgnome}", "{id}","{url}" '
            todos = ""

            #ver se existe primeiro o ficheiro
            if not "cpu_caracteristicas.txt" in os.listdir():
                with open("cpu_caracteristicas.txt", "w") as file:
                    pass
            #se existir o ficheiro
            with open("cpu_caracteristicas.txt", "r") as file:
                todos = file.read()
            todos+=f"\n{caract}"
            with open("cpu_caracteristicas.txt", "w") as file:
                file.write(todos)
            print("")

    except Exception as e:
        print(e)

driver.close()