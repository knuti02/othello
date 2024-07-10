// translate a number to a list of numbers indicating the position of the bit set to 1
export const binToLst = (num: number) => {
    const lst = [];
    const num_str = num.toString(2);
    for (let i = 0; i < num_str.length; i++) {
        if (num_str[i] === "1") {
            lst.push(num_str.length - i - 1);
        }
    }

    return lst;
};