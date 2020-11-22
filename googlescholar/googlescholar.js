
const crawler = require('./crawler');
const utils = require("./utils");

var self = module.exports = {
    /**
     * list games from page
     */
    listPapers: async (url) => {
        console.log("list papers from: " + url);
        let response = await crawler.getPageHTML(url);

        let elements = crawler.getPostElementsCore(response, 'div.gs_a');
        let details = crawler.getPostTitles(elements[0], elements[1]);


        elements = crawler.getPostElementsCore(response, 'h3.gs_rt');
        let titles = crawler.getPostTitles(elements[0], elements[1]);


        elements = crawler.getPostElementsCore(response, 'div[id=gs_n] > center > table > tbody > tr > td > a');
        let hrefs = crawler.getPostHref(response[0], elements[1]);
        hrefs.pop();


        let list = [];
        for (let i = 0; i < titles.length; i++) {
            let paper = {
                name: titles[i],
                details: details[i]
            };
            list.push(paper);
        }

        console.log(list);

        return [list, hrefs];
    },
    /**
     * list games from all pages by year 
     */
    listPapersRecursive: async (keyword, limitRecursive, timeoutBase, startFromItem) => {
        try {
            let list = [];
            let url = "https://scholar.google.com/scholar?start=" + (startFromItem ? startFromItem : "0") + "&q=allintitle:+" + keyword + "&hl=en&as_sdt=0,5";
            let rootUrl = "https://scholar.google.com";
            let res = await self.listPapers(url);
            let urls = res[1];
            let plist = res[0];

            list = list.concat(plist);

            let ms = utils.getTimeoutRandom(timeoutBase);
            console.log("robot waiting: " + ms);
            await utils.wait(ms);

            for (let i = 0; i < urls.length; i++) {
                console.log("fetching page: " + i + " of " + urls.length + " as: " + urls[i]);
                if (limitRecursive) {
                    if (i >= limitRecursive) {
                        break;
                    }
                }

                if (urls[i]) {
                    let process = true;
                    if (startFromItem) {
                        // start=150&
                        let currentStart = urls[i].substring(urls[i].indexOf("?start=") + 7, url[i].indexOf("&q="));
                        if (Number.parseInt(currentStart) < startFromItem) {
                            process = false;
                        }
                    }
                    if (process) {
                        res = await self.listPapers(rootUrl + urls[i]);
                        plist = res[0];
                        let urls1 = res[1];
                        if (urls1[urls1.length - 1] !== urls[urls.length - 1]) {
                            urls.push(urls1[urls1.length - 1]);
                        }
                        list = list.concat(plist);
                        ms = utils.getTimeoutRandom(timeoutBase);
                        console.log("robot waiting: " + ms);
                        await utils.wait(ms);
                    } else {
                        console.log("skip url: ", urls[i]);
                    }
                }
            }

            for (let item of list) {
                item.keyword = keyword;
            }

            ms = utils.getTimeoutRandom(timeoutBase);
            console.log("robot waiting: " + ms);
            await utils.wait(ms);

            return list;
        } catch (error) {
            throw error;
        }
    }
}