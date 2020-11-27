
const writer = require('./writer');
const metacritic = require('./metacritic');
const reader = require('./reader');

let dataFolder = "../data/metacritic_v2/";

dataFolder = "../data/metacritic_v3/";

var getFilename = (platform, category) => {
    let plt = platform.replace("-", "_");
    if (category) {
        plt += "." + (category.replace("-", "_"));
    }
    let filename = dataFolder + "result_database." + plt + ".json";
    return filename;
};

var main = async (platform, useLegacy, category) => {
    // 2008 - 2020
    let res = await metacritic.listGamesRecursive(platform, 100, useLegacy, category);

    console.log("writing database file");
    await writer.writeFile(JSON.stringify(res), getFilename(platform, category));
    console.log("done");
};


var extractCSV = async (filename, replacetoken) => {
    // rank,title,score,user_score,release_date
    content = await reader.readFile(filename);
    content = JSON.parse(content);
    var csv = "rank,title,score,user_score,release_date,category\r\n";
    var index = 0;

    for (let i = 0; i < content.length; i++) {
        let game = content[i];

        if (replacetoken) {
            game.name = game.name.replace(/,/g, " ");
            if (game.category) {
                game.category = game.category.replace(/,/g, " ");
            }
            game.releaseDate = game.releaseDate.split(", ")[1];
        }
        var line = (index + 1) + "," + game.name + "," + game.score + "," + game.userScore + "," + game.releaseDate + "," + game.category;
        index += 1;
        csv += line + "\r\n";

    }
    await writer.writeFile(csv, filename + ".csv");
    return true;
};

var mainCombined = async (useLegacy, category) => {
    await main(platform, useLegacy, category);
    await extractCSV(getFilename(platform, category), true);
};

var mainCombinedCategories = async (categories) => {
    for (let i = 0; i < categories.length; i++) {
        await mainCombined(true, categories[i]);
    }
}

var concat = async (platforms, resultName) => {
    let content = [];
    for (let i = 0; i < platforms.length; i++) {
        let platform = platforms[i];
        let c = await reader.readFile(getFilename(platform, null));
        c = JSON.parse(c);
        content = content.concat(c);
    }
    await writer.writeFile(JSON.stringify(content), getFilename(resultName, null));
}


let platform = "ios";
platform = "ps4";
platform = "xboxone";

// main(platform, false);

platform = "pc";
// platform = "ps3";
// platform = "ps2";
// platform = "xbox360";
// platform = "wii";
// platform = "xbox";
// platform = "ds";

// mainCombined(true, "action");
// mainCombinedCategories(['action', 'adventure', 'first-person', 'role-playing', 'racing', 'third-person', 'simulation', 'real-time']);
mainCombinedCategories(['action']);

// concat(["ps4", "xboxone", "ps2", "xbox360", "wii", "xbox", "ds"], "console");
// extractCSV(dataFolder + "result_database.console.json", true);
