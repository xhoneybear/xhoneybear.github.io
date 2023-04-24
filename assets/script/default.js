const root = document.styleSheets[0].cssRules[5].style;
const setVar = (Var, Val) => root.setProperty(Var, Val);
var dark = false;

const terminal = document.getElementById("input");
var lock = false;
queue = [];

const ageField = document.getElementById("age");

function sleep(ms) {
    return new Promise(resolve => setTimeout(resolve, ms));
}

async function toggleTheme() {
    setVar('--animate', 0.5);
    if (root.getPropertyValue('--bg') == ' white') {
        dark = true;
        setVar('--bg', ' black');
        setVar('--font', ' var(--primary)');
        setVar('--title', ' var(--secondary)');
        setVar('--shadow', ' rgba(255, 255, 255, 0.25)');
        setVar('--icons', ' 1');
        setVar('--handle', ' right');
        setVar('--primary', ' #fd0');
        setVar('--secondary', ' #fb0');
    }
    else {
        dark = false;
        setVar('--bg', ' white');
        setVar('--font', ' black');
        setVar('--title', ' black');
        setVar('--shadow', ' rgba(0, 0, 0, 0.5)');
        setVar('--icons', ' 0');
        setVar('--handle', ' left');
        setVar('--primary', ' #fb0');
        setVar('--secondary', ' #fd0');
    }
    await sleep(500);
    setVar('--animate', 0);
}

async function switchTab(n) {
    for (let i = 0; i < document.querySelectorAll('div.menu').length; i++) {
        document.querySelectorAll('div.menu')[i].classList.remove('active');
    }
    document.querySelectorAll('div.menu')[n].classList.add('active');
    setVar('--animate', 1);
    setVar('--tab', n);
    await sleep(1000);
    setVar('--animate', 0);
}

var theme = window.matchMedia("(prefers-color-scheme: dark)")
if (theme.matches) {
    toggleTheme()
}

// I don't know if this works properly, if it doesn't work change != to ==
theme.addEventListener('change', state => {
    if (state.matches != dark) {
        toggleTheme();
    }
})

async function typeWrite(text) {
    queue.push(text);
    if (!lock && terminal.innerHTML.length > 0 && terminal.innerHTML != text) {
        await typeDelete();
    }
    while (lock) {
        await sleep(100);
    }
    if (terminal.innerHTML.length == 0 && queue.length <= 1) {
        lock = true;
        for (let i = 0; i < text.length; i++) {
            await sleep(75);
            terminal.innerHTML += text.charAt(i);
            if (terminal.innerHTML.length == text.length || text.charAt(i+1) == ' ') {
                setVar("--command", 'green');
            }
        }
        lock = false;
    }
    queue.splice(0, 1);
}

async function typeDelete(text=terminal.innerHTML) {
    while (lock) {
        await sleep(100);
    }
    if (!lock && terminal.innerHTML.length > 0) {
        lock = true;
        for (let i = terminal.innerHTML.length; i >= 0; i--) {
            await sleep(75);
            terminal.innerHTML = terminal.innerHTML.slice(0, i);
            if (terminal.innerHTML.length != text.length && text.slice(0, i+1).search(' ') == -1) {
                setVar("--command", 'red');
            }
        }
        lock = false;
    }
}

function insertAge() {
    const today = new Date();
    const birthDate = new Date(2002, 2, 13);
    const age = Math.floor((today - birthDate) / (1000 * 60 * 60 * 24 * 365.25));
    ageField.innerHTML = age;
}