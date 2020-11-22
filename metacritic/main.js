
const writer = require('./writer');
const metacritic = require('./metacritic');
const reader = require('./reader');


var main = async (platform, useLegacy) => {
    // 2008 - 2020
    let res = await metacritic.listGamesRecursive(platform, 50, useLegacy);

    console.log("writing database file");
    await writer.writeFile(JSON.stringify(res), "result_database." + platform + ".json");
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

let dataFolder = "../data/metacritic_v2/"
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

// main(platform, true);
extractCSV(dataFolder + "result_database." + platform + ".json", true);
