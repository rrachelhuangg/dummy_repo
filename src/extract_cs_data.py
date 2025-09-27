from firecrawl import Firecrawl
import random
import json

firecrawl = Firecrawl(api_key='fc-71d8f0b5d1f344419cde5d315c57a9ca')

cs_prof_links = [{"https://www.cs.wm.edu/~ppeers/publications.php?sort=year":0}, 
{"https://ojcchar.github.io/publications/":0},
{"https://www.cs.wm.edu/~dmitry/publications/":0},
{"https://lindagaw.github.io/publications.html":0},
{"https://www.cs.wm.edu/~smherwig/research.html":0},
{"https://www.cs.wm.edu/%7Ekemper/publication.html":0},
{"https://www.cs.wm.edu/~liqun/paperc.html":0},
{"https://sidilu.org/":0},
{"https://www.cs.wm.edu/~wm/mao_publications.html":0},
{"https://antoniomastropaolo.com/publications/":0},
{"https://www.adwaitnadkarni.com/publications/":0},
{"https://www.cs.wm.edu/~denys/publications.html":0},
{"https://www.cs.wm.edu/~bren/pub.html":0},
{"https://jren73.github.io/publications/":0},
{"https://huajieshao.github.io/publication.html":0},
{"https://www.cs.wm.edu/~andreas/publications/":0},
{"https://sarchlab.org/syifan/publication":0},
{"https://treywoodlief.com/publications/":0},
{"https://yaz91.github.io/publications/":0},
{"https://zjanice.github.io/publication.html":0},
{"https://gang-zhou.com/publications/":0}]

count = 0
selected_links = []
while count < 5:
    select = random.randint(0, len(cs_prof_links)-1)
    check = ""
    for entry in cs_prof_links[select]:
        check = entry
        break
    print("CHECK: ", check)
    if cs_prof_links[select][check]==0:
        cs_prof_links[select][check]=1
        count += 1
        response = firecrawl.crawl(check,
            limit=1,
            scrape_options={
                'formats': [
                    'links',
                ],
                'proxy': 'auto',
                'maxAge': 600000,
                'onlyMainContent': True,
                'prompt':'Extract all of the links from this page.'
            }
        )
        prof_links = []
        for doc in response.data:
            for link in doc.links:
                if '.pdf' in link:
                    if len(prof_links) >=5:
                        break
                    else:
                        prof_links += [link]
        selected_links += prof_links

print("SELECTED LINKS: ", selected_links)

schema = {
    "type": "object",
    "properties": {"title": {"type":"string"}, "description": {"type": "string"}},
    "required": ["description"],
}

overall_cs_data = {}

for link in selected_links:
    res = firecrawl.extract(
        urls=[link],
        prompt="Extract the page title and description.",
        schema=schema,
    )
    data = res.data["description"]
    print("DATA: ", data)
    overall_cs_data[link] = data

with open("cs_data.json", "w") as file:
    json.dump(overall_cs_data, file, indent=4)


