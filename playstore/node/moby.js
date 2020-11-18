

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
        let response = await crawler.getPostTitles(url, 'div.mobList > div.molist > table > tbody > tr > td');
        let list = [];
        for (let i = 0; i < response.length / 3; i++) {
            let game = {
                name: response[i * 3],
                publisher: response[i * 3 + 1],
                category: response[i * 3 + 2],
                pageUrl: url
            };
            list.push(game);
        }
        return list;
    },
    /**
     * list games from all pages by year 
     */
    listGamesRecursive: async (year) => {
        try {
            let list = [];
            if (!year) {
                url = 'https://www.mobygames.com/browse/games/android/list-games/';
            } else {
                url = 'https://www.mobygames.com/browse/games/android/' + year + '/list-games/';
            }
            let plist = await self.listGames(url);
            list = list.concat(plist);
            response = await crawler.getPostHref(url, 'div.mobFooter > a');
            for (let i = 0; i < response.length && i < 3; i++) {
                plist = await self.listGames(response[i]);
                list = list.concat(plist);
            }
            return list;
        } catch (error) {
            throw error;
        }
    }
}