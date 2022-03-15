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
 * startFromItem not working properly
 */
var main = async (outfile, keywords, startFromItem) => {
    let res = [];
    let maxpage = 2;
    maxpage = 50;

    let q = await ui.question("type y to start\n");
    if (q === "y") {
        console.log("starting");
    } else {
        return;
    }

    for (let i = 0; i < keywords.length; i++) {
        let find = ' ';
        let re = new RegExp(find, 'g');
        let kw = keywords[i].replace(re, "+");
        console.log("fetching data from " + kw);
        try {
            let res1 = await googlescholar.listPapersRecursive(kw, maxpage, 20000, startFromItem);
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
    let mainOutputFilename = dataFolder + "result_database_processed.json";
    await writer.writeFile(JSON.stringify(content), mainOutputFilename);
    var groups = utils.groupBy(content, "keyword");
    var groupsNames = Object.keys(groups);
    console.log(groupsNames);
    var outputFilenames = [];

    for (let i = 0; i < groupsNames.length; i++) {
        let find = ' ';
        let re = new RegExp(find, 'g');
        let fname = groupsNames[i].toLowerCase().replace(re, "_");
        let newFilename = filename.replace(".json", "") + "." + fname + ".json";
        outputFilenames.push(newFilename);
        await writer.writeFile(JSON.stringify(groups[groupsNames[i]]), newFilename);
        console.log(newFilename);
        console.log(groups[groupsNames[i]].length);
    }

    // console.log(Object.keys(groups));
    return [mainOutputFilename, outputFilenames];

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
    let [mainOutputFilename, outputFilenames] = await processDatabase(filename);
    await extractCSV(mainOutputFilename, true);
    for (let i = 0; i < outputFilenames.length; i++) {
        await extractCSV(outputFilenames[i], true);
    }
};

var merge = async (filenames) => {
    let files = [];
    for (let filename of filenames) {
        files.push(dataFolder + filename);
    }
    let contentMerge = [];
    for (let i = 0; i < files.length; i++) {
        let content = await reader.readFile(files[i]);
        content = JSON.parse(content);
        contentMerge = contentMerge.concat(content);
    }
    await writer.writeFile(JSON.stringify(contentMerge), dataFolder + "result_database_merge.json");
}

let mode = "collect";
mode = "merge";
mode = "process";
let files = ["result_database.3.json", "result_database.4.json", "result_database.5.json", "result_database.7.json", "result_database.8.json"]

console.log("mode: ", mode);

switch (mode) {
    case "collect":
        let keywords = ["Crowdsensing", "Blockchain", "Crowdsensing Blockchain", "Serious Gaming"];
        keywords = ["Urban Water", "Crowdsensing Water", "Blockchain Water", "Serious Gaming Water"];
        keywords = ["IoT for water infrastructure monitoring", "Big Data in water infrastructure", "Anomaly detection in water infrastructure", "Decision Support System Water", "water smart cities"];
        keywords = ["IoT water", "big data water", "anomaly detection water", "water smart cities OR water smart city"];
        // keywords = ["big data water"];
        // let outfile = dataFolder + "result_database.4.json";
        keywords = ["water smart cities OR water smart city"];
        keywords = ["decision support system water"];
        let outfile = dataFolder + "result_database.8.json";
        main(outfile, keywords, null);
        break;
    case "merge":
        merge(files);
        break;
    case "process":
        postprocess(dataFolder + "result_database_merge.json");
        break;
}


