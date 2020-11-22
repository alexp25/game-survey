var fs = require('fs');
const csv = require('csv-parser');

module.exports = {
    readFile: (filename) => {
        return new Promise((resolve, reject) => {
            fs.readFile(filename, {}, (err, data) => {
                if (err) {
                    reject(err);
                    return;
                }
                resolve(data);
            });
        });
    },
    readCsvFile: (filename) => {
        return new Promise((resolve, reject) => {
            let rows = [];
            fs.createReadStream(filename)
                .pipe(csv())
                .on('data', (row) => {
                    rows.push(row);
                })
                .on('end', () => {
                    console.log('CSV file successfully processed');
                    resolve(rows);
                })
                .on('error', (err) => {
                    reject(err);
                });
        });
    }
};

