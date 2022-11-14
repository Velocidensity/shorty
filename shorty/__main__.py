from shorty import app


def run():
    app.run(
        host=app.config['BIND_HOST'],
        port=app.config['BIND_PORT']
    )


if __name__ == "__main__":
    run()
