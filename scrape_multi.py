from subprocess import Popen, PIPE
from lxml import etree
from io import StringIO
import traceback
import json

user_agent = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.95 Safari/537.36'

with open("config.json", "r") as f:
    config = f.read()
    config = json.loads(config)

for k, thread in enumerate(config["threads"]):
    print("thread: " + str(k) + "/" + str(len(config["threads"])))

    for page in range(thread["pages"][0], thread["pages"][1]):
        urls = [thread["url1"] + str(page), thread["url2"] + str(page)]
        details_list = [False, True]
        folder = thread["out_folder"]

        print("page: " + str(page) + "/" + str(thread["pages"][1]))

        for j in range(len(urls)):
            try:
                url = urls[j]
                details = details_list[j]

                print("fetching: " + url)

                get = Popen(['curl', '-s', '-A', user_agent, url], stdout=PIPE)
                result = get.stdout.read().decode('utf8')

                tree = etree.parse(StringIO(result), etree.HTMLParser())
                # divs = tree.xpath('//div')

                str_tree = etree.tostring(tree, encoding='utf8', method='xml')

                str_data = str_tree.decode()

                print("writing file")

                # print(str_tree)
                
                if details:
                    filename = folder + "/page" + str(page) + ".d.txt"
                else:
                    filename = folder + "/page" + str(page) + ".txt"
                with open(filename, "w", encoding="utf-8") as f:
                    f.write(str_data)
            except KeyboardInterrupt:
                quit()
            except:
                traceback.print_exc()
