
var GoogleSearchScraper = require('phantom-google-search-scraper');
/**
 * scotocitorul pe google
 */
var self = module.exports = {
    googleSearchPhantom: async (searchText) => {
        try {
            let results = await GoogleSearchScraper.search({
                query: searchText, // Query for google engine
                limit: 1, // Limit number of results
                keepPages: true, // Populate results.pages with rendered HTML content.
                // solver: GoogleScraper.commandLineSolver, // Optional solver for resolving captcha (see commandLineSolver.js)
                userAgent: 'GoogleSearchScraper1.0',
                // headers: { // Default http headers for PhantomJSs
                //     'Accept-Language': 'ru-RU,en,*'
                // },
                phantomOptions: [ // Command line options use for PhantomJS
                    '--ignore-ssl-errors=yes'
                ]
            });

            return results.pages;
        } catch (error) {
            throw error;
        }
    },
    /**
     * get android package name from google search results
     */
    getPackageName: (str) => {
        var searchWord = "id=com";
        var findex = str.indexOf(searchWord);
        var finder = str.substring(findex + 3, findex + 100);
        finder = finder.substring(0, finder.indexOf("</div"));
        return finder;
    },

    getPackageUrl: (str) => {
        var searchWordRoot = 'href="/url?q=';
        var searchWord = searchWordRoot;
        var searchWordInclude = "https://play.google.com/store/apps/details";
        searchWord += searchWordInclude;
        var findex = str.indexOf(searchWord);
        var finder = str.substring(findex + searchWordRoot.length);
        finder = finder.substring(0, finder.indexOf("\">"));
        return finder;
        // href="/url?q=https://play.google.com/store/apps/details%3Fid%3Dcom.rovio.angrybirdsspace.ads%26hl%3Den&amp;sa=U&amp;ved=2ahUKEwjS_KSz747tAhWMsKQKHdH-BEAQFjARegQIBhAB&amp;usg=AOvVaw3qJE46MiwJ-Tc6Nf9JZ6zX">
    },

    /**
     * more robust getter using url extractor
     */
    getPackageNameV2: (str) => {
        let url = self.getPackageUrl(str);
        let startToken = "%3Fid%3D";
        let packageName = url.substring(url.indexOf(startToken) + startToken.length, url.indexOf("%26h"));
        return packageName;
    }
}