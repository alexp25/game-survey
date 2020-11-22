
const crawler = require('./crawler');

var self = module.exports = {
    extractValue: (finder, searchWord, offset, endstring) => {
        var findex = finder.indexOf(searchWord);
        var finder = finder.substring(findex);
        var value = finder.substring(searchWord.length + offset, finder.indexOf(endstring));
        return value;
    },
    extractValueMode2: (str, searchWord, endstring, offsetMax) => {
        findex = str.indexOf(searchWord);
        var finder = str.substring(findex, findex + offsetMax);
        finder = finder.substring(finder, finder.indexOf(endstring));

        var finderSplit = finder.split("span");
        finder = finderSplit[2];

        var installs = finder.substring(finder.indexOf(">") + 1, finder.indexOf("</"));
        return installs;
    },
    getGameDetails: async (packageName) => {
        try {
            let url = "https://play.google.com/store/apps/details?id=" + packageName + "&hl=en_US&gl=US";

            // "aggregateRating":{"@type":"AggregateRating","ratingValue":"4.049019813537598","ratingCount":"787"}
            response = await crawler.getPageHTML(url);
            let str = response;

            var searchWord = "aggregateRating";
            var findex = str.indexOf(searchWord);
            var finder = str.substring(findex, findex + 200);
            // console.log(finder);

            var rating = self.extractValue(finder, "ratingValue", 3, "\",");
            var reviews = self.extractValue(finder, "ratingCount", 3, "\"}");
            var price = self.extractValue(finder, "price\"", 2, "\",");
            var priceCurrency = self.extractValue(finder, "priceCurrency\"", 2, "\",");

            var installs = self.extractValueMode2(str, "Installs</div>", "Current Version</div>", 1000);
            var inAppProducts = null;
            try {
                inAppProducts = self.extractValueMode2(str, "In-app Products</div>", "Permissions</div>", 1000);
            } catch{

            }
            var size = self.extractValueMode2(str, "Size</div>", "Installs</div>", 1000);
            var updated = self.extractValueMode2(str, "Updated</div>", "Size</div>", 1000);

            var details = {
                rating: Number.parseFloat(rating),
                reviews: Number.parseInt(reviews),
                price: price,
                priceCurrency: priceCurrency,
                installs: installs,
                inAppProducts: inAppProducts,
                size: size,
                updated: updated
            };

            return details;
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