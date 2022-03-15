const axios = require('axios');
const cheerio = require('cheerio');
const { JSDOM } = require('jsdom');
const writer = require('./writer');
const puppeteer = require('puppeteer-extra');
// add stealth plugin and use defaults (all evasion techniques)
const StealthPlugin = require('puppeteer-extra-plugin-stealth');
puppeteer.use(StealthPlugin());

var self = module.exports = {
    test: () => {


        // const $ = cheerio.load('<h2 class="title">Hello world</h2>');

        const $ = cheerio.load('<div id="title">Hello world</div>');

        // $('h2.title').text('Hello there!');
        // $('h2').addClass('welcome');

        // $.html();

        var text = $('div[id=title]').text();
        console.log(text);
    },
    getPageHTML: async (url) => {
        try {
            // const { data } = await axios.get(
            //     url,
            //     { headers: { 'User-Agent': 'Mozilla/5.0' } }
            // );
            // await writer.writeFile(data, "index.html");
            const browser = await puppeteer.launch({ headless: true });
            const page = await browser.newPage();
            const response = await page.goto(url);
            console.log("waiting for timeout");
            await page.waitForTimeout(5000);
            console.log("fetching response");
            let data = await response.text();
            await writer.writeFile(data, "index.html");
            await page.screenshot({ path: 'index.png', fullPage: true });
            console.log("closing browser");
            await browser.close();
            console.log("browser closed");
            return data;
        } catch (error) {
            console.error(error);
            throw error;
        }
    },
    getPostElements: async (url, tags) => {
        try {
            const { data } = await axios.get(
                url
            );
            // await writer.writeFile(data, "index.html");
            const $ = cheerio.load(data);
            const postElements = [];

            // 'div > p.title > a'
            $(tags).each((_idx, el) => {
                const post = $(el);
                postElements.push(post);
            });
            return [$, postElements];
        } catch (error) {
            throw error;
        }
    },
    getPostElementsCore: (data, tags) => {
        try {
            const $ = cheerio.load(data);
            const postElements = [];

            $(tags).each((_idx, el) => {
                const post = $(el);
                postElements.push(post);
            });

            return [$, postElements];
        } catch (error) {
            throw error;
        }
    },
    getPostTitles: ($, posts) => {
        try {
            let postTitles = posts.map(post => post.text());
            return postTitles;
        } catch (error) {
            console.error(error);
            return [];
        }
    },
    getPostHref: ($, posts) => {
        try {
            let postTitles = posts.map(post => post.attr("href"));
            return postTitles;
        } catch (error) {
            console.error(error);
            return [];
        }
    },
    getPostHrefAnchor: ($, posts) => {
        try {
            let postTitles = posts.map(post => {
                let href;
                post.find('a').each((_idx, el) => {
                    href = $(el).attr("href");
                });
                return href;
            });
            return postTitles;
        } catch (error) {
            console.error(error);
            return [];
        }
    }
}