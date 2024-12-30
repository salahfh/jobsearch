from jobsearch.ai.gemini import Gemini

import pytest

@pytest.mark.skip('Avoid Uncessary API calls.')
def test_gemeni_authenticate_correctly():
    gemini = Gemini()
    assert 'True' in gemini.model.generate_content('Is it working? Responde with True').text