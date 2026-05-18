from shared import VOLUME_CONFIG, merge_volume_config


def test_volume_config_deep_merges_nested_override_maps():
    override = {
        'regex_replacements': {
            r'\bexample\b': 'sample',
        },
        'text_replacements': {
            'Charneck': 'Charnock',
        },
    }

    config = merge_volume_config(1, override)

    assert config['regex_replacements'][r'\bexample\b'] == 'sample'
    assert config['regex_replacements'][r'(\w+)]y\b'] == r'\1ly'
    assert config['text_replacements']['Charneck'] == 'Charnock'


def test_volume_config_merge_does_not_mutate_shared_defaults():
    config = merge_volume_config(2, {'regex_replacements': {r'\bfoo\b': 'bar'}})

    assert config['regex_replacements'][r'\bfoo\b'] == 'bar'
    assert 'regex_replacements' not in VOLUME_CONFIG[2]
