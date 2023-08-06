# BattleNet Clients
BattleNet Clients provide a uniform interface for Blizzard's Battle.net Developer Rest Application Programming
Interface (BNET Rest API) 

## Installation

Windows, OS X & Linux:

    pip install battlenet_client

## Clone
Clone the latest version: https://gitlab.com/battlenet1/battlenet-client.git

## Usage Example
    # client_id and client_secret found in your battle.net developer account 
    import battlenet_client
    client = battlenet_client.BattleNetClient(battlenet_client.UNITED_STATES, battlenet_client.WOW,
                 client_id='<client_id>', client_secret='<client_secret>')
    client.get('data/wow/playable-class/1', locale='en_US', namespace='static-us')

For more information, please the [wiki][wiki]

Note: This package is a dependency of my other [Battle.net REST API packages](https://gitlab.com/battlenet1)

## Release History
Please change log for complete history

## Meta

David "Gahd" Couples – [@gahdania][twitter] – gahdania@gahd.io

Distributed under the GPL v3+ license. See ``LICENSE`` for more information.

[Battle.net Client on Gitlab][gitlab]

## Contributing

1. [Fork it][fork]
2. Create your feature branch (`git checkout -b feature/fooBar`)
3. Commit your changes (`git commit -am 'Add some fooBar'`)
4. Push to the branch (`git push origin feature/fooBar`)
5. Create a new Pull Request

<!-- Markdown link & img dfn's -->
[wiki]: https://battlenet1.gitlab.io/battlenet-client
[twitter]: https://twitter.com/gahdania
[gitlab]: https://gitlab.com/battlenet1/battlenet-client
[fork]: https://gitlab.com/battlenet1/battlenet-client/-/forks/new
[header]: https://gilab.com/