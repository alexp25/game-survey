var fs = require('fs');

module.exports = {
    json2csv_items: function (items) {
        const replacer = (key, value) => value === null ? '' : value; // specify how you want to handle null values here
        let header = Object.keys(items[0]);
        header = ["title", "installs", "minInstalls", "maxInstalls", "score", "scoreText", "ratings", "reviews", "price", "free", "currency", "size", "genre", "genreId", "developer", "released", "updated", "editorsChoice", "appId"];
        let csv = items.map(row => header.map(fieldName => JSON.stringify(row[fieldName], replacer).replace(",", " ")).join(','));
        csv.unshift(header.join(','));
        csv = csv.join('\r\n');

        // const delimiter = ",";

        // let csv = header.join(delimiter) + "\r\n";
        // for (let i = 0; i < items.length; i++) {
        //     let item = items[i];
        //     let csv_line = "";
        //     for (let j = 0; j < header.length; j++) {
        //         let key = header[j];
        //         let entry = "";
        //         if (item[key]) {
        //             if (item[key].length == null) {
        //                 entry = item[key];
        //             } else {
        //                 // item is string or array
        //                 if (item[key][0].length == null) {
        //                     // item is string/value
        //                     entry = item[key];
        //                 } else {
        //                     // item is array of strings/values
        //                     // entry = "ARRAY";
        //                     entry = item[key];
        //                 }
        //             }
        //             // entry = JSON.stringify(item[key]);
        //         } else {
        //             entry = "UNDEFINED";
        //         }
        //         csv_line += "" + (entry.replace(",", " ").replace("\"", "")) + delimiter
        //     }
        //     csv_line += "\r\n";
        //     csv += csv_line;
        // }
        console.log(csv);
        return csv;
    },
    writeResult: function (res, name) {
        let csv = this.json2csv_items(res);
        fs.writeFile('result_' + name + '.csv', csv, function (err) {
            if (err) throw err;
            console.log('Saved!');
        });
        fs.writeFile('result_' + name + '.json', JSON.stringify(res), function (err) {
            if (err) throw err;
            console.log('Saved!');
        });
    },
    writeFile: (content, filename) => {
        return new Promise((resolve, reject) => {
            fs.writeFile(filename, content, (err) => {
                if (err) {
                    reject(err);
                    return;
                }
                resolve(true);
            });
        });
    }
};

