// https://github.com/facundoolano/google-play-scraper


const gplay = require('google-play-scraper');
const writer = require('./writer');
const moby = require('./moby');


var getDetails = function () {
    // gplay.app({ appId: 'com.google.android.apps.translate' })
    gplay.app({ appId: 'com.leplace.global' })
        .then(console.log, console.log);
};

var listApps = function (category, details, maxn, page) {
    return gplay.list({
        category: category ? category : gplay.category.GAME_ACTION,
        collection: gplay.collection.TOP_FREE,
        num: maxn,
        page: page,
        fullDetail: details,
        throttle: 10
    });
};

var listReviews = function () {
    // This example will return 3000 reviews
    // on a single call
    gplay.reviews({
        appId: 'com.leplace.global',
        sort: gplay.sort.NEWEST,
        num: 10
    }).then((reviews) => {
        console.log(reviews.data.map(review => review.date));
    }).catch((err) => {
        console.error(err);
    });
};


var searchApps = function () {
    gplay.search({
        term: "panda",
        num: 2
    }).then(console.log, console.log);
}

var getGameCategories = function () {
    return new Promise((resolve, reject) => {
        gplay.categories().then((categories) => {
            resolve(categories.filter(cat => cat.startsWith("GAME")));
            // console.log(categories);
        }).catch((err) => {
            reject(err);
        });
    });
};


var main = async function () {
    let gameCats = await getGameCategories();
    console.log(gameCats);
    let games = await listApps(gplay.categories.GAME, false, 10, 1);
    console.log(games.length);
    console.log(games);
    // writer.writeResult(games, "all_games");
};

var mainMoby = async () => {
    let res = await moby.listGamesRecursive(2020, 0);
    console.log(res);
};


// main();
mainMoby();

// getDetails();
// listReviews();

// listApps();