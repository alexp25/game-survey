// https://github.com/facundoolano/google-play-scraper


const gplay = require('google-play-scraper');
const writer = require('./writer');
const moby = require('./moby');
const playstore = require('./playstore');
const crawler = require('./crawler');
const reader = require('./reader');
const googlebot = require('./googlebot');
const utils = require('./utils');



let dataFolder = "../data/playstore/";

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
var mainMoby = async (platform, years) => {
    let res = [];

    if (years) {
        for (let i = 0; i < years.length; i++) {
            console.log("fetching games from " + years[i]);
            let res1 = await moby.listGamesRecursive(years[i], platform, null);
            res = res.concat(res1);
        }
    } else {
        res = await moby.listGamesRecursive(null, platform, null);
    }

    console.log("writing database file");
    await writer.writeFile(JSON.stringify(res), dataFolder + "result_database." + platform + ".json");
    console.log("done");
};

/**
 * crawler second pass
 * update result database with details for each game
 * NOTE: not required as first pass is already year filtered
 */
var updateDetailsMoby = async () => {
    let resultDatabase = await reader.readFile(dataFolder + "result_database.json");
    let games = JSON.parse(resultDatabase);
    for (let i = 0; i < games.length && i < 3; i++) {
        let game = games[i];
        console.log("fetching details for game " + i + " of " + games.length + ": " + game.name);
        let res = await moby.getGameDetails(game.url);
        let details = moby.parseGameDetails(res);
        console.log(details);
    }
}

var updateDetailsGoogleSearch = async (platform) => {
    try {
        // let result = await googlebot.googleSearchV2("Angry Birds: Space");
        // result = result.toString();
        // let packageName = googlebot.getPackageName(result);
        // console.log(packageName);
        // await writer.writeFile(result, "googlesearch.2.html");

        // WARNING: 2nd pass, check invalid package names starting with https:, or containing </>
        // method 2 check valid package names containing dots

        let resultDatabase = await reader.readFile(dataFolder + "result_database." + platform + ".json");
        let games = JSON.parse(resultDatabase);

        let checkpoint = 100;
        let count = 0;

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

                if ((count % checkpoint) == 0) {
                    console.log("writing database file (checkpoint)");
                    await writer.writeFile(JSON.stringify(games), dataFolder + "result_database." + platform + ".googlesearch.json");
                    console.log("done");
                }

                count += 1;

            } catch (error) {
                console.log("error fetching google results");
                game.packageName = null;
            }
            await utils.wait(1000);
        }
        console.log("writing database file");
        await writer.writeFile(JSON.stringify(games), dataFolder + "result_database." + platform + ".googlesearch.json");
        console.log("done");
    } catch (error) {
        console.error(error);
    }
}

var updateDetailsPlaystore = async (platform, rerun) => {
    try {
        // let result = await googlebot.googleSearchV2("Angry Birds: Space");
        // result = result.toString();
        // let packageName = googlebot.getPackageName(result);
        // console.log(packageName);
        // await writer.writeFile(result, "googlesearch.2.html");

        // WARNING: 2nd pass, check invalid package names starting with https:, or containing </>
        // method 2 check valid package names containing dots

        let resultDatabase = await reader.readFile(rerun ? dataFolder + "result_database." + platform + ".playstore.json" : dataFolder + "result_database." + platform + ".googlesearch.json");
        let games = JSON.parse(resultDatabase);
        let checkpoint = 100;
        let count = 0;
        for (let i = 2142; i < games.length; i++) {
            let game = games[i];
            console.log("fetching details for game " + i + " of " + games.length + ": " + game.name + " [" + game.packageName + "]");
            game.errorLoading = false;
            game.invalidMetadata = false;

            if ((game.packageName.split(".").length >= 2) && (game.packageName.indexOf("http") === -1) && (game.packageName.length >= 7)) {
                if (!game.loaded && !game.errorLoading) {
                    try {
                        let details = await playstore.getGameDetails(game.packageName);
                        Object.assign(game, details);
                        game.loaded = true;
                        // console.log(game);

                        if ((count % checkpoint) == 0) {
                            console.log("writing database file (checkpoint)");
                            await writer.writeFile(JSON.stringify(games), dataFolder + "result_database." + platform + ".playstore.json");
                            console.log("done");
                        }
                        count += 1;

                    } catch (error) {
                        console.log("error fetching google results");
                        // console.log(error);
                        game.errorLoading = true;
                    }

                    await utils.wait(1000);
                }
            } else {
                console.log("invalid package name: ", game.packageName);
                game.invalidMetadata = true;
            }
        }
        console.log("writing database file");
        await writer.writeFile(JSON.stringify(games), dataFolder + "result_database." + platform + ".playstore.json");
        console.log("done");
    } catch (error) {
        console.error(error);
    }
}

var showStats = async (filename) => {
    content = await reader.readFile(filename);
    content = JSON.parse(content);

    var stats = {
        titles: content.length,
        loaded: content.filter(item => item.loaded).length,
        error: content.filter(item => item.errorLoading).length,
        invalid: content.filter(item => item.invalidMetadata).length
    };

    console.log(stats);
}

