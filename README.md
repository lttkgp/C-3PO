<a href="https://www.deviantart.com/steveargyle/art/C-3PO-578309067"><img align="right" alt="C3PO by SteveArgyle on Deviantart" width="150" src="https://user-images.githubusercontent.com/10023615/83328359-fb6dd380-a29f-11ea-9f3e-07499b8f0cd2.jpg"/></a>

# C3PO
When he's not flying around with the Solos and Skywalkers on the Millenium Falcon, C-3PO decided to help LTTKGP out with managing the huge amount of songs being posted each day to the group and organising them in a database (such a nice guy!) so we can build cool functionality on top of it.

## Getting started
These instructions will get you a copy of the project up and running on your local machine for development and testing purposes. See deployment for notes on how to deploy the project on a live system.

### Prerequisites
- Python 3.6+ with `pip` for installing packages
- Virtualenv (recommended)
- Postgres (can be local or remote)
- MongoDB (can be local or remote)
- <details>
    <summary> Facebook Graph API Credentials </summary>

    You will need 'User access tokens' to work with the Graph API. You can find more information here: [Graph API documentation](https://developers.facebook.com/docs/graph-api/overview#step2).

    As explained in the link above, create a new Facebook app (My Apps -> Add a new app) and generate user access tokens through the Graph API explorer.
  </details>
- <details>
    <summary> Spotify Web API Credentials </summary>

    You will also need Spotify authorization for fetching song metadata. The prodcude is very straightforward. Register a new application here:
    [Spotify for Developers](https://developer.spotify.com/my-applications)

    That will give you a unique **client ID** and **client secret key** to use in authorization flows.
  </details>

### Setting up
- Create a `.env` file, using the `.env.template` file as reference.
  ```sh
  cp .env.template .env
  ```
  Fill all the fields using the credentials created as part of the pre-requisites.
- Create a `.config.ini` file, using the `.config.template.ini` file as reference.
  ```sh
  cp .config.template.ini .config.ini
  ```
  Update the `[mongo]` and `[postgres]` sections with credentials to your DB instances.
- Install Python requirements
  ```sh
  pip install -r requirements.txt
  ```

### Running the Flask server
Run the flask server with:
```sh
flask run
```
The API server should be accessible at http://localhost:5000/.

### Populating the database
TODO: Add instructions to run the job

## Contributing
Contributions are always welcome. Your contributions could either be creating new features, fixing bugs or improving documentation and examples. Find more detailed information in [CONTRIBUTING.md](.github/CONTRIBUTING.md).

## License
[MIT](LICENSE)
