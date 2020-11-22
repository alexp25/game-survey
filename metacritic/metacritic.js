


const crawler = require('./crawler');
const utils = require('./utils');

var self = module.exports = {



    /**
     * list games from page
     */
    listGames: async (url) => {

        console.log("list papers from: " + url);
        let response = await crawler.getPageHTML(url);

        let elements = crawler.getPostElementsCore(response, 'table.clamp-list > tbody > tr > td.score > a.metascore_anchor > div');
        let scores = crawler.getPostTitles(elements[0], elements[1]);

        elements = crawler.getPostElementsCore(response, 'table.clamp-list > tbody > tr > td.details > div.collapsed > div.score > a.metascore_anchor > div');
        let userScores = crawler.getPostTitles(elements[0], elements[1]);

        elements = crawler.getPostElementsCore(response, 'table.clamp-list > tbody > tr > td.details > a.title > h3');
        let titles = crawler.getPostTitles(elements[0], elements[1]);

        elements = crawler.getPostElementsCore(response, 'table.clamp-list > tbody > tr > td.details > span');
        let dates = crawler.getPostTitles(elements[0], elements[1]);

        elements = crawler.getPostElementsCore(response, 'div.page_flipper > span.next > a.action');
        let next = crawler.getPostHref(elements[0], elements[1]);

        // console.log(titles);

        let list = [];
        for (let i = 0; i < titles.length; i++) {
            let game = {
                name: titles[i],
                score: scores[i],
                userScore: userScores[i],
                releaseDate: dates[i],
                next: (next.length > 0) ? next[0] : null
            };
            list.push(game);
        }

        return list;
    },

    /**
     * list games from page
     */
    listGamesLegacy: async (url) => {
        return self.listGames(url);
    },

    /**
     * list games from all pages by year 
     */
    listGamesRecursive: async (platform, limitRecursive, useLegacy) => {
        try {
            let list = [];

            let url = 'https://www.metacritic.com/browse/games/release-date/available/' + platform + '/metascore?view=condensed';
            if (useLegacy) {
                url = 'https://www.metacritic.com/browse/games/score/metascore/all/' + platform + '/filtered?view=condensed';
            }

            let plist = useLegacy ? await self.listGamesLegacy(url) : await self.listGames(url);
            list = list.concat(plist);

            console.log(list);
            console.log(list.length);
            console.log("next: ", plist[0].next);

            let nextUrlCore = plist[0].next;
            if (!nextUrlCore) {
                return list;
            }

            // return list;

            let nextUrl = "https://www.metacritic.com" + nextUrlCore;

            await utils.wait(2000);
            
            let i = 0;
            while (true) {

                if (limitRecursive) {
                    if (i >= limitRecursive) {
                        break;
                    }
                }

                if (!nextUrlCore) {
                    console.log("no more pages");
                    break;
                }

                console.log("fetching page: " + i + ": " + nextUrl);

                try {
                    plist = useLegacy ? await self.listGamesLegacy(nextUrl) : await self.listGames(nextUrl);
                    list = list.concat(plist);
                    console.log("next: ", plist[0].next);

                    nextUrlCore = plist[0].next;
                    nextUrl = "https://www.metacritic.com" + nextUrlCore;

                    await utils.wait(2000);

                    i += 1;
                } catch (err) {
                    console.error(err);
                    break;
                }
            }

            for (let item of list) {
                delete item.next;
            }

            return list;
        } catch (error) {
            throw error;
        }
    }
}