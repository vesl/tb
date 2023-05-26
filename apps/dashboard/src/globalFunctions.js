export const stringFunctions = {
    firstLetterUpper: (string) => {
        const words = string.split(" ");
        for (let i = 0; i < words.length; i++) {
            words[i] = words[i][0].toUpperCase() + words[i].substr(1);
        }
        return words.join(" ");
    },
    formatDate: (date) => {
        return date.toLocaleDateString('en-US').replace(/\//g,'-')  
    }
}