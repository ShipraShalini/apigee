{
	'user': {
		'mappings': {
			'info': {
				'properties': {
					'first_name': {
						'type': 'string',
                        'index': 'not_analyzed'
					},
					'last_name': {
						'type': 'string',
                        'index': 'not_analyzed'
					},
					'country': {
						'type': 'string',
                        'index': 'not_analyzed'
					},
					'ip_address': {
						'type': 'string',
                        'index': 'not_analyzed'
					},
					'email': {
						'type': 'string',
                        'index': 'not_analyzed'
					}
				}
			}
		}
	}
}


{
	'user': {
		'mappings': {
			'info': {
				'dynamic_templates': [{
					'notanalyzed': {
						'match_mapping_type': 'string',
						'mapping': {
							'index': 'not_analyzed',
							'type': 'string'
						},
						'match': '*'
					}
				}],
			}
		}
	}
}