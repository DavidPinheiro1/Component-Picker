#ctrl+alt+shitf+insert para scratch file

import time
from selenium import webdriver
from selenium.webdriver.common.by import By

driver = webdriver.Chrome()

paginas = ["https://www.pcdiga.com/componentes?category=processadores&fabricante=intel&produtos_por_pagina=36",
           "https://www.pcdiga.com/componentes?category=processadores&fabricante=amd&produtos_por_pagina=36"]

url=[]

for paginacao in paginas:
    driver.get(paginacao)

    time.sleep(1)
    try:
        driver.find_element(by=By.CSS_SELECTOR, value=".ch2-btn.ch2-allow-all-btn.ch2-btn-primary.ch2-btn-text-xxs").click()
    except:
        pass

    while True:

        lista = driver.find_elements(by=By.CSS_SELECTOR, value=".grid.justify-between .flex.flex-col.bg-background-off.rounded-r4 ")

        for separated_cpu in lista:
            link = separated_cpu.find_element(by=By.CSS_SELECTOR, value=".relative a").get_property("href")
            url.append(link)


        buttons = driver.find_elements(By.CSS_SELECTOR, value=".flex.items-center.h-full.gap-x-5 .text-primary")

        anterior = False

        if not buttons:
            break

        for button in buttons:
            if "previous" in button.get_attribute("aria-label"):
                anterior = True
            if "next" in button.get_attribute("aria-label"):
                anterior = False
                button.click()



        time.sleep(2)
        print(url)
        print(len(url))

        if anterior:
            break

    file=open("links_cpu.txt", "w")
    for files in url:
        file.write(f"{files}\n")
        print("")

    file.close()

driver.close()