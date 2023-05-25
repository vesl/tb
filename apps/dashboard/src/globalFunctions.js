export const stringFunctions = {
    firstLetterUpper: (string) => {
        const words = string.split(" ");
        for (let i = 0; i < words.length; i++) {
            words[i] = words[i][0].toUpperCase() + words[i].substr(1);
        }
        return words.join(" ");
    }
}

export const toastFunctions = {
    popError(message) {
        this.$toast.add({ severity: 'error', summary: 'Error', detail: message, life: 3000 });
    }
}