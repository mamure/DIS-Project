function parseGame(data) {
    document.getElementById('game-id').textContent = data.game_id;
    document.getElementById('game-date').textContent = data.game_date;
    document.getElementById('event-name').textContent = data.event_name;
    document.getElementById('event-date').textContent = data.event_date;
    document.getElementById('result').textContent = data.result;

    document.getElementById('white-player-name').textContent = data.white_player.player_name;
    document.getElementById('white-player-title').textContent = data.white_player.title;
    document.getElementById('white-player-elo').textContent = data.white_player.elo || 'No data';
    document.getElementById('white-player-fide-id').textContent = data.white_player.fide_id;

    document.getElementById('black-player-name').textContent = data.black_player.player_name;
    document.getElementById('black-player-title').textContent = data.black_player.title;
    document.getElementById('black-player-elo').textContent = data.black_player.elo || 'No data';
    document.getElementById('black-player-fide-id').textContent = data.black_player.fide_id;

    document.getElementById('moves').textContent = data.moves;
}

document.addEventListener('DOMContentLoaded', function() {
    // Call the parseGame function with the data object
    parseGame(data);
});
