
module.exports = {
    wait: (ms) => {
        return new Promise((resolve) => {
            setTimeout(() => {
                resolve(true);
            }, ms);
        });
    },
    getTimeoutRandom: (ms) => {
        return Math.floor(ms + (Math.random() - 0.5) * ms);
    },
    groupBy: (items, key) => items.reduce(
        (result, item) => ({
            ...result,
            [item[key]]: [
                ...(result[item[key]] || []),
                item,
            ],
        }),
        {},
    )
}