# -*- coding: utf-8 -*-
from selenium import webdriver
import csv

driver = webdriver.Firefox()

#сначала получаем всы ссылки на курсы из раздела
def get_links(url):
    driver.get(url)
    course_links = []
    total_pages = driver.find_elements_by_xpath('//ul[@class = "pagination__ul"]//a')
    last_page = int(total_pages[-2].text)

    for n in range(last_page):
        courses = driver.find_elements_by_xpath('//article')
        for z in courses:
            if z.get_attribute("title") != 'Available for CourseHunters subscribers only':  #проверяем, что курс уже доступен для просмотра
                course_links.append(z.find_element_by_xpath('.//a').get_attribute("href"))
        if len(driver.find_elements_by_xpath("//a[@rel='next']")) > 0:
            driver.find_element_by_xpath("//a[@rel='next']").click()
    return course_links

links = get_links('https://coursehunters.net/testirovanie-quality-assurance-qa')


#в каждом уроке находим названия урока, длитеольность и ссылку, и пишем все в csv
def list_of_lessons(course_url):
    driver.get(course_url)
    driver.find_element_by_css_selector('span.lessons-list__more').click()
    lessons = driver.find_elements_by_css_selector('li.lessons-list__li')
    course_name = driver.find_element_by_tag_name('h1').text[:-13]
    for l in lessons:
        title = l.find_element_by_xpath(".//span[@itemprop='name']").text
        duration = l.find_element_by_xpath(".//em[@itemprop='duration']").text
        url = l.find_element_by_xpath(".//link[@itemprop='url']").get_attribute("href")
        row = [course_name, title, duration, url]
        with open('output.csv', 'a', newline='') as csvfile:
            filewriter = csv.writer(csvfile, delimiter=',')
            filewriter.writerow(row)
    print("Added " + course_name)

for l in links:
    list_of_lessons(l)