var extractCSV = async (filename, replacetoken, checkRating) => {
    // rank,title,score,user_score,release_date
    content = await reader.readFile(filename);
    content = JSON.parse(content);
    var csv = "rank,title,score,user_score,release_date,category\r\n";
    var index = 0;
    console.log(content.length);
    content.sort((a, b) => {
        if (a.name > b.name) {
            return 1;
        }
        if (a.name < b.name) {
            return -1;
        }
        return 0;
    });
    for (let i = 0; i < content.length; i++) {
        let game = content[i];
        // console.log(game.name);
        if (game.rating != null || !checkRating) {
            if (replacetoken) {
                game.name = game.name.replace(/,/g, " ");
                game.category = game.category.replace(/,/g, " ");
            }
            var line = (index + 1) + "," + game.name + "," + game.rating + "," + game.rating + "," + game.year + "," + game.category;
            index += 1;
            csv += line + "\r\n";
        }
    }
    await writer.writeFile(csv, filename + ".csv");
    return true;
};

var extractCategories = async (filename) => {
    content = await reader.readCsvFile(filename);
    // console.log(content);


    for (let i = 0; i < content.length; i++) {
        content[i].category = content[i].category.split(" ")[0];
    }

    const groupBy = (items, key) => items.reduce(
        (result, item) => ({
            ...result,
            [item[key]]: [
                ...(result[item[key]] || []),
                item,
            ],
        }),
        {},
    );

    var groups = groupBy(content, "category");

    var groupsNames = Object.keys(groups);

    for (let i = 0; i < groupsNames.length; i++) {
        let newFilename = filename.replace(".csv", "") + "." + groupsNames[i].toLowerCase().replace("-", "") + ".csv";
        await writer.writeCsvFile(groups[groupsNames[i]], newFilename);
        console.log(newFilename);
        console.log(groups[groupsNames[i]].length);
    }

    // console.log(Object.keys(groups));
}

var getDiff = async (file1, file2, result, concatResult) => {
    let c1 = await reader.readFile(file1);
    let c2 = await reader.readFile(file2);
    c1 = JSON.parse(c1);
    c2 = JSON.parse(c2);

    console.log("all: " + c1.length + ", " + c2.length);

    let removed = [];
    let added = [];
    let common = [];

    for (let i = 0; i < c2.length; i++) {
        let existing = false;
        for (let j = 0; j < c1.length; j++) {
            if (c2[i].name === c1[j].name) {
                existing = true;
                break;
            }
        }
        if (!existing) {
            added.push(c2[i]);
        }
    }


    for (let i = 0; i < c1.length; i++) {
        let existing = false;
        for (let j = 0; j < c2.length; j++) {
            if (c1[i].name === c2[j].name) {
                existing = true;
                break;
            }
        }
        if (!existing) {
            removed.push(c1[i]);
        } else {
            common.push(c1[i]);
        }
    }

    console.log("added: " + added.length);
    console.log("existing: " + common.length);
    console.log("removed: " + removed.length);

    let combined = c1.concat(added);

    let combinedUnique = [];
    for (let i = 0; i < combined.length; i++) {
        let existing = false;
        for (let j = 0; j < combinedUnique.length; j++) {
            if (combined[i].name === combinedUnique[j].name) {
                existing = true;
            }
        }
        if (!existing) {
            combinedUnique.push(combined[i]);
        }
    }

    console.log("combined: " + combined.length);
    console.log("combinedUnique: " + combinedUnique.length);


    await writer.writeFile(JSON.stringify(added), result);
    await writer.writeFile(JSON.stringify(combinedUnique), concatResult);

};



let platform = "android";
// platform = "iphone";
// platform = null;

// mainMoby(platform, [2008, 2009, 2010, 2011, 2012, 2013, 2014, 2015, 2016, 2017, 2018, 2019, 2020]);
// mainMoby(platform, null);

// extractCSV(dataFolder + "result_database." + platform + ".json", true, false);

// updateDetailsGoogleSearch(platform);
// platform += ".2";
// extractCSV(dataFolder + "result_database." + platform + ".googlesearch.json", true, false);

// updateDetailsPlaystore(platform, true);

// showStats(dataFolder + "result_database.json");
// showStats(dataFolder + "result_database." + platform + ".playstore.json");
// extractCSV(dataFolder + "result_database." + platform + ".playstore.json", true);
platform += ".3"
extractCategories(dataFolder + "result_database." + platform + ".playstore.json.csv");


// getDiff(dataFolder + "result_database.playstore.1.json", dataFolder + "result_database.android.json", dataFolder + "result_database.android.2.json");
// extractCSV(dataFolder + "result_database." + platform + ".2.json", true, false);

// updateDetailsGoogleSearch(platform + ".2");
// updateDetailsPlaystore(platform + ".2", true);

// getDiff(dataFolder + "result_database.android.1.playstore.json", dataFolder + "result_database.android.2.playstore.json", dataFolder + "result_database.android.3.playstore.json", dataFolder + "result_database.android.3.playstore.json");
// platform += ".3"
// extractCSV(dataFolder + "result_database." + platform + ".playstore.json", true, true);