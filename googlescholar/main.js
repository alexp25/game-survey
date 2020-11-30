// https://github.com/facundoolano/google-play-scraper

const writer = require('./writer');
const googlescholar = require('./googlescholar');
const ui = require('./ui');
const reader = require('./reader');
const utils = require('./utils');


let dataFolder = "../data/googlescholar/"

/**
 * notes
 * stopped at
 * fetching page: 16 of 17 as: /scholar?start=0&q=allintitle:+Crowdsensing+Blockchain&hl=en&as_sdt=0,5
 * empty results
 * 
 * exclude [CITATION]
 */

/**
 * crawler first pass
 */
var main = async (outfile, keywords, startFromItem) => {
    let res = [];
    let maxpage = 2;
    maxpage = 50;

    let q = await ui.question("type y to start");
    if (q === "y") {
        console.log("starting");
    } else {
        return;
    }

    for (let i = 0; i < keywords.length; i++) {
        console.log("fetching games from " + keywords[i]);
        try {
            let res1 = await googlescholar.listPapersRecursive(keywords[i], maxpage, 60000, startFromItem);
            res = res.concat(res1);
            console.log("writing database file (checkpoint)");
            await writer.writeFile(JSON.stringify(res), outfile);
            console.log("done");
        } catch (err) {
            console.error(err);
            console.log("error encountered, exit crawler?");
            let q = await ui.question("type y to exit (else continue)");
            if (q === "y") {
                break;
            }
        }
    }

    console.log("writing database file");
    await writer.writeFile(JSON.stringify(res), outfile);
    console.log("done");
    // let res = await moby.getGameDetails("https://www.mobygames.com/game/android/cascade-gem-jewel-adventure");
    // console.log(res);
};

var processDatabase = async (filename) => {
    let content = await reader.readFile(filename);
    content = JSON.parse(content);

    console.log("initial results: " + content.length);

    let uniqueItems = [];
    content = content.filter((item) => {
        if (item.name.indexOf("[CITATION]") !== -1) {
            return false;
        }
        if (uniqueItems.find(e => e.name === item.name && e.keyword === item.keyword)) {
            // not unique
            // console.log("duplicate entry: " + item.name);
            return false;
        }
        uniqueItems.push(item);
        return true;
    });

    console.log("filtered results: " + content.length);

    await writer.writeFile(JSON.stringify(content), dataFolder + "result_database_processed.json");

    var groups = utils.groupBy(content, "keyword");

    var groupsNames = Object.keys(groups);
    console.log(groupsNames);

    var outputFilenames = [];

    for (let i = 0; i < groupsNames.length; i++) {
        let newFilename = filename.replace(".json", "") + "." + groupsNames[i].toLowerCase().replace(" ", "_") + ".json";
        outputFilenames.push(newFilename);
        await writer.writeFile(JSON.stringify(groups[groupsNames[i]]), newFilename);
        console.log(newFilename);
        console.log(groups[groupsNames[i]].length);
    }

    // console.log(Object.keys(groups));
    return outputFilenames;

};

var extractCSV = async (filename, replacetoken) => {
    // rank,title,score,user_score,release_date
    content = await reader.readFile(filename);
    content = JSON.parse(content);
    var csv = "index,keyword,title,details,year\r\n";
    var years = [];

    for (let i = 2000; i < 2021; i++) {
        years.push("" + i);
    }

    var index = 0;
    for (let i = 0; i < content.length; i++) {
        let paper = content[i];
        if (replacetoken) {
            paper.name = paper.name.replace(/,/g, " ");
            paper.details = paper.details.replace(/,/g, " ");
            paper.year = null;
            for (let year of years) {
                if (paper.details.indexOf(year) !== -1) {
                    paper.year = Number.parseInt(year);
                    break;
                }
            }
        }
        var line = (index + 1) + "," + paper.keyword + "," + paper.name + "," + paper.details + "," + paper.year;
        index += 1;
        csv += line + "\r\n";
    }
    await writer.writeFile(csv, filename + ".csv");
    return true;
};

var postprocess = async (filename) => {
    let outputFilenames = await processDatabase(filename);
    await extractCSV(filename, true);
    for (let i = 0; i < outputFilenames.length; i++) {
        await extractCSV(outputFilenames[i], true);
    }
};

var merge = async () => {
    let files = [
        dataFolder + "result_database.1.json",
        dataFolder + "result_database.2.json",
        dataFolder + "result_database.4.json"
    ];
    let contentMerge = [];
    for (let i = 0; i < files.length; i++) {
        let content = await reader.readFile(files[i]);
        content = JSON.parse(content);
        contentMerge = contentMerge.concat(content);
    }
    await writer.writeFile(JSON.stringify(contentMerge), dataFolder + "result_database_2.json");
}


// let keywords = ["Crowdsensing", "Blockchain", "Crowdsensing Blockchain", "Serious Gaming"];
// let keywords = ["Urban Water", "Crowdsensing Water", "Blockchain Water", "Serious Gaming Water"];
// let outfile = dataFolder + "result_database.4.json";
// main(outfile, keywords, null);
// merge();
postprocess(dataFolder + "result_database_2.json");
