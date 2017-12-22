# C-3PO (WIP)

When he's not flying around with the Solos and Skywalkers on the Millenium Falcon, C-3PO decided to help LTTKGP out with managing the huge amount of songs being posted each day and organising them in a database (such a nice guy!). Known for his loving nature, he feels it'd be so much better to appreciate the top OPs on the group with weekly highlights. He also promises to use his supreme knowledge of Machine Learning to analyze trends and give music recommendations.

## Setup
### Facebook Graph API
You will need 'User access tokens' to work with the Graph API. You can find more information here: https://developers.facebook.com/docs/graph-api/overview#step2

As explained in the link above, create a new Facebook app (My Apps -> Add a new app) and generate user access tokens through the Graph API explorer.

Once done, create a file in repo root called `.env` with contents as follows:
```
FB_LONG_ACCESS_TOKEN="xxxx"
FB_SHORT_ACCESS_TOKEN="xxx"
FB_APP_ID="xxxx"
FB_APP_SECRET="xxxx"
```

### Python requirements
Use `pip` to install the project requirements as:
```bash
pip install -r requirements.txt
```

## Contributing
Contributions are always welcome. Your contributions could either be creating new features, fixing bugs or improving documentation and examples. Find more detailed information in [CONTRIBUTING.md](https://github.com/lttkgp/C-3PO/blob/master/CONTRIBUTING.md).

## KWoC?
If you reached here through KWoC '17, you're already doing great by doing your research before selecting your project. Please do have a look at [KWOC.md](https://github.com/lttkgp/C-3PO/blob/master/KWOC.md) to find out more about me, the programme and plans for KWoC.

## License
MIT
