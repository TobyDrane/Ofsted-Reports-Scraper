import os
import requests
from bs4 import BeautifulSoup
from tqdm import tqdm
import typer

BASE_OFSTED_URL = "https://reports.ofsted.gov.uk"
data = {"pages": [], "schools": []}

if not os.path.exists("./data"):
    os.makedirs("./data")

def extract_next_page_url(url):
    page = requests.get(url)
    soup = BeautifulSoup(page.content, "html.parser")
    next_button = soup.find("a", class_="pagination__next")

    if next_button:
        return BASE_OFSTED_URL + next_button["href"]


def get_pages(url):
    data["pages"].append(url)
    found_all_pages = False
    with tqdm(
        total=None, desc="Fetching page links: ", unit="page", position=0, leave=True
    ) as pbar:
        while not found_all_pages:
            next_page_url = extract_next_page_url(url)
            if next_page_url:
                data["pages"].append(next_page_url)
                url = next_page_url
                pbar.update(1)  # Increment the progress bar
            else:
                found_all_pages = True


def extract_school_pages(url):
    page = requests.get(url)
    soup = BeautifulSoup(page.content, "html.parser")
    links = soup.select("ul.results-list > li > h3")
    for link in links:
        tag = link.find("a", href=True)
        if tag:
            data["schools"].append(BASE_OFSTED_URL + tag["href"])


def extract_reports(url):
    page = requests.get(url)
    soup = BeautifulSoup(page.content, "html.parser")
    school = soup.find("h1", class_="heading--title").text.strip()
    timeline_ol = soup.find("ol", class_="timeline")
    for li in timeline_ol.find_all("li", class_="timeline__day"):
        # Skip the events with class 'timeline__day--opened'
        if "timeline__day--opened" in li.get("class", []):
            continue

        try:
            # Find the publication link within the <a> tag
            publication_link = li.find("a", class_="publication-link")
            date_span = publication_link.find("span", class_="nonvisual")

            if not date_span:
                raise Exception("No date span found for given element")

            date_text = date_span.text.strip()

            inspection_type = date_text.split(",")[0].strip().replace(" ", "-")
            formatted_date = date_text.split("-")[-1].strip()
            formatted_date = formatted_date.lower().replace(" ", "-")

            result_string = f"{inspection_type.lower()}_{formatted_date}"

            pdf_url = publication_link["href"]

            filename = f"{school}_{result_string}.pdf"
            filename = filename.replace(" ", "-").lower()

            response = requests.get(pdf_url)
            with open("./data/" + filename, "wb") as pdf_file:
                pdf_file.write(response.content)
        except:
            continue


def main(url: str):
    print("FETCH PAGE LINKS")
    get_pages(url)

    print("FETCH SCHOOL LINKS")
    for page in tqdm(
        data["pages"],
        desc="Fetching school links: ",
        unit="page",
        position=0,
        leave=True,
    ):
        extract_school_pages(page)

    print("FETCH REPORTS")
    for school in tqdm(
        data["schools"],
        desc="Fetching school reports: ",
        unit="school",
        position=0,
        leave=True,
    ):

if __name__ == "__main__":
    typer.run(main)