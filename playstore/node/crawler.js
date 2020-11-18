const axios = require('axios');
const cheerio = require('cheerio');
const { JSDOM } = require('jsdom');
const writer = require('./writer');

var self = module.exports = {
    test: () => {
        const $ = cheerio.load('<h2 class="title">Hello world</h2>')

        $('h2.title').text('Hello there!')
        $('h2').addClass('welcome')

        $.html()
    },
    getPostTitles: async (url, tags) => {
        try {
            const { data } = await axios.get(
                url
            );
            // await writer.writeFile(data, "index.html");
            const $ = cheerio.load(data);
            const postTitles = [];

            // 'div > p.title > a'
            $(tags).each((_idx, el) => {
                const postTitle = $(el).text();
                postTitles.push(postTitle);
            });
            return postTitles;
        } catch (error) {
            throw error;
        }
    },
    getPostHref: async (url, tags) => {
        try {
            const { data } = await axios.get(
                url
            );
            // await writer.writeFile(data, "index.html");
            const $ = cheerio.load(data);
            const postTitles = [];

            // 'div > p.title > a'
            $(tags).each((_idx, el) => {
                const postTitle = $(el).attr('href');
                postTitles.push(postTitle);
            });
            return postTitles;
        } catch (error) {
            throw error;
        }
    }
}