

// https://www.mobygames.com/browse/games/android/2020/
// https://www.mobygames.com/browse/games/android/2020/list-games/
// https://www.mobygames.com/browse/games/android/2020/offset,25/so,0a/list-games/
// https://www.mobygames.com/browse/games/android/2020/offset,50/so,0a/list-games/

const crawler = require('./crawler');
const utils = require('./utils');

var self = module.exports = {
    /**
     * list games from page
     */
    listGames: async (url, year) => {
        let page = await crawler.getPageHTML(url);
        let response = crawler.getPostElementsCore(page, 'div.mobList > div.molist > table > tbody > tr > td');
        let titles = crawler.getPostTitles(response[0], response[1]);
        let hrefs = crawler.getPostHrefAnchor(response[0], response[1]);

        response = crawler.getPostElementsCore(page, 'div.mobFooter > a');
        let pageLinks = crawler.getPostHref(response[0], response[1]);

        let list = [];
        if (!year) {
            for (let i = 0; i < titles.length / 4; i++) {
                let game = {
                    name: titles[i * 4],
                    year: titles[i * 4 + 1],
                    publisher: titles[i * 4 + 2],
                    category: titles[i * 4 + 3],
                    pageUrl: url,
                    url: hrefs[i * 4]
                };
                list.push(game);
            }
        } else {
            for (let i = 0; i < titles.length / 3; i++) {
                let game = {
                    name: titles[i * 3],
                    publisher: titles[i * 3 + 1],
                    category: titles[i * 3 + 2],
                    pageUrl: url,
                    url: hrefs[i * 3]
                };
                list.push(game);
            }
        }
        return [list, pageLinks];
    },
    /**
     * list games from all pages by year 
     */
    listGamesRecursive: async (year, platform, limitRecursive) => {
        try {
            let list = [];
            if (!year) {
                url = 'https://www.mobygames.com/browse/games/' + platform + '/list-games/';
            } else {
                url = 'https://www.mobygames.com/browse/games/' + platform + '/' + year + '/list-games/';
            }
            let plist = await self.listGames(url, year);
            let urls = plist[1];
            plist = plist[0];
            if (year) {
                plist.forEach(el => el.year = year);
            }
            list = list.concat(plist);
            console.log(list);

            await utils.wait(2000);

            for (let i = 0; i < urls.length; i++) {
                console.log("fetching page: " + i + " of " + urls.length);
                if (limitRecursive) {
                    if (i >= limitRecursive) {
                        break;
                    }
                }
                try {
                    plist = await self.listGames(urls[i], year);
                    let urls1 = plist[1];
                    if (urls1[urls1.length - 1] !== urls[urls.length - 1]) {
                        urls.push(urls1[urls1.length - 1]);
                    }

                    plist = plist[0];
                    if (year) {
                        plist.forEach(el => el.year = year);
                    }
                    list = list.concat(plist);
                    await utils.wait(2000);
                } catch (err) {
                    console.error(err);
                    break;
                }
            }
            return list;
        } catch (error) {
            throw error;
        }
    },

    /**
     *  'Published by',
        'Big Fish Games, Inc',
        'Developed by',
        'funkitron, Inc.',
        'Released',
        'Feb 10, 2020',
        'Official Site',
        'Cascade Gem & Jewel Adventure',
        'Also For',
        'iPad, iPhone | Combined View' 
     */
    getGameDetails: async (url) => {
        try {
            response = await crawler.getPostElements(url, 'div[id=coreGameRelease] > div');
            let text = crawler.getPostTitles(response[0], response[1]);
            return text;
        } catch (error) {
            throw error;
        }
    },
    parseGameDetails: (detailsList) => {
        let details = {
            releaseDate: 0,
            releaseYear: 0
        };
        for (let i = 0; i < detailsList.length; i++) {
            if (detailsList[i] == "Released") {
                details.releaseDate = detailsList[i + 1];
                var year = details.releaseDate.split(",");
                year = year[year.length - 1].replace(" ", "");
                details.releaseYear = Number.parseInt(year);
            }
        }
        return details;
    }
}