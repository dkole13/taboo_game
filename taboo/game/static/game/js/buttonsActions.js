const startButton = document.getElementById('startButton');
const startBlock = document.getElementById('startBlock');
const rulesBlock = document.getElementById('rulesBlock');
const getInfoBlock = document.getElementById('getInfoBlock');

function ShowRules() {
    startBlock.style.display = 'none';
    rulesBlock.style.display = 'block';
}

function ShowGetInfo() {
    rulesBlock.style.display = 'none';
    getInfoBlock.style.display = 'block';
}
