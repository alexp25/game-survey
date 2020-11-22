const readline = require('readline');

const rl = readline.createInterface({
    input: process.stdin,
    output: process.stdout
});

exports.question = (q) => {
    return new Promise((resolve) => {
        var response;

        rl.setPrompt(q);
        rl.prompt();

        rl.on('line', (userInput) => {
            response = userInput;
            rl.close();
        });

        rl.on('close', () => {
            resolve(response);
        });
    });
};