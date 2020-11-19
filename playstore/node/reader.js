var fs = require('fs');

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
    }
};

