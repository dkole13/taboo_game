let usedWords = [];
let currentWord = '';

function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

const csrftoken = getCookie('csrftoken');

function fetchNewWord() {
    fetch('/get_next_word/', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': csrftoken,
        },
        body: JSON.stringify({used: usedWords})
    })
    .then(response => response.json())
    .then(data => {
        currentWord = data.word;
        usedWords.push(currentWord);
        document.getElementById('current-word').innerText = currentWord;
        document.getElementById('taboo-word-1').innerText = data.taboo_words[0];
        document.getElementById('taboo-word-2').innerText = data.taboo_words[1];
        document.getElementById('taboo-word-3').innerText = data.taboo_words[2];
        document.getElementById('taboo-word-4').innerText = data.taboo_words[3];
        document.getElementById('taboo-word-5').innerText = data.taboo_words[4];
    });
}

fetchNewWord();

let currentTeam = 'red';
let timerId;

function startTimer() {
    let timeLeft = 10;
    const timerEl = document.getElementById('timer');
    timerEnded = false

    const countdown = setInterval(() => {
        if (timeLeft <= 0) {
            clearInterval(countdown);
            timerEl.textContent = "00:00";
            timerEnded = true
        } else {
            let minutes = Math.floor(timeLeft / 60);
            let seconds = timeLeft % 60;

            let formatted =
                (minutes < 10 ? '0' : '') + minutes + ':' + (seconds < 10 ? '0' : '') + seconds;
            timerEl.textContent = formatted;
            timeLeft--;
        }
    }, 1000);

}

function switchTeam() {
    currentTeam = currentTeam === 'blue' ? 'red' : 'blue';
    updateUIForTeam();
    startTimer();
}

function updateUIForTeam() {
    const currentWordRectangle = document.getElementById('current-word');
    const guessedBtn = document.getElementById('found-btn');
    const skipBtn = document.getElementById('skip-btn');
    const timerEl = document.getElementById('timer');

    if (currentTeam === 'blue') {
        currentWordRectangle.style.backgroundColor = '#0047ab';
        guessedBtn.style.backgroundColor = '#0047ab';
        skipBtn.style.backgroundColor = '#d32f2f';
        timerEl.style.color = '#0047ab';
    } else {
        currentWordRectangle.style.backgroundColor = '#d32f2f';
        guessedBtn.style.backgroundColor = '#d32f2f';
        skipBtn.style.backgroundColor = '#0047ab';
        timerEl.style.color = '#d32f2f';
    }
}

document.getElementById('skip-btn').addEventListener('click', () => {
    if (currentTeam === 'blue') {
        let redScoreElem = document.getElementById('red-score');
        redScoreElem.innerText = parseInt(redScoreElem.innerText) + 1;
    } else {
        let blueScoreElem = document.getElementById('blue-score');
        blueScoreElem.innerText = parseInt(blueScoreElem.innerText) + 1;
    }

    if (timerEnded) {
        switchTeam();
    };

    fetchNewWord();
});

document.getElementById('found-btn').addEventListener('click', () => {
    if (currentTeam === 'red') {
        let redScoreElem = document.getElementById('red-score');
        redScoreElem.innerText = parseInt(redScoreElem.innerText) + 1;
    } else {
        let blueScoreElem = document.getElementById('blue-score');
        blueScoreElem.innerText = parseInt(blueScoreElem.innerText) + 1;
    }

    if (timerEnded) {
        switchTeam();
    };

    fetchNewWord();
});

startTimer();
