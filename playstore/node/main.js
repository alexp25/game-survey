// https://github.com/facundoolano/google-play-scraper


const gplay = require('google-play-scraper');
const writer = require('./writer');
const moby = require('./moby');
const crawler = require('./crawler');
const reader = require('./reader');
const googlebot = require('./googlebot');
const utils = require('./utils');


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

/**
 * crawler first pass
 */
var mainMoby = async () => {
    // 2008 - 2020
    let years = [2008, 2009, 2010, 2011, 2012, 2013, 2014, 2015, 2016, 2017, 2018, 2019, 2020];
    // years = [2008, 2009];
    let res = [];

    for (let i = 0; i < years.length; i++) {
        console.log("fetching games from " + years[i]);
        let res1 = await moby.listGamesRecursive(years[i], null);
        res = res.concat(res1);
    }

    console.log("writing database file");
    await writer.writeFile(JSON.stringify(res), "result_database.json");
    console.log("done");
    // let res = await moby.getGameDetails("https://www.mobygames.com/game/android/cascade-gem-jewel-adventure");
    // console.log(res);
};

/**
 * crawler second pass
 * update result database with details for each game
 * NOTE: not required as first pass is already year filtered
 */
var updateDetailsMoby = async () => {
    let resultDatabase = await reader.readFile("result_database.json");
    let games = JSON.parse(resultDatabase);
    for (let i = 0; i < games.length && i < 3; i++) {
        let game = games[i];
        console.log("fetching details for game " + i + " of " + games.length + ": " + game.name);
        let res = await moby.getGameDetails(game.url);
        let details = moby.parseGameDetails(res);
        console.log(details);
    }
}

var updateDetailsGoogleSearch = async () => {
    try {
        // let result = await googlebot.googleSearchV2("Angry Birds: Space");
        // result = result.toString();
        // let packageName = googlebot.getPackageName(result);
        // console.log(packageName);
        // await writer.writeFile(result, "googlesearch.2.html");

        // WARNING: 2nd pass, check invalid package names starting with https:, or containing </>
        // method 2 check valid package names containing dots

        let resultDatabase = await reader.readFile("result_database.json");
        let games = JSON.parse(resultDatabase);
        for (let i = 0; i < games.length; i++) {
            let game = games[i];
            console.log("fetching details for game " + i + " of " + games.length + ": " + game.name);
            try {
                let result = await googlebot.googleSearchPhantom(game.name + " apps on google play");
                result = result.toString();
                let packageName = googlebot.getPackageNameV2(result);
                // let packageUrl = googlebot.getPackageUrl(result);
                // console.log(packageUrl);
                console.log(packageName);
                game.packageName = packageName;
                // game.packageUrl = packageUrl;
            } catch (error) {
                console.log("error fetching google results");
                game.packageName = null;
            }
            await utils.wait(1000);
        }
        console.log("writing database file");
        await writer.writeFile(JSON.stringify(games), "result_database.3.json");
        console.log("done");
    } catch (error) {
        console.error(error);
    }
}

// mainMoby();
// updateDetailsMoby();
updateDetailsGoogleSearch();


// crawler.test();

// getDetails();
// listReviews();

// listApps();