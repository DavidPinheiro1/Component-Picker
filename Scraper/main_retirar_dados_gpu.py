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

file=open("links_gpu.txt", "r")
links=file.read().split("\n")
file.close()


for url in links:

    try:

        if url != "":
            driver.get(url)
            print(url)

            time.sleep(10)
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

            specs2 = driver.find_elements(by=By.CSS_SELECTOR,
                                         value=".reset-defaults.cms-product-table ul li ul li ul li")


            preco = driver.find_element(by=By.CSS_SELECTOR,
                                 value=".text-primary.text-2xl.font-black").text

            nome_raw = driver.find_element(by=By.CSS_SELECTOR, value=".grid.gap-6 h1").text.split(" ")
            nome = ""
            for nomebreak in nome_raw:

                if "GDDR" in nomebreak.lower():
                    break
                nome += f"{nomebreak} "

            nome = nome.strip()

            print(nome)
            print(preco)
            memoria = ""
            cuda = ""
            directX = ""
            openGL = ""


            for caracteristicas in specs:
                if "Memória:" in caracteristicas.text:
                    memoria = caracteristicas.text
                if "Núcleos CUDA" in caracteristicas.text or "Stream Processors:" in caracteristicas.text:
                    cuda = caracteristicas.text
                if "directx" in caracteristicas.text.lower():
                    directX = caracteristicas.text
                if "opengl" in caracteristicas.text.lower():
                    openGL = caracteristicas.text

            print(memoria)
            print(cuda)
            print(directX)
            print(openGL)
            print("")

            cursor.execute(f''' INSERT INTO "graficas" VALUES("{nome}", "{preco}", "{memoria}", "{cuda}", "{directX}", "{openGL}", "{imgnome}", "{id}","{url}")''')

            conn.commit()

            caract = f' "{nome}", "{preco}", "{memoria}", "{cuda}", "{directX}", "{openGL}", "{imgnome}", "{id}","{url}" '
            todos = ""

            #ver se existe primeiro o ficheiro
            if not "gpu_caracteristicas.txt" in os.listdir():
                with open("gpu_caracteristicas.txt", "w") as file:
                    pass
            with open("gpu_caracteristicas.txt", "r") as file:
                todos = file.read()
            todos+=f"\n{caract}"
            with open("gpu_caracteristicas.txt", "w") as file:
                file.write(todos)
            print("")

    except Exception as e:
        print(e)

driver.close()