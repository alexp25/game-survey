

// https://www.mobygames.com/browse/games/android/2020/
// https://www.mobygames.com/browse/games/android/2020/list-games/
// https://www.mobygames.com/browse/games/android/2020/offset,25/so,0a/list-games/
// https://www.mobygames.com/browse/games/android/2020/offset,50/so,0a/list-games/

const crawler = require('./crawler');

var self = module.exports = {
    /**
     * list games from page
     */
    listGames: async (url) => {
        let response = await crawler.getPostElements(url, 'div.mobList > div.molist > table > tbody > tr > td');
        let titles = crawler.getPostTitles(response[0], response[1]);
        let hrefs = crawler.getPostHrefAnchor(response[0], response[1]);
        let list = [];
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
        return list;
    },
    /**
     * list games from all pages by year 
     */
    listGamesRecursive: async (year, limitRecursive) => {
        try {
            let list = [];
            if (!year) {
                url = 'https://www.mobygames.com/browse/games/android/list-games/';
            } else {
                url = 'https://www.mobygames.com/browse/games/android/' + year + '/list-games/';
            }
            let plist = await self.listGames(url);
            plist.forEach(el => el.year = year);
            list = list.concat(plist);
            response = await crawler.getPostElements(url, 'div.mobFooter > a');
            let urls = crawler.getPostHref(response[0], response[1]);
            for (let i = 0; i < urls.length; i++) {
                console.log("fetching page: " + i + " of " + urls.length);
                if (limitRecursive) {
                    if (i >= limitRecursive) {
                        break;
                    }
                }
                plist = await self.listGames(urls[i]);
                plist.forEach(el => el.year = year);
                list = list.concat(plist);
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