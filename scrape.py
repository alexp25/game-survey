from subprocess import Popen, PIPE
from lxml import etree
from io import StringIO
import traceback

user_agent = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.95 Safari/537.36'

folder = "./data/metacritic_rts"
details = True

for i in range(19,21):

    # try:

    # url = 'https://www.metacritic.com/browse/games/score/metascore/all/pc/filtered?view=condensed&sort=desc&page=' + str(i)
    # url = 'https://www.metacritic.com/browse/games/score/userscore/all/all/filtered?view=condensed&sort=desc&page=' + str(i)
    # url = 'https://www.metacritic.com/browse/games/genre/metascore/action/pc?view=condensed&page=' + str(i)
    # url = 'https://www.metacritic.com/browse/games/genre/metascore/action/pc?view=detailed&page=' + str(i)

    # url = 'https://www.metacritic.com/browse/games/genre/metascore/first-person/pc?view=condensed&page=' + str(i)
    # url = 'https://www.metacritic.com/browse/games/genre/metascore/first-person/pc?view=detailed&page=' + str(i)

    # url = 'https://www.metacritic.com/browse/games/genre/metascore/racing/pc?view=condensed&page=' + str(i)
    # url = 'https://www.metacritic.com/browse/games/genre/metascore/racing/pc?view=detailed&page=' + str(i)

    # url = 'https://www.metacritic.com/browse/games/genre/metascore/role-playing/pc?view=condensed&page=' + str(i)
    # url = 'https://www.metacritic.com/browse/games/genre/metascore/role-playing/pc?view=detailed&page=' + str(i)

    url = 'https://www.metacritic.com/browse/games/genre/metascore/real-time/pc?view=condensed&page=' + str(i)
    url = 'https://www.metacritic.com/browse/games/genre/metascore/real-time/pc?view=detailed&page=' + str(i)

    # url = 'https://www.metacritic.com/browse/games/genre/metascore/third-person/pc?view=condensed&page=' + str(i)
    # url = 'https://www.metacritic.com/browse/games/genre/metascore/third-person/pc?view=detailed&page=' + str(i)

    # url = 'https://www.metacritic.com/browse/games/genre/metascore/simulation/pc?view=condensed&page=' + str(i)
    # url = 'https://www.metacritic.com/browse/games/genre/metascore/simulation/pc?view=detailed&page=' + str(i)

    # url = 'https://www.metacritic.com/browse/games/genre/metascore/adventure/pc?view=condensed&page=' + str(i)
    # url = 'https://www.metacritic.com/browse/games/genre/metascore/adventure/pc?view=detailed&page=' + str(i)

    print("fetching: " + url)

    get = Popen(['curl', '-s', '-A', user_agent, url], stdout=PIPE)
    result = get.stdout.read().decode('utf8')

    tree = etree.parse(StringIO(result), etree.HTMLParser())
    # divs = tree.xpath('//div')

    str_tree = etree.tostring(tree, encoding='utf8', method='xml')

    str_data = str_tree.decode()

    print("writing file")

    # print(str_tree)
    filename = folder + "/page" + str(i) + ".txt"
    if details:
        filename = folder + "/page" + str(i) + ".d.txt"

    with open(filename, "w", encoding="utf-8") as f:
        f.write(str_data)

    # quit()

    # print(divs)
    # except:
    #     print("exception at index: ", i)
    #     traceback.print_exc()