const axios = require('axios');
const cheerio = require('cheerio');
const { JSDOM } = require('jsdom');
const writer = require('./writer');

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
            const { data } = await axios.get(
                url,
                { headers: { 'User-Agent': 'Mozilla/5.0' } }
            );
            await writer.writeFile(data, "index.html");
            return data;
        } catch (error) {
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