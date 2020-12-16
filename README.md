<a href="https://www.deviantart.com/steveargyle/art/C-3PO-578309067"><img align="right" alt="C3PO by SteveArgyle on Deviantart" width="150" src="https://user-images.githubusercontent.com/10023615/83328359-fb6dd380-a29f-11ea-9f3e-07499b8f0cd2.jpg"/></a>

# C3PO

When he's not flying around with the Solos and Skywalkers on the Millenium Falcon, C-3PO decided to help LTTKGP out with managing the huge amount of songs being posted each day to the group and organising them in a database (such a nice guy!) so we can build cool functionality on top of it.

## Getting started

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes.

### Prerequisites

- Docker & Docker Compose
- <details>
    <summary> Spotify Web API Credentials </summary>

  You will also need Spotify authorization for fetching song metadata. The prodcude is very straightforward. Register a new application here:
  [Spotify for Developers](https://developer.spotify.com/my-applications)

  That will give you a unique **client ID** and **client secret key** to use in authorization flows.
  </details>

- <details>
    <summary>Google Application Credentials</summary>
    
    Google Application Credentials is an API key that is required to extract YouTube metadata from the Youtube Data API. To get the key, create a new project on the [Google Developer Console](https://console.developers.google.com/), enable the YouTube Data API and proceed to `Credentials` and create a new API key.
  </details>

### Setting up

- Create a `.env` file, using the `.env.template` file as reference.

  ```sh
  cp .env.template .env
  ```

  Fill all the fields using the credentials created as part of the pre-requisites.

### Starting the server

Run the server with:

```sh
docker-compose up
```

The API server should be accessible at http://localhost:8000/.

### Populating the database

Follow the instructions on [R2-D2](https://github.com/lttkgp/R2-D2) and start it.

## Contributing

Contributions are always welcome. Your contributions could either be creating new features, fixing bugs or improving documentation and examples. Find more detailed information in [CONTRIBUTING.md](.github/CONTRIBUTING.md).

## License

[MIT](LICENSE)
