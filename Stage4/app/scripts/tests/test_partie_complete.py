import os
import sys

# Ensure Stage4 is on the Python path so we can import the Flask app
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'Stage4')))

import pytest
from app import create_app

@pytest.fixture()
def client():
    app = create_app()
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client


def test_full_game(client):
    # Start a new game
    resp = client.post('/api/start_game', json={'num_players': 2, 'seed': 42})
    assert resp.status_code == 200
    data = resp.get_json()
    assert 'game_id' in data
    game_id = data['game_id']

    winner = None
    turns = 0
    result = None

    # Play until a winner is declared or a safety limit is reached
    while winner is None and turns < 200:
        resp = client.post('/api/play_turn', json={'game_id': game_id})
        assert resp.status_code == 200
        result = resp.get_json()
        assert 'state' in result
        assert 'winner' in result
        state = result['state']
        for key in ['num_players', 'deck_size', 'discard_pile', 'hands', 'current_player', 'direction', 'turn']:
            assert key in state
        winner = result['winner']
        turns += 1

    assert winner is not None
    assert 'scores' in result
    assert isinstance(result['scores'], list)
